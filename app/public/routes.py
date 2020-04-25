from flask import abort, render_template, redirect, url_for
from app.models import Post
from .forms import CommentForm
from app.models import Comment
from . import public_bp
from ..auth.routes import current_user


@public_bp.route('/')
def index():
    posts = Post.get_all()
    return render_template('public/index.html', posts=posts)


@public_bp.route('/p/<int:post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.get_post_id(post_id)
    # print('post -->', post)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        coment_form = form.comment.data
        comentario = Comment(current_user.id, post_id, coment_form)
        comentario.save()
        return redirect(url_for('public.show_post', post_id=post_id))
    return render_template('public/post_view.html', post=post, form=form)
