from data_models import User, Movie, UserMovies
from typing import List, Tuple, Union
from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self) -> Tuple[Union[List[Tuple[str]], dict], int]:
        """Returns a list of all usernames as tuples or an error dict."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int) -> Tuple[Union[List[Movie], dict], int]:
        """Returns all movies associated with a given user ID."""
        pass

    @abstractmethod
    def add_user(self, user: User) -> Tuple[dict, int]:
        """Adds a new user object to the database."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> Tuple[dict, int]:
        """Deletes a user and all related user-movie associations."""
        pass

    @abstractmethod
    def get_all_movies(self) -> Tuple[Union[List[Movie], dict], int]:
        """Returns a list of all movie entries."""
        pass

    @abstractmethod
    def add_movie(self, movie: Movie, user_id: int) -> Tuple[dict, int]:
        """Adds a movie to the database."""
        pass

    @abstractmethod
    def update_movie(self, movie: Movie, rating: float) -> Tuple[Union[str, dict], int]:
        """Updates the rating of an existing movie in the database."""
        pass

    @abstractmethod
    def delete_movie(self, user_id: int, movie_id: int) -> Tuple[dict, int]:
        """Deletes a movie from the database for a user."""
        pass

    @abstractmethod
    def add_element(self, element: Union[User, Movie, UserMovies]) -> Tuple[dict, int]:
        """Adds a generic element to the session and commits it."""
        pass

    @abstractmethod
    def commit_only(self) -> Tuple[Union[str, dict], int]:
        """Commits the current database session."""
        pass

    @abstractmethod
    def get_movie(self, movie_id: int) -> Tuple[Union[Movie, dict], int]:
        """Gets a movie by movie ID."""
        pass

    @abstractmethod
    def get_user_by_name(self, username: str) -> Tuple[Union[User, dict], int]:
        """Gets a user by name."""
        pass
