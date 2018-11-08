from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:localonly@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key ="KJ75259"

db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body =  db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/newpost', methods = ['POST', 'GET'])
def make_a_post():

    if request.method == 'POST':
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
            new_post = BlogPost(post_title, post_body)    #building a new BlogPost object with the BlogPost constructer
            db.session.add(new_post)
            db.session.commit()                          #finishing up adding the object to the db
            post_count = post_count + 1
            display_post_title = Task.query.filter_by(id=post_count).all()
            display_post_body = Task.query.filter_by(id=post_count).all()


    if request.method == 'GET':
        return render_template('add-post.html')     #renders the template

@app.route('/blog', methods = ['POST', 'GET'])

def index():                                         #slimmed down rendering of the blog template

    post_id = request.args.get('id')
    if post_id == None:
        postings = BlogPost.query.all()                          #if the requested id param is none then
        return render_template('view-post.html', postings=postings)  #we just render the front page

    else:
        single_post = BlogPost.query.filter_by(id=post_id).all() #if not I filter the BlogPosts by the id then render
        return render_template('one-post.html', postings=single_post)







if __name__ =="__main__":            #you know what this does
    app.run()
