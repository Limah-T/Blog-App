import os
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import BlogPostForm, CommentForm, ContactForm
from my_flask_app import db, mail
from .auth import login_required
from .models import BlogPost, Comment, User
from datetime import datetime
from flask_login import current_user
from flask_mail import Message
from dotenv import load_dotenv

load_dotenv()

views = Blueprint('views', __name__)


@views.route("/")
@views.route("/home")
def home():
    post_database = db.session.execute(db.select(BlogPost).order_by(BlogPost.date.desc())).scalars().all()
    return render_template('home.html', all_posts=post_database)


@views.route("/about")
def about():
    return render_template('about.html')


@views.route("/contact")
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)


@views.route("/send-message", methods=['GET', 'POST'])
@login_required
def send_message():
    form = ContactForm()
    try:
        msg = Message(
            subject=form.about.data,
            sender=form.email.data,
            recipients=[os.environ.get('RECIPIENT')]
        )
        # msg.body = form.message.data
        msg.html = (f"Message: {form.email.data}: <p>{form.message.data}</p>")
        mail.send(msg)
        flash(message="Message sent!", category='success')
        return redirect(url_for('views.contact'))
    except Exception as e:
        return str(e)


@views.route("/add-new-post", methods=['GET', 'POST'])
@login_required
def add_new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(title=form.title.data, subtitle=form.subtitle.data, img_url=form.img_url.data,
                            content=form.content.data, date=datetime.now().strftime("%B-%d-%Y"),
                            user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash(message="Post created", category="success")
        return redirect(url_for('views.show_post', post_id=new_post.id))
    return render_template("create_post.html", form=form, new_post=True)


@views.route("/show-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    print(post_id)
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    comment = db.session.execute(db.select(Comment).where(Comment.post_id == post_id)).scalars().all()
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(message="You have to login or signup to comment", category="error")
            return render_template("post.html", post=post, form=form, unauthorized_user=True)
        print(f"Form Comment Data: post id: {post.id, post_id}")
        print(f"text: {form.text.data}")
        print(f"User: {current_user.id}")
        new_comment = Comment(text=form.text.data, post_id=post_id, author_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('views.show_post', post_id=post.id))
    return render_template("post.html", post=post, form=form, all_comments=comment)


@views.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    try:
        post = db.get_or_404(BlogPost, post_id)
        if post.id == post.user.id:
            pass
    except:
        flash(message="You are not permitted to edit this post")
        return redirect(url_for('views.home'))
    else:
        form = BlogPostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            content=post.content
        )

        if form.validate_on_submit():
            post.title = form.title.data
            post.subtitle = form.subtitle.data
            post.img_url = form.img_url.data
            post.content = form.content.data
            db.session.commit()
            flash(message="Post edited", category='success')
            return redirect(url_for('views.show_post', post_id=post.id))

    return render_template('create_post.html', form=form, is_edit=True, post_id=post_id)


@views.route("/delete-post/<int:post_id>", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    try:
        post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar_one()
        if post.id == post.user.id:
            pass
    except:
        flash(message="You are not permitted to delete this post")
        return redirect(url_for('views.home'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash(message="Post deleted!", category="success")
        return redirect(url_for('views.home'))


