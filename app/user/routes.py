from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from PIL import Image
import secrets

from . import user_bp
from .. import db
from ..models import User, Post, Comment
from ..decorators import admin_required, permission_required
from .forms import (
    EditProfileForm, 
    ChangePasswordForm, 
    DeleteAccountForm,
    NotificationSettingsForm,
    PrivacySettingsForm
)

# Helper function to save profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resize image
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save the image
    i.save(picture_path)
    
    # Delete old profile picture if it's not the default
    if current_user.image_file != 'default.jpg':
        old_picture_path = os.path.join(
            current_app.root_path, 
            'static/profile_pics', 
            current_user.image_file
        )
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)
    
    return picture_fn

@user_bp.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user, is_published=True)\
                     .order_by(Post.date_posted.desc())\
                     .paginate(page=page, per_page=10, error_out=False)
    
    # Update last seen on profile view
    if user == current_user:
        user.ping()
    
    return render_template('user/profile.html', 
                         user=user, 
                         posts=posts,
                         title=f"{user.username}'s Profile")

@user_bp.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    if current_user.username != username and not current_user.is_admin:
        abort(403)
    
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm()
    password_form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        
        user.username = form.username.data
        user.email = form.email.data
        user.about_me = form.about_me.data
        user.location = form.location.data
        user.website = form.website.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.about_me.data = user.about_me
        form.location.data = user.location
        form.website.data = user.website
    
    return render_template('user/edit_profile.html', 
                         title='Edit Profile',
                         form=form,
                         password_form=password_form,
                         user=user)

@user_bp.route('/user/<username>/change_password', methods=['POST'])
@login_required
def change_password(username):
    if current_user.username != username and not current_user.is_admin:
        abort(403)
    
    user = User.query.filter_by(username=username).first_or_404()
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
        else:
            flash('Current password is incorrect.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    
    return redirect(url_for('user.edit_profile', username=user.username))

@user_bp.route('/user/<username>/delete', methods=['POST'])
@login_required
def delete_account(username):
    if current_user.username != username and not current_user.is_admin:
        abort(403)
    
    user = User.query.filter_by(username=username).first_or_404()
    
    # Log out the user before deleting the account
    logout_user()
    
    # Delete user's posts, comments, etc.
    # (Handled by CASCADE in the database, but we can add additional cleanup here if needed)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('main.home'))

@user_bp.route('/user/<username>/posts')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user, is_published=True)\
                     .order_by(Post.date_posted.desc())\
                     .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('user/user_posts.html', 
                         user=user, 
                         posts=posts,
                         title=f"{user.username}'s Posts")

@user_bp.route('/user/<username>/comments')
def user_comments(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(author=user, is_approved=True)\
                          .order_by(Comment.date_posted.desc())\
                          .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('user/user_comments.html', 
                         user=user, 
                         comments=comments,
                         title=f"{user.username}'s Comments")

@user_bp.route('/settings/notifications', methods=['GET', 'POST'])
@login_required
def notification_settings():
    form = NotificationSettingsForm()
    
    if form.validate_on_submit():
        # Update user notification preferences
        current_user.email_notifications = form.email_notifications.data
        current_user.comment_notifications = form.comment_notifications.data
        current_user.reply_notifications = form.reply_notifications.data
        current_user.newsletter = form.newsletter.data
        
        db.session.commit()
        flash('Your notification settings have been updated!', 'success')
        return redirect(url_for('user.notification_settings'))
    elif request.method == 'GET':
        form.email_notifications.data = current_user.email_notifications
        form.comment_notifications.data = current_user.comment_notifications
        form.reply_notifications.data = current_user.reply_notifications
        form.newsletter.data = current_user.newsletter
    
    return render_template('user/notification_settings.html', 
                         title='Notification Settings',
                         form=form)

@user_bp.route('/settings/privacy', methods=['GET', 'POST'])
@login_required
def privacy_settings():
    form = PrivacySettingsForm()
    
    if form.validate_on_submit():
        # Update user privacy preferences
        current_user.show_email = form.show_email.data
        current_user.show_last_seen = form.show_last_seen.data
        current_user.allow_search_engines = form.allow_search_engines.data
        
        db.session.commit()
        flash('Your privacy settings have been updated!', 'success')
        return redirect(url_for('user.privacy_settings'))
    elif request.method == 'GET':
        form.show_email.data = current_user.show_email
        form.show_last_seen.data = current_user.show_last_seen
        form.allow_search_engines.data = current_user.allow_search_engines
    
    return render_template('user/privacy_settings.html', 
                         title='Privacy Settings',
                         form=form)
