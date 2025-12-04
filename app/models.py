from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

from app import db

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User {}>'.format(self.username)


class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    due_date: so.Mapped[datetime] = so.mapped_column(index=True
                                                    , default=lambda: datetime.now(timezone.utc))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True
                                                    , default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    completed = db.Column(db.Boolean, default=False)
    author: so.Mapped[User] = so.relationship(back_populates="tasks")
    def __repr__(self):
        return 'Task {}>'.format(self.title)

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))