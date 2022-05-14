from App.User import User

class UserManager():
	def __init__(self, DAO):
		self.user = User(DAO.db.user)
		self.book = DAO.db.book
		self.dao = self.user.dao

	def list(self):
		user_list = self.dao.list()

		return user_list

	def signin(self, email, password):
		user = self.dao.getByEmail(email)

		if user is None:
			return False

		user_pass = user['password'] # user pass at 
		if user_pass != password:
			return False

		return user

	def signout(self):
		self.user.signout()
		
	def get(self, id):
		user = self.dao.getById(id)

		return user

	def signup(self, name, email, password):
		user = self.dao.getByEmail(email)

		if user is not None:
			return "already_exists"

		user_info = {"name": name, "email": email, "password": password, "bio": '', "mob": '', "lock": '0'}
		
		new_user = self.dao.add(user_info)

		return new_user
		
	def get(self, id):
		user = self.dao.getById(id)

		return user
		
	def update(self, name, email, password, bio, id):
		user_info = {"name": name, "email": email, "password": password, "bio":bio}
		
		user = self.dao.update(user_info, id)

		return user

	def getBooksList(self, id):
		return self.book.getBooksByUser(id)

	def getSendList(self, id):
		return self.dao.getSendByUser(id)

	def getInboxList(self, id):
		return self.dao.getInboxByUser(id)

	def getUsersByBook(self, book_id):
		return self.dao.getUsersByBook(book_id)

	def delete(self, id):
		self.dao.delete(id)

	def be_admin(self, id):
		self.dao.be_admin(id)

	def getUserId(self, email):
		return self.dao.getByEmail(email)
	
	def getDocument(self, id):
		return self.dao.getDocumentByUser(id)

	def sendDocument(self, sender_id, receiver_id, title, description, file_path, removed_at):
		return self.dao.send_document(sender_id, receiver_id, title, description, file_path, removed_at)

	def checkDeadline(self, now_time):
		return self.dao.check_deadline(self, now_time)

	def addArchive(self, sender_id, receiver_id, title, description, file_path, created_at):
		return self.dao.add_archive(sender_id, receiver_id, title, description, file_path, created_at)

	def showAllArchived(self):
		return self.dao.show_all_archived()
	
	def showOneArchived(self, id):
		return self.dao.show_one_archived(id)