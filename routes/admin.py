from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, Flask
from app import DAO
from Misc.functions import *

from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager
from werkzeug.utils import secure_filename


import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kerim123'
app.config['UPLOAD_PATH'] = 'static/media'

admin_view = Blueprint('admin_routes', __name__, template_folder='../templates/admin/', url_prefix='/admin')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


@admin_view.route('/', methods=['GET'])
@admin_manager.admin.login_required
def home():
	admin_manager.admin.set_session(session, g)

	return render_template('admin/home.html', g=g)


@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signin():
	g.bg = 1
	
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('admin/signin.html', error="Email and password are required")

		d = admin_manager.signin(email, (password))

		if d and len(d)>0:
			session['admin'] = int(d["id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.admin.login_required
def signout():
	admin_manager.signout()

	return redirect("/admin/", code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.admin.login_required
def users_view():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	myusers = admin_manager.getUsersList()


	return render_template('users.html', g=g, admin=admin, users=myusers)


@admin_view.route('/users/delete/<int:id>', methods=['POST'])
@admin_manager.admin.login_required
def users_delete(id):
	admin_manager.admin.set_session(session, g)

	id = int(id)

	if id is not None:
		user_manager.delete(id)
	admin = admin_manager.get(id)
	myusers = admin_manager.getUsersList()

	return render_template('users.html', g=g, admin=admin, users=myusers)




@admin_view.route('/users/be_admin/<int:id>', methods=['POST'])
@admin_manager.admin.login_required
def users_admin(id):
	admin_manager.admin.set_session(session, g)

	id = int(id)

	if id is not None:
		user_manager.be_admin(id)
	admin = admin_manager.get(id)
	myusers = admin_manager.getUsersList()

	return render_template('users.html', g=g, admin=admin, users=myusers)



# Control section
@admin_view.route('/control/', methods=['GET'])
@admin_manager.admin.login_required
def control():
	admin_manager.admin.set_session(session, g)
	documents = admin_manager.dao.getAllDocumentByAdmin()

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)

	return render_template('admin/control.html', g=g, admin = admin, documents = documents)


@admin_view.route('control/details/<int:control_id>', methods=['GET'])
@admin_manager.admin.login_required
def control_details(control_id):
	admin_manager.admin.set_session(session, g)

	if control_id != None:


		id = int(admin_manager.admin.uid())
		admin = admin_manager.get(id)
		document_info = admin_manager.getDocumentList(control_id)

		myusers = admin_manager.getUsersList()
		sender = admin_manager.user.getById(document_info['sender_id'])
		reciever = admin_manager.user.getById(document_info['receiver_id'])

		print(document_info['filepath'])

		return render_template('admin/control-details.html', g=g, admin = admin, users = myusers, reciever = reciever['name'], sender = sender['name'], sender_email=sender['email'], receiver_email=reciever['email'], document_title = document_info['title'], document_description = document_info['description'], file_path = document_info['filepath'], send_time = document_info['create_at'], removed_at = document_info['removed_at'])





# Books actions
@admin_view.route('/books/', methods=['GET'])
@admin_manager.admin.login_required
def books():
	admin_manager.admin.set_session(session, g)

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)
	mybooks = book_manager.list(availability=0)

	return render_template('books/views.html', g=g, books=mybooks, admin=admin)

@admin_view.route('/books/<int:id>')
@admin_manager.admin.login_required
def view_book(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)
		users = user_manager.getUsersByBook(id)

		print('----------------------------')
		# print(users)
		
		if b and len(b) <1:
			return render_template('books/book_view.html', error="No Documents found!")

		return render_template("books/book_view.html", books=b, books_owners=users, g=g, file_path=b['filepath'])


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_add():
	admin_manager.admin.set_session(session, g)

	if request.method == 'POST':
		_form = request.form
		title = str(_form['title'])
		qty = _form['qty']
		description = str(_form['desc'])

		file = request.files["file"]

		file.save(os.path.join(app.config['UPLOAD_PATH'], str(secure_filename(file.filename))))
		file_path = str(app.config['UPLOAD_PATH'] + '/' + str(secure_filename(file.filename)))[7:]

		print(file_path)


		book_manager.add(title, qty, '1', 'Admin', '1', description, file_path)
		
		# return render_template('books/add', g=g)
	
	return render_template('admin/books/add.html', g=g)


@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_edit(id):
	admin_manager.admin.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)

		if b and len(b) <1:
			return render_template('edit.html', error="No documents found!")
		else:
			if request.method == 'POST':
				_form = request.form
				title = str(_form['title'])
				qty = _form['qty']
				description = str(_form['desc'])

				book_manager.update(id, title, qty, '0', description)

			return render_template("books/edit.html", book=b, g=g)
	
	return redirect('/books')

@admin_view.route('/books/delete/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def book_delete(id):
	id = int(id)

	if id is not None:
		book_manager.delete(id)
	
	return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
def search():
	admin_manager.admin.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("books/view.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/admin/books')

	id = int(admin_manager.admin.uid())
	admin = admin_manager.get(id)

	d=book_manager.search(keyword, 0)

	if len(d) >0:
		return render_template("books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

	return render_template('books/views.html', error="No documents found!", keyword=escape(keyword))

