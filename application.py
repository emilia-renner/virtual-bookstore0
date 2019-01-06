# Import packages
import os
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Book
from flask import session as login_session
from flask import make_response, send_from_directory
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from werkzeug.utils import secure_filename
import random
import string
import httplib2
import json
import requests

app = Flask(__name__, template_folder='templates')

# Import client ID information for Gplus signin
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Virtual Bookstore"

engine = create_engine('sqlite:///virtual_bookstore.db?check_same_thread=False')  # noqa E501
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect to Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    print(login_session['gplus_id'])

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    print(data)

    login_session['username'] = data.get('name', False)
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome '
    if login_session['username']:
        output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; '\
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    if login_session['username']:
        flash("You are now logged in as %s." % login_session['username'])
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])  # noqa E501
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    user = session.query(User).filter_by(email=email).one()
    return user.id


# Disconnect from Google - Revoke a current user's token
# and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON Endpoints
@app.route('/categories/<int:category_id>/JSON')
def categoriesJSON(category_id):
    books = session.query(Book).filter_by(category_id=category_id).all()
    return jsonify(Books=[i.serialize for i in books])


@app.route('/categories/<int:category_id>/<int:book_id>/JSON')
def bookJSON(category_id, book_id):
    book = session.query(Book).filter_by(id=book_id).all()
    return jsonify(BookInfo=[i.serialize for i in book])


# Initial routing function which queries the categories database- main page
@app.route('/', methods=['GET', 'POST'])
def categories():
    categories = session.query(Category).all()
    return render_template('main.html', categories=categories)


# Routing function to add a new category to the categories database
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    if request.method == 'POST':
        newItem = Category(name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New category, %s, successfully created.'
              '  You can now add books for this category.'
              % newItem.name)
        return redirect(url_for('categories'))
    else:
        return render_template('addCategory.html')


# Routing function to delete a category you have created
@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    itemToDelete = session.query(Category).filter_by(id=category_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this category.')
        return redirect(url_for('categories'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('categories'))
    else:
        return render_template('deleteCategory.html',
                               category_id=category_id,
                               item=itemToDelete)


# Routing function to view all books in a category
@app.route('/categories/<int:category_id>')
def books(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template('books.html',
                           category=category,
                           books=books,
                           category_id=category_id,
                           creator=creator)


# routing function to view a particular book
@app.route('/categories/<int:category_id>/<int:book_id>')
def viewBook(category_id, book_id):
    category = session.query(Category).filter_by(id=category_id).one()
    book = session.query(Book).filter_by(id=book_id).one()
    creator = getUserInfo(category.user_id)
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template('viewBook.html',
                           category=category,
                           books=books,
                           book=book,
                           category_id=category_id,
                           book_id=book_id,
                           creator=creator)


# Allow for the user to upload images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# Determine if file uploaded by the user is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# routing funtion to add a new book to a category
@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newBook(category_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newItem = Book(name=request.form['name'],
                       picture=filename,
                       author=request.form['author'],
                       description=request.form['description'],
                       category_id=category_id,
                       user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New book successfully created for %s." % newItem.name)
        return redirect(url_for('books', category_id=category_id))
    else:
        return render_template('create.html', category_id=category_id)


# routing funtion to edit information about a book
@app.route('/categories/<int:category_id>/<int:book_id>/edit', methods=['GET', 'POST'])  # noqa E501
def editBook(category_id, book_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    editedItem = session.query(Book).filter_by(id=book_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    book = session.query(Book).filter_by(id=book_id).one()
    if login_session['user_id'] != book.user_id:
        flash('You are not authorized to edit this book.')
        return redirect(url_for('books', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
            flash('Book successfully edited.')
        else:
            flash('Please edit name or enter a new name in order to edit additional information.')  # noqa E501
        return redirect(url_for('books', category_id=category_id))
    else:
        return render_template('edit.html',
                               category_id=category_id,
                               book_id=book_id,
                               item=editedItem)


# routing function to delete a particular book
@app.route('/categories/<int:category_id>/<int:book_id>/delete', methods=['GET', 'POST'])  # noqa E501
def deleteBook(category_id, book_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    itemToDelete = session.query(Book).filter_by(id=book_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this book.')
        return redirect(url_for('books', category_id=category_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('books', category_id=category_id))
    else:
        return render_template('delete.html',
                               category_id=category_id,
                               book_id=book_id,
                               item=itemToDelete)


# uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    print(login_session)
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('categories'))
    else:
        flash('You were not logged in')
        return redirect(url_for('categories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
