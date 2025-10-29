from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', 
                         validators=[DataRequired(), 
                                   Length(min=3, max=20, message='Username must be between 3 and 20 characters')])
    email = StringField('Email', 
                       validators=[DataRequired(), 
                                 Email(message='Please enter a valid email address')])
    about_me = TextAreaField('About Me', 
                            validators=[Length(max=500, message='About me cannot exceed 500 characters')],
                            render_kw={"rows": 4, "placeholder": "Tell us about yourself..."})
    location = StringField('Location', 
                          validators=[Length(max=100, message='Location cannot exceed 100 characters')],
                          render_kw={"placeholder": "City, Country"})
    website = StringField('Website', 
                         validators=[Optional(), 
                                   Length(max=200, message='Website URL is too long')],
                         render_kw={"placeholder": "https://yourwebsite.com"})
    picture = FileField('Profile Picture', 
                       validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only (jpg, jpeg, png)')])
    submit = SubmitField('Update Profile')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', 
                                   validators=[DataRequired(message='Current password is required')],
                                   render_kw={"placeholder": "Enter current password"})
    new_password = PasswordField('New Password', 
                               validators=[DataRequired(message='New password is required'),
                                         Length(min=8, message='Password must be at least 8 characters long')],
                               render_kw={"placeholder": "Enter new password"})
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[DataRequired('Please confirm your new password'),
                                             EqualTo('new_password', message='Passwords must match')],
                                   render_kw={"placeholder": "Confirm new password"})
    submit = SubmitField('Change Password')


class DeleteAccountForm(FlaskForm):
    confirm_username = StringField('Confirm Username', 
                                 validators=[DataRequired('Please enter your username to confirm')],
                                 render_kw={"placeholder": "Type your username to confirm"})
    confirm = BooleanField('I understand that this action cannot be undone', 
                          validators=[DataRequired('You must confirm this action')])
    submit = SubmitField('Delete My Account', 
                        render_kw={"class": "btn btn-danger"})


class NotificationSettingsForm(FlaskForm):
    email_notifications = BooleanField('Email Notifications', 
                                     default=True,
                                     description='Receive email notifications for comments and updates')
    comment_notifications = BooleanField('New Comments', 
                                       default=True,
                                       description='Notify me when someone comments on my posts')
    reply_notifications = BooleanField('Comment Replies', 
                                     default=True,
                                     description='Notify me when someone replies to my comments')
    newsletter = BooleanField('Newsletter', 
                            default=True,
                            description='Subscribe to our newsletter for updates and news')
    submit = SubmitField('Save Notification Settings')


class PrivacySettingsForm(FlaskForm):
    show_email = BooleanField('Show Email Address', 
                            default=False,
                            description='Make your email address visible to other users')
    show_last_seen = BooleanField('Show Last Seen', 
                                default=True,
                                description='Show when you were last active on the site')
    allow_search_engines = BooleanField('Allow Search Engines', 
                                      default=True,
                                      description='Allow search engines to index my profile')
    submit = SubmitField('Save Privacy Settings')
