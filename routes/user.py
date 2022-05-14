from crypt import methods
from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash, Flask
from app import DAO
from Misc.functions import *
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from datetime import datetime

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kerim123'
app.config['UPLOAD_PATH'] = 'static/media'

def sensor():
	now_time = datetime.now().date()
	user_manager.dao.check_deadline(str(now_time))

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=60)
sched.start()



from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():

	g.bg = 1

	sensor()

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")

		d = user_manager.signin(email, (password))

		if d and len(d)>0:
			session['user'] = int(d['id'])

			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')
		print(name, email, password)

		if len(name) < 1 or len(email)<1 or len(password)<1:
			return render_template('signup.html', error="All fields are required")

		new_user = user_manager.signup(name, email, (password))

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")


		return render_template('signup.html', msg = "You've been registered!")


	return render_template('signup.html')


@user_view.route('/privacy', methods=['GET'])
def privacy():

	return render_template('privacy.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	user_manager.update(name, email, (password), bio, user_manager.user.uid())

	flash('Your info has been updated!')
	return redirect("/user/")



# Activity page

@user_view.route('/activity/', methods=['GET', 'POST'])
@user_manager.user.login_required
def show_activity():
	user_manager.user.set_session(session, g)
	
	id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)
	myarchives = user_manager.showAllArchived()
	myinbox = user_manager.getInboxList(user_manager.user.uid())
	mysend = user_manager.getSendList(user_manager.user.uid())

	print(myarchives)


	if request.method == 'POST':
		_form = request.form
		file = request.files["file"]

		file.save(os.path.join(app.config['UPLOAD_PATH'], str(secure_filename(file.filename))))

		print(app.config['UPLOAD_PATH'])
		print(str(app.config['UPLOAD_PATH'] + '/' + str(secure_filename(file.filename))))

		reciever_email = str(_form["reciever"])
		title = str(_form["title"])
		description = str(_form["description"])
		file_path = str(app.config['UPLOAD_PATH'] + '/' + str(secure_filename(file.filename)))[7:]
		removed_at = str(_form["removed_at"])

		receiver = user_manager.getUserId(reciever_email)


		user_manager.sendDocument(id, receiver['id'], title, description, file_path, removed_at)

 


	return render_template("activity.html", user=d, books=mybooks, archives=myarchives, inboxes=myinbox, sends=mysend, g=g, book = 'kerim')



@user_view.route('/activity', methods=['GET'])
def search():
	user_manager.user.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("activity.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/activity')

	id = int(user_manager.user.uid())
	user = user_manager.get(id)

	d=user_manager.search(keyword, 0)

	if len(d) >0:
		return render_template("activity.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, user=user)

	return render_template('activity.html', error="No users found!", keyword=escape(keyword))



# inbox page
@user_view.route('/inboxes', methods=['GET'])
def inbox():
	user_manager.user.set_session(session, g)

	id = int(user_manager.user.uid())


	return render_template('inbox.html')




@user_view.route('/inboxes/<int:inbox_id>', methods=['GET'])
def inbox_detail(inbox_id):
	user_manager.user.set_session(session, g)

	# id = int(user_manager.user.uid())
	myinbox = user_manager.getDocument(inbox_id)

	sender_email = user_manager.get(myinbox['sender_id'])['email']


	return render_template('inbox.html', myinbox=myinbox, sender_email=sender_email)


@user_view.route('/inboxes/<int:inbox_id>', methods=['POST'])
def inbox_detail_post(inbox_id):
	user_manager.user.set_session(session, g)

	# id = int(user_manager.user.uid())
	myinbox = user_manager.getDocument(inbox_id)

	sender_email = user_manager.get(myinbox['sender_id'])['email']

	if request.method == 'POST':
		_form = request.form.to_dict()

		for key in _form:
			print((key))
			if key == 'increase_deadline':
				pass
			if key == 'change_executer':
				pass
			if key == 'archive_document':
				user_manager.addArchive(myinbox['sender_id'], myinbox['receiver_id'], myinbox['title'], myinbox['description'], myinbox['filepath'], myinbox['create_at'])
				

		




	return render_template('inbox.html', myinbox=myinbox, sender_email=sender_email)








# send page
@user_view.route('/send', methods=['GET'])
def send():
	user_manager.user.set_session(session, g)

	id = int(user_manager.user.uid())


	return render_template('send.html')




@user_view.route('/send/<int:send_id>', methods=['GET'])
def send_detail(send_id):
	user_manager.user.set_session(session, g)

	mysends = user_manager.getDocument(send_id)

	receiver_email = user_manager.get(mysends['receiver_id'])['email']



	return render_template('send.html', mysends=mysends, receiver_email=receiver_email)


@user_view.route('/send/<int:send_id>', methods=['POST'])
def send_detail_post(send_id):
	user_manager.user.set_session(session, g)

	mysends = user_manager.getDocument(send_id)

	receiver_email = user_manager.get(mysends['receiver_id'])['email']
	
	
	if request.method == 'POST':
		_form = request.form
		deadline = str(_form['archive'])

		user_manager.addArchive(mysends['sender_id'], mysends['receiver_id'], mysends['title'], mysends['description'], mysends['filepath'], mysends['create_at'])




	return render_template('send.html', mysends=mysends, receiver_email=receiver_email)




# archive page
@user_view.route('/archive', methods=['GET'])
def archive():
	user_manager.user.set_session(session, g)

	id = int(user_manager.user.uid())


	return render_template('archive.html')




@user_view.route('/archive/<int:id>', methods=['GET'])
def archive_detail(id):
	user_manager.user.set_session(session, g)

	myarchives = user_manager.showOneArchived(id)

	receiver_email = user_manager.get(myarchives['receiver_id'])['email']

	print(receiver_email, myarchives['receiver_id'])



	return render_template('archive.html', myarchives=myarchives, receiver_email=receiver_email)