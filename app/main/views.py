from flask import render_template, request, redirect, url_for, abort
from . import main
from ..requests import get_quote
from .forms import CommentsForm, UpdateProfile,BlogForm 
from ..models import Comment, Blog, User,Role
from flask_login import login_required, current_user
from .. import db,photos

import markdown2

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    disp_quotes = get_quote()
    quote=disp_quotes["quote"]
    quote_author=disp_quotes["author"]
    # blog= blog.get_all_blogs()
    title = 'Home - Welcome to The best Blogging Website Online'
    return render_template('index.html', title = title , quote = quote, quote_author = quote_author)

#this section consist of the category root functions

@main.route('/fashion')
def fashion():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Fashion'
    return render_template('fashion.html', title = title )

@main.route('/food')
def food():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Food Blogs'

    blogs= Blog.get_all_blogs()

    return render_template('food.html', title = title, blogs= blogs )

@main.route('/travel')
def travel():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Travel Blogs'

    blogs= Blog.get_all_blogs()

    return render_template('travel.html', title = title, blogs= blogs )

@main.route('/music')
def music():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Music Blogs'

    blog= Blog.get_all_blogs()

    return render_template('music.html', title = title, blogs= blogs )


@main.route('/lifestyle')
def lifestyle():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Lifestyle Blogs'
    blogs= Blog.get_all_blogs()
    return render_template('lifestyle.html', title = title, blogs= blogs )

@main.route('/blog/<int:blog_id>')
def blog(blog_id):

    '''
    View blog page function that returns the pitch details page and its data
    '''
    found_blog= get_blog(blog_id)
    title = blog_id
    blog_comments = Comment.get_comments(blog_id)

    return render_template('blog.html',title= title ,found_blog= found_blog, blog_comments= blog_comments)

@main.route('/search/<blog_name>')
def search(blog_name):
    '''
    View function to display the search results
    '''
    searched_blogs = search_blog(blog_name)
    title = f'search results for {blog_name}'

    return render_template('search.html',blogs = searched_blogs)

@main.route('/blog/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    '''
    Function that creates new 
    '''
    form = BlogForm()


    if category is None:
        abort( 404 )

    if form.validate_on_submit():
        blog= form.content.data
        category_id = form.category_id.data
        new_blog= Blog(blog= blog, category_id= category_id)

        new_blog.save_blog()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', new_blog_form= form , category= category)

@main.route('/category/<int:id>')
def category(id):
    '''
    function that returns pitches based on the entered category id
    '''
    category = BlogCategory.query.get(id)

    if category is None:
        abort(404)

    blogs_in_category = Blogs.get_blog(id)
    return render_template('category.html' ,category= category, blogs= blogs_in_category)

@main.route('/blog/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    if form.validate_on_submit():
        new_comment = Comment(blog_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comment()
        return redirect(url_for('main.index'))
    return render_template('new_comment.html',comment_form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular blog
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)