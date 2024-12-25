from . import db
from db import db
from flask_login import UserMixin

from flask_login import UserMixin

from sqlalchemy.orm import relationship

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    articles = relationship("articles", back_populates="user")  # Добавляем связь

class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)
    user = relationship("users", back_populates="articles")  # Добавляем связь
    