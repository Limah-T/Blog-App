from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text
from my_flask_app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
    posts = relationship('BlogPost', back_populates="user", cascade="all, delete")
    comments = relationship('Comment', back_populates="author", cascade="all, delete")
    likes = relationship('Likes', back_populates="user", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(1000), nullable=False)
    img_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(200), nullable=False)
    user = relationship('User', back_populates="posts")
    comments = relationship('Comment', back_populates="post", cascade="all, delete")
    likes = relationship('Likes', back_populates="post", cascade="all, delete")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author = relationship('User', back_populates="comments")
    post =  relationship('BlogPost', back_populates="comments", cascade="all, delete")
    likes = relationship('Likes', back_populates="comments", cascade="all, delete")


class Likes(db.Model):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    post = relationship('BlogPost', back_populates="likes", cascade="all, delete")
    user = relationship('User', back_populates="likes", cascade="all, delete")
    comments = relationship('Comment', back_populates="likes", cascade="all, delete")