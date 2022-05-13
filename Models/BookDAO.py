class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "books"

	def add (self, title, count, edition, author, availability, description):
		q = self.db.query("INSERT INTO books (`name`, `desc`, `author`, `availability`, `edition`, `count`) VALUES('{}', '{}', '{}', '{}', '{}', {});".format(title, description, author, availability, edition, count))
		self.db.commit()
		return q

	def update (self, id, title, count, availability, description):
		q = self.db.query("UPDATE books SET `name` = '{}', `desc` = '{}', `availability` = '{}', `count` = {} WHERE id = {};".format(title, description, availability, count, id))
		self.db.commit()
		return q

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q


	def reserve(self, user_id, book_id):
		if not self.available(book_id):
			return "err_out"

		q = self.db.query("INSERT INTO reserve (user_id, book_id) VALUES('{}', '{}');".format(user_id, book_id))
		
		self.db.query("UPDATE @table set count=count-1 where id={};".format(book_id))
		self.db.commit()

		return q

	def getBooksByUser(self, user_id):
		q = self.db.query("select * from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		# print(books)
		return books

	def getBooksCountByUser(self, user_id):
		q = self.db.query("select count(reserve.book_id) as books_count from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBook(self, id):
		q = self.db.query("select * from @table where id={}".format(id))

		book = q.fetchone()

		print(book)
		return book

	def available(self, id):
		book = self.getById(id)
		count = book['count']

		if count < 1:
			return False

		return True

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		book = q.fetchone()

		return book

	def list(self, availability=1):
		query="select * from @table"
		# Usually when no-admin user query for book
		if availability==1: query= query+"  WHERE availability={}".format(availability)
		
		books = self.db.query(query)
		
		books = books.fetchall()


		return books

	def getReserverdBooksByUser(self, user_id):
		query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
		
		books = self.db.query(query)
		
		books = books.fetchone()


		return books

	def search_book(self, name, availability=1):
		query="select * from @table where name LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books