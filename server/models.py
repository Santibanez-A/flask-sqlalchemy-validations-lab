from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not phone_number or not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")

        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits.")

        return phone_number

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Author must have a name.")

        existing_author = Author.query.filter(
            Author.name == name.strip()
        ).first()

        if existing_author and existing_author.id != self.id:
            raise ValueError("Author names must be unique.")

        return name.strip()

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("content")
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError(
                "Post content must be at least 250 characters."
            )
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be 250 characters or fewer.")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category

    @validates("title")
    def validate_title(self, key, title):
        phrases = [
            "Won't Believe",
            "Secret",
            "Top",
            "Guess"
        ]

        if not any(phrase in title for phrase in phrases):
            raise ValueError(
                "Title must contain 'Won't Believe', 'Secret', 'Top', or 'Guess'."
            )

        return title

    def __repr__(self):
        return (
            f'Post(id={self.id}, title={self.title}, '
            f'content={self.content}, summary={self.summary})'
        )