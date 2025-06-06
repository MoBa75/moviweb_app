from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """Returns a list of all user names."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Returns all movies associated with a given user."""
        pass

    @abstractmethod
    def add_user(self, user):
        """Adds a new user object to the database."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Deletes a user and all related user-movie associations."""
        pass

    @abstractmethod
    def get_all_movies(self):
        """Returns a list of all movie entries."""
        pass

    @abstractmethod
    def add_movie(self, movie, user_id):
        """Adds a movie to the database."""
        pass

    @abstractmethod
    def update_movie(self, movie, rating):
        """Updates an existing movie in the database."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Deletes a movie from the database."""
        pass

    @abstractmethod
    def add_element(self, element):
        """Adds a generic element to the session and commits it."""
        pass

    @abstractmethod
    def commit_only(self):
        """Commits the current database session."""
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        """Gets a movie by movie id."""
        pass

    @abstractmethod
    def get_user_by_name(self, username):
        """Gets a user by name."""
        pass
