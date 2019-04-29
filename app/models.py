from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    post = db.relationship('Post',backref = 'users',lazy="dynamic")

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        reviews = Comment.query.filter_by(post_id=id).all()
        return comments

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'

class Post(db.Model):
    '''
    Post class to define Post Objects
    '''
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key = True)
    post = db.Column(db.String)
    category_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'post',lazy="dynamic")


    def save_post(self):
        '''
        Function that saves posts
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_posts(cls):
        '''
        Function that queries the databse and returns all the posts
        '''
        return Post.query.all()

    @classmethod
    def get_posts_by_category(cls,cat_id):
        '''
        Function that queries the databse and returns posts based on the
        category passed to it
        '''
        return Posts.query.filter_by(category_id= cat_id)



class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment= db.Column(db.String)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    username =  db.Column(db.String)


    def save_comment(self):
        '''
        Function that saves comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()

        return comments

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'
