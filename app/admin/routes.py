from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.models import Post
from . import admin_bp
from .forms import PostForm


@admin_bp.route('/admin/post/', methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route('/admin/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def post_form(post_id=None):
    form = PostForm()

    if form.validate_on_submit():
        titulo = form.title.data
        titulo_slug = form.title_slug.data
        content_form = form.content.data
        next = request.args.get('next')

        post = Post(title=titulo, content=content_form, user_id=current_user.id)
        post.save()

        if next:
            return redirect(next)
        return redirect(url_for('public.index'))

    return render_template('admin/post_form.html', form=form)