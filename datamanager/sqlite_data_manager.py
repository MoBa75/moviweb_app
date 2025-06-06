from datamanager.data_manager_interface import DataManagerInterface
from data_models import db, User, Movie, UserMovies
from sqlalchemy.exc import SQLAlchemyError

class SQLiteDataManager(DataManagerInterface):
    """Handles all database operations using SQLAlchemy."""

    def __init__(self, app):
        """Initializes the database for the Flask app."""
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
        """Adds an element to the session and commits it to the database."""
        try:
            self.db.session.add(element)
            return self.commit_only()
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def get_all_users(self):
        """Retrieves the names of all users in the database."""
        try:
            return self.db.session.query(User.name).all(), 200
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def get_user_movies(self, user_id):
        """Retrieves all movies associated with a given user ID."""
        try:
            user = self.db.session.get(User, user_id)
            if not user:
                return {'error': "User does not exist."}, 404
            return [entry.movies for entry in user.user_movies], 200
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def add_user(self, user):
        """Adds a new user to the database if the user not already exist."""
        try:
            existing_user = self.db.session.query(User).filter_by(name=user.name).first()
            if existing_user:
                return {"error": f"User '{user.name}' already exists."}, 409
            return self.add_element(user)
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def delete_user(self, user_id):
        """
        Deletes a user from the database by ID, including associated
        user-movie links. Deletes movies without remaining links.
        """
        try:
            user = self.db.session.get(User, user_id)
            if not user:
                return {'error': 'User not found'}, 404
            connection = self.db.session.query(UserMovies).filter_by(user_id=user_id).all()
            if connection:
                connected_movies = [movie_connection.movie_id for movie_connection in connection]
                self.db.session.delete(connection)
                for movie_id in connected_movies:
                    if not self.db.session.query(UserMovies).filter_by(movie_id=movie_id).first():
                        self.db.session.get(Movie, movie_id).delete()
            self.db.session.delete(user)
            result, status = self.commit_only()
            if status == 200:
                return {'message': 'User deleted'}, 200
            return result, status
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def get_all_movies(self):
        """Retrieves all movie entries from the database."""
        try:
            return self.db.session.query(Movie).all(), 200
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def add_movie(self, movie, user_id):
        """Adds a new movie to the database if the title not already exist."""
        try:
            existing_movie = self.db.session.query(Movie).filter_by(title=movie.title).first()
            if not existing_movie:
                self.add_element(movie)
                existing_movie = movie
            else:
                connection = (self.db.session.query(UserMovies)
                              .filter_by(user_id=user_id, movie_id=existing_movie.id).first())
                if connection:
                    return {"error": f"Movie '{movie.title}' already exists."}, 409
            new_connection = UserMovies(user_id=user_id, movie_id=existing_movie.id)
            return self.add_element(new_connection)
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def update_movie(self, movie, rating):
        """Updates rating of a movie."""
        if not isinstance(movie, Movie):
            return {'error': 'Movie has to be a Movie class instance.'}, 400
        if not isinstance(rating, float):
            return {'error': 'Rating has to be a float.'}, 400

        movie.rating = rating
        message, status = self.commit_only()
        return message, status

    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie connection by user and movie id from the
        database, deletes the movie if no connection is left.
        """
        movie, result = self.get_movie(movie_id)
        if result != 200:
            return {'error': 'Movie not found'}, 404

        try:
            connection = (self.db.session.query(UserMovies).filter_by(user_id=user_id,
                                                                      movie_id=movie_id).first())
            self.db.session.delete(connection)
            further_connection = (self.db.session.query(UserMovies)
                                  .filter_by(movie_id=movie_id).first())
            if not further_connection:
                self.db.session.delete(movie)
            result, status = self.commit_only()
            if status == 200:
                return {'message': 'Movie deleted'}, 200
            return result, status
        except SQLAlchemyError as error:
            self.db.session.rollback()
            return {'error': str(error)}, 500

    def get_movie(self, movie_id):
        """Gets a movie by movie id."""
        try:
            existing_movie = self.db.session.get(Movie, movie_id)
            if not existing_movie:
                return {'error': 'Movie not found'}, 404
            return existing_movie, 200
        except SQLAlchemyError as error:
            return {'error': str(error)}, 500

    def get_user_by_name(self, username):
        """Gets a user by name."""
        try:
            existing_user = self.db.session.query(User).filter_by(name=username).first()
            if not existing_user:
                return {'error': 'User not found'}, 404
            return existing_user, 200
        except SQLAlchemyError as error:
            self.db.session.rollback()
            return {'error': str(error)}, 500
