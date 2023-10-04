from datetime import datetime
from hashlib import md5

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db =SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=True,
        unique=True
    )
    email = db.Column(
        db.String(120),
        index=True,
        unique=True
    )
    password_hash = db.Column(
        db.String(128)
    )
    about_me = db.Column(
        db.String(140)
    )
    last_seen = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    posts = db.relationship(
        'Post',
        backref='author',
        lazy='dynamic'
    )

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'User:\t{self.username}\n'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0
    
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    body = db.Column(
        db.String(140)
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    def __repr__(self):
        return f'Post: \n\t{self.body}\n'
        

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))