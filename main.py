from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from verify import verify_password, verify_email
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:testonly@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key ="KJ75259"

db = SQLAlchemy(app)

class User(db.Model):
    """docstring for BlogPost."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('BlogPost', backref='owner')   #reference to BlogPost owner

    def __init__(self, email, password):

        self.email = email
        self.password = password




class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body =  db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body

        self.owner = owner           #logged through User

@app.before_request               #before_request reroutes to white-listed routes
def require_login():
    allowed_routes = ['login', 'register', 'blog_view', 'index']    #list
    if request.endpoint not in allowed_routes and 'email' not in session: #uses list to run a selection
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']           #pulls the email and pass from login form
        password = request.form['password']
        user = User.query.filter_by(email=email).first()  #queries the User db for first user with that email
        if user and user.password == password:      # if there IS that user, and if their password = the db password
            session['email'] = email                #it goes ahead and stores their email in the session data
            flash('Logged in')
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            #TODO this needs to be two separate messages

    return render_template('login.html')




@app.route('/register', methods=['POST', 'GET'])           #added register route
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']             #pulls the form data
        verify = request.form['verify']

        if verify_password(password, verify) == True:

            existing_user = User.query.filter_by(email=email).first() #sees if the user exists already
            if not existing_user:                                     #if not
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()                     #creates user
                session['email'] = email                      #adds users email to session
                return redirect('/newpost')
            else:
                flash('Duplicate User, please log in or use a different email.')         #error case message
                return render_template('register.html', email=email)                     #rendering again showing error message

        else:
            flash(verify_password(password, verify), 'error')
            return render_template('register.html', email=email)


    if request.method == 'GET':

        return render_template('register.html')                            #simple render for GET

@app.route('/logout')                                     #logout function
def logout():
    del session['email']                                  #deletes session
    return redirect('/blog')

@app.route('/newpost', methods = ['POST', 'GET'])
def make_a_post():

    if request.method == 'POST':
        owner = User.query.filter_by(email=session['email']).first()
        post_title = request.form['title']    #passing the title from the form into python
        post_body = request.form['blog-entry'] #passing the body from the form into python
        if post_title =="" and post_body =="":
            flash('Missing post title, and your post doesn\'t have any words', 'error')
            return redirect('/newpost')
        elif post_title == "":
            flash('Please fill out the title field', 'error')    #error conditional with flash messages.
            return render_template('add-post.html', post_body=post_body)
        elif post_body == "":
            flash('Please fill out the text box', 'error')
            return render_template('add-post.html', post_title=post_title)


        else:
            new_post = BlogPost(post_title, post_body, owner)    #building a new BlogPost object with the BlogPost constructer
            db.session.add(new_post)                            #passing in "owner" also
            db.session.commit()                          #finishing up adding the object to the db

                            # hopefully this pulls the last id value.
            single_post = BlogPost.query.filter_by(title=post_title).all() #filters by the value just stated
            return render_template('one-post.html',postings=single_post) #renders template passing in that param


    if request.method == 'GET':
        return render_template('add-post.html')     #renders the template

@app.route('/blog', methods = ['POST',  'GET'])

def blog_view():                                         #slimmed down rendering of the blog template
    user_id = request.args.get('userid')
    owner = User.query.filter_by(id=user_id).first()
    post_id = request.args.get('id')
    if post_id == None:
        if user_id:
            posts = BlogPost.query.filter_by(owner=owner).all()
            return render_template('user-posts.html', posts=posts)
        postings = BlogPost.query.all()                          #if the requested id param is none then
        return render_template('view-post.html', postings=postings)  #we just render the front page

    else:
        single_post = BlogPost.query.filter_by(id=post_id).all() #if not I filter the BlogPosts by the id then render
        return render_template('one-post.html', postings=single_post)

@app.route('/', methods = ['POST', 'GET'])

def index():

    users = User.query.all()
    if request.method == 'GET':
        return render_template('index.html', users=users)










if __name__ =="__main__":            #you know what this does
    app.run()
