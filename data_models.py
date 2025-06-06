from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Represents an user.

    Attributes:
        id (integer): primary key, auto-incrementing unique identifier
        name (string): name of the user (must be unique)
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    user_movies = db.relationship('UserMovies', back_populates='user', cascade='all, delete')

    def __repr__(self):
        """Returns a concise, unambiguous representation
        of the User instance for debugging"""
        return f"<User(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """Returns a human-readable string representation of the User instance."""
        return f"{self.name}"

class Movie(db.Model):
    """
    Represents a movie.
    Attributes:
        id (integer): primary key, auto-incrementing unique identifier
        title (string): movie name
        director (sting): director from the movie
        year (integer): year of the book's first publication year
        rating (integer): rating of the movie
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    poster = db.Column(db.String(300))

    user_movies = db.relationship('UserMovies', back_populates='movies',
                                  cascade='all, delete')

    def __repr__(self):
        """Returns a concise, unambiguous representation
        of the Movie instance for debugging"""
        return (f"<Movie(id={self.id}, title='{self.title}', director={self.director}, "
                f"year={self.year}, rating={self.rating})>")

    def __str__(self):
        """Returns a human-readable string representation of the Movie instance."""
        return f"{self.title} ({self.year}) by {self.director}"

class UserMovies(db.Model):
    """
    This table is the link of the user from the user table
    and the movies from the movie table.
    Attributes:
        id (integer): primary key, auto-incrementing unique identifier
        user_id (integer): user id key, foreign key
        movie_id (integer): movie id key, foreign key
    """
    __tablename__ = 'user_movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    user = db.relationship('User', back_populates='user_movies')
    movies = db.relationship('Movie', back_populates='user_movies')

    def __repr__(self):
        """Returns a concise, unambiguous representation
        of the UserMovie instance for debugging"""
        return (f"<user_movie_id(id={self.id}, user_id='{self.user_i}', "
                f"movie_id={self.movie_id}, user_rating={self.user_rating})>")
