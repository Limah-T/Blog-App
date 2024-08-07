from wtforms import ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from wtforms import PasswordField, StringField, TextAreaField, EmailField, SubmitField
import re


def validate_username(form, field):
    pattern = "^[a-zA-z0-9_]*$"
    if not re.match(pattern, field.data):
        raise ValidationError("Username can only contain letters, numbers, and underscores.")


class SignupForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), validate_username])
    email = EmailField(label="Email", validators=[DataRequired(), Email(message="Invalid Email", check_deliverability=True)])
    password = PasswordField(label="Password", validators=[DataRequired(),
                                                           Length(min=6, message="Password must be more than 6 characters")])
    confirm_password = PasswordField(label="Confirm Password", validators=[InputRequired(),EqualTo(fieldname='password',
                                                                message="Password do not match, try again")])
    signup = SubmitField(label="Sign me up!")


class LoginForm(FlaskForm):
    email = StringField(label="Email or Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    login = SubmitField(label="Log me In!")


class BlogPostForm(FlaskForm):
    title = StringField(label="Blog Title", validators=[DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    img_url = TextAreaField(label="Image_URL", validators=[DataRequired()],
                          render_kw={'placeholder': 'Background image: You can use any of the default urls listed above (copy and paste here) or '
                                                    'copy image url of your choice in any website','rows': '2', 'cols': '30'})
    content = TextAreaField(label="Content", render_kw={'rows': 6, 'cols': 50},validators=[DataRequired()])
    submit = SubmitField(label="Post Blog")


class CommentForm(FlaskForm):
    text = TextAreaField(label="Comment", render_kw={'rows': 3, 'cols': 30}, validators=[DataRequired()])
    submit = SubmitField(label="Post Comment")


class ContactForm(FlaskForm):
    about = StringField(label="Title of the message", validators=[DataRequired()])
    email = EmailField(label="Email Address", validators=[DataRequired()])
    message = TextAreaField(label="Enter your message", render_kw={'rows': 6, 'cols': 50}, validators=[DataRequired()])
    send = SubmitField(label="Send")