from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:localonly@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

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

        new_post = BlogPost(post_title, post_body)    #building a new BlogPost object with the BlogPost constructer
        db.session.add(new_post)
        db.session.commit()                          #finishing up adding the object to the db
        return redirect('/blog')
    else:
        return render_template('add-post.html')     #renders the template

@app.route('/blog', methods = ['POST', 'GET'])

def index():                                         #slimmed down rendering of the blog template
    postings = BlogPost.query.all()
    return render_template('view-post.html', postings=postings)







if __name__ =="__main__":            #you know what this does
    app.run()
