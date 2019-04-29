from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import CommentsForm, UpdateProfile, PostForm, 
from ..models import Comment, Post, User,Role
from flask_login import login_required, current_user
from .. import db,photos

import markdown2



@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to The best Blogging Website Online'

 
    post= post.get_all_posts()

    return render_template('index.html', title = title)

@main.route('/post/<int:post_id>')
def post(post_id):

    '''
    View post page function that returns the post details page and its data
    '''
    found_post= get_post(post_id)
    title = post_id
    post_comments = Comment.get_comments(post_id)

    return render_template('post.html',title= title ,found_post= found_post, post_comments= post_comments)

@main.route('/blog/post/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_post(id):
    form = PostForm()
    blog = get_blog(id)
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data

        # Updated post instance
        new_post = Post(blog_id=blog.id,blog_title=title,image_path=blog.poster,blog_post=post,user=current_user)

        # save post method
        new_post.save_review()
        return redirect(url_for('.blog',id = blog.id ))

    title = f'{blog.title} post'
    return render_template('new_post.html',title = title, post_form=form, blog=blog)

@main.route('/post/<int:id>')
def single_post(id):
    post=Post.query.get(id)
    if post is None:
        abort(404)
    format_post = markdown2.markdown(post.blog_post,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('post.html',post = post,format_post=format_post)


@main.route('/post/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    if form.validate_on_submit():
        new_comment = Comment(post_id =id,comment=form.comment.data,username=current_user.username)
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
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments = comments, id=id)