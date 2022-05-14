from xml.dom.minidom import Document


class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "users"

	def list(self):
		users = self.db.query("select @table.id,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY reserve.user_id").fetchall()

		return users

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where email='{}'".format(email))

		user = q.fetchone()

		return user
	
	def getInboxByUser(self, id):
		q = self.db.query("select * from document where receiver_id = {}".format(id))

		inboxes = q.fetchall()

		return inboxes

	def getDocumentByUser(self, id):
		q = self.db.query("select * from document where id = {}".format(id))

		document = q.fetchone()

		return document


	def getSendByUser(self, id):
		q = self.db.query("select * from document where sender_id = {}".format(id))

		sends = q.fetchall()

		return sends

	def check_deadline(self, now_time):
		q = self.db.query("delete from document where removed_at <= '{}'".format(now_time))
		self.db.commit()

		return q
	

	def add(self, user):
		name = str(user['name'])
		email = str(user['email'])
		password = str(user['password'])

		q = self.db.query("INSERT INTO @table (name, email, password, bio, mob, `lock`) VALUES('{}', '{}', '{}', '{}', '{}', {});".format(name, email, password, '', '', 0))
		self.db.commit()
		
		return q


	def update(self, user, _id):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user['bio']

		q = self.db.query("UPDATE @table SET name = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(name, email, password, bio, _id))
		self.db.commit()
		
		return q

	def delete(self, id):
		q = self.db.query("DELETE from @table where id='{}'".format(id))
		self.db.commit()
		user = q.fetchone()

		return user


	def be_admin(self, id):
		user_email = self.db.query("SELECT email FROM @table where id = '{}'".format(id)).fetchone()
		user_password = self.db.query("SELECT password FROM @table where id = '{}'".format(id)).fetchone()

		q = self.db.query("INSERT INTO admin (email, password) VALUES('{}', '{}')".format(user_email['email'], user_password['password']))
		self.db.commit()		
		# return q
	def send_document(self, sender_id, receiver_id, title, description, file_path, removed_at):	
		q = self.db.query("INSERT INTO document (sender_id, receiver_id, title, description, filepath, removed_at) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(sender_id, receiver_id, title, description, file_path, removed_at))
		self.db.commit()
		


	# Add archive table
	def add_archive(self, sender_id, receiver_id, title, description, file_path, created_at):
		q = self.db.query("INSERT INTO archive (sender_id, receiver_id, title, description, file_path, create_at) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(sender_id, receiver_id, title, description, file_path, created_at))
		self.db.commit()

		return q

	# Show all archived document
	def show_all_archived(self):
		documents = self.db.query("SELECT * FROM archive")
		documents = documents.fetchall()
		self.db.commit()

		return documents

	
	# Show one archived document
	def show_one_archived(self, id):
		documents = self.db.query("SELECT * FROM archive WHERE id = '{}'".format(id))
		document = documents.fetchone()
		self.db.commit()

		return document