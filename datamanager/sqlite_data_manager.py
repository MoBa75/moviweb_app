from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from data_models import db, User, Movie, UserMovies
from sqlalchemy.exc import SQLAlchemyError

class SQLiteDataManager(DataManagerInterface):
    """
    Handles all database operations using SQLAlchemy.
    """

    def __init__(self, app):
        """
        Initializes the database for the Flask app.
        """
        db.init_app(app)
        self.db = db

    def commit_only(self):
        """
        Commits the current session to the database.
        Rolls back and returns an error message if the commit fails.
        """
        try:
            self.db.session.commit()
            return "", 200
        except SQLAlchemyError as error:
            self.db.session.rollback()
            return {'error': str(error)}, 500

    def add_element(self, element):
        """
        Adds an element to the session and commits it to the database.
        """
        self.db.session.add(element)
        return self.commit_only()[0]

    def get_all_users(self):
        """
        Retrieves the names of all users in the database.
        """
        try:
            return self.db.session.query(User.name).all()
        except SQLAlchemyError as error:
            return {'error': str(error)}

    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a given user ID.
        """
        try:
            user = self.db.session.get(User, user_id)
            if not user:
                return {'error': f"User does not exist."}
            return [entry.movies for entry in user.user_movies]
        except SQLAlchemyError as error:
            return {'error': str(error)}

    def add_user(self, user):
        """
        Adds a new user to the database if the user not already exist.
        """
        existing_user = self.db.session.query(User).filter_by(name=user.name).first()
        if existing_user:
            return {"error": f"User '{user.name}' already exists."}
        return self.add_element(user)

    def delete_user(self, user_id):
        """
        Deletes a user from the database by ID, including associated user-movie links.
        """
        user = self.db.session.get(User, user_id)
        if not user:
            return {'error': 'User not found'}, 404

        self.db.session.delete(user)
        result, status = self.commit_only()
        if status == 200:
            return {'message': 'User deleted'}, 200
        return result, status

    def get_all_movies(self):
        """
        Retrieves all movie entries from the database.
        """
        try:
            return self.db.session.query(Movie).all()
        except SQLAlchemyError as error:
            return {'error': str(error)}

    def add_movie(self, movie):
        """
        Adds a new movie to the database if the title not already exist.
        """
        existing_movie = self.db.session.query(Movie).filter_by(title=movie.title).first()
        if existing_movie:
            return {"error": f"Movie '{movie.title}' already exists."}
        return self.add_element(movie)

    def update_movie(self, movie):
        """
        Commits updates made to an existing movie object.
        """
        message, status = self.commit_only()
        return message, status

    def delete_movie(self, movie_id):
        """
        Deletes a movie entry from the database by movie ID.
        """
        movie = self.db.session.get(Movie, movie_id)
        if not movie:
            return {'error': 'Movie not found'}, 404

        self.db.session.delete(movie)
        result, status = self.commit_only()
        if status == 200:
            return {'message': 'Movie deleted'}, 200
        return result, status
