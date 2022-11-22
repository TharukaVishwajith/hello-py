from datetime import datetime
from sqlalchemy.orm import validates

from app.sqla import sqla
from dataclasses import dataclass


@dataclass
class Post(sqla.Model):
    __tablename__ = 'post'
    id = sqla.Column(sqla.Integer, primary_key=True)
    # author_id = sqla.Column(
    #     sqla.Integer, sqla.ForeignKey('user.id'), nullable=False)
    # author = sqla.relationship(
    #     'User', backref=sqla.backref('posts', lazy=True))
    created: datetime = sqla.Column(sqla.DateTime, nullable=False,
                                    default=datetime.utcnow)
    title: str = sqla.Column(sqla.Text, nullable=False)
    body: str = sqla.Column(sqla.Text, nullable=False)

    @validates('title')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} is required.')
        return value

    def __repr__(self):
        return self.title
