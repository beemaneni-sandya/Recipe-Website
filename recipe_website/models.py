from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    recipes = db.relationship('Recipe', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Recipe id={self.id}, title='{self.title[:20]}...'>"