from flask_sqlalchemy import SQLAlchemy
from data_manager_interface import DataManagerInterface
from data_models import db, User, Movie, UserMovies
from sqlalchemy.exc import SQLAlchemyError

class SQLiteDataManager(DataManagerInterface):

    def __init__(self, app):
        db.init_app(app)
        self.db = db

    def add_element(self, element):
        """
        Adds and commits a file to the database, handles
        errors and rollbacks session in case of error.
        :param element: the element to save in the database,
                        Book or Author class instance
        :return: empty string if successful, else an error message
        """
        try:
            self.db.session.add(element)
            self.db.session.commit()
            return ""
        except SQLAlchemyError as error:
            self.db.session.rollback()
            return f"Database error: {str(error)}"
        except Exception as error:
            self.db.session.rollback()
            return f"An unexpected error occurred: {str(error)}"

    def get_all_users(self):
        pass

    def get_user_movies(self, user_id):
        pass

    def add_user(self, user):
        pass

    def add_movie(self, movie):
        pass

    def update_movie(self, movie):
        pass

    def delete_movie(self, movie_id):
        pass

