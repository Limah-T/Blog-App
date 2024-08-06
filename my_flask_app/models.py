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
    # profile_pic: Mapped[str] = mapped_column(String(200))
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=True)
    posts: Mapped[list['BlogPost']] = relationship('BlogPost', back_populates="user")
    comment: Mapped[list['Comment']] = relationship('Comment', back_populates="comment_author")
    like: Mapped[list['Likes']] = relationship('Likes', back_populates="user_like")


class BlogPost(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    subtitle: Mapped[str] = mapped_column(String(1000), nullable=False)
    img_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(200), nullable=False)
    user: Mapped[list['User']] = relationship('User', back_populates="posts")
    comment: Mapped[list['Comment']] = relationship('Comment', back_populates="comment_post")
    like: Mapped[list['Likes']] = relationship('Likes', back_populates="post_like")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    comment_author: Mapped[list['User']] = relationship('User', back_populates="comment")
    comment_post: Mapped[list['BlogPost']] = relationship('BlogPost', back_populates="comment")


class Likes(db.Model):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_like: Mapped[list['BlogPost']] = relationship('BlogPost', back_populates="like")
    user_like: Mapped[list['User']] = relationship('User', back_populates="like")
