from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name!")
        
        existing = Author.query.filter_by(name=name).first()
        if existing and existing.id != self.id:  # avoid blocking updates to same record
            raise ValueError("Author name must be unique!")
        
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number should be exactly 10 digits!")
        
        return phone_number

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

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if not len(content) >= 250:
            raise ValueError("Post content length should be more or equal to 250 characters!")
        
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if not len(summary) <= 250:
            raise ValueError("Summary too long test. More than 250 chars.")
        
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'!")
        
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbaity_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title or not any(keyword in title for keyword in clickbaity_keywords):
            raise ValueError("Must have a title that is clickbaity!")
        
        return title



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
