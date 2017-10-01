from flask import render_template, session, redirect, url_for, flash
from playhouse.flask_utils import get_object_or_404, object_list

from app.decorators import login_required
from . import main
from .forms import PostForm, EditProfileForm
from ..models import User, Post
from ..utils import get_current_user, redirect_url


@main.route('/')
def index():
    if session.get('logged_in'):
        return private_time_line()
    return public_time_line()


@main.route('/private')
@login_required
def private_time_line():
    user = get_current_user()
    posts = Post.select().where((Post.author << user.following()) | (Post.author == user))
    if not posts:
        flash('You can find some interesting posts and follow their author.')
        return public_time_line()
    return object_list('index.html', posts, check_bounds=False, context_variable='posts_list')


@main.route('/public')
def public_time_line():
    posts = Post.select()
    return object_list('index.html', posts, check_bounds=False, context_variable='posts_list')


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    user = get_current_user()
    form = PostForm()
    if form.validate_on_submit():
        Post.create(content=form.content.data, author_id=user.id)
        return redirect(url_for('.index'))
    form.content.data = ''
    return render_template('create_post.html', form=form)


@main.route('/user/<username>/following')
@login_required
def following(username):
    user = get_object_or_404(User, User.username == username)
    return object_list('follows.html', user.following(), check_bounds=False, context_variable='follows_list', user=user,
                       endpoint='main.following')


@main.route('/user/<username>/followers')
@login_required
def followers(username):
    user = get_object_or_404(User, User.username == username)
    return object_list('follows.html', user.followers(), check_bounds=False, context_variable='follows_list', user=user,
                       endpoint='main.followers')


@main.route('/user/<username>/follow')
@login_required
def follow(username):
    user = get_object_or_404(User.select(), (User.username == username))
    if get_current_user().follow(user):
        flash('You follow {}'.format(user.username))
    return redirect(url_for('main.user_detail', username=user.username))


@main.route('/user/<username>/unfollow')
@login_required
def unfollow(username):
    user = get_object_or_404(User.select(), (User.username == username))
    if get_current_user().unfollow(user):
        flash('You unfollow {}'.format(user.username))
    return redirect(url_for('main.user_detail', username=user.username))


@main.route('/user/<username>')
@login_required
def user_detail(username):
    user = get_object_or_404(User.select(), (User.username == username))
    return object_list('user.html', user.posts, check_bounds=False, context_variable='posts_list', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = get_current_user()
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.save()
        flash('Your profile has been update.')
        return redirect(url_for('main.user_detail', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = get_object_or_404(Post.select(), (Post.id == post_id))
    if post.author == get_current_user():
        Post.delete().where(Post.id == post_id).execute()
    return redirect(redirect_url())


@main.app_template_filter('is_following')
def is_following(from_user, to_user):
    return from_user.is_following(to_user)


@main.app_context_processor
def _inject_user():
    return {'current_user': get_current_user()}
