from flask import Flask, request, render_template, redirect, url_for
from data_models import db, User, Movie, UserMovies
from db_validation import validate_database
import os
from datamanager.sqlite_data_manager import SQLiteDataManager
from movie_data_api import get_movie_data

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'movies.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)

validate_database(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    users = data_manager.get_all_users()
    if isinstance(users, dict) and 'error' in users:
        return render_template('error.html', error=users['error'])

    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user = User.query.filter_by(name=username).first()
            if user:
                return redirect(url_for('user_movies', user_id=user.id))
            else:
                return render_template('home.html', users=users,
                                       error="User not found.")
    return render_template('home.html', users=users)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    if isinstance(movies, dict) and 'error' in movies:
        return render_template('error.html', error=movies['error']), 404
    return render_template('user_movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('name')
        if username:
            new_user = User(name=username)
            error = data_manager.add_user(new_user)
            if not error:
                return redirect(url_for('home'))
        return render_template('add_user.html',
                               error=error if error else "Username is required")
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return render_template('error.html', error="Movie not found"), 404

    if request.method == 'POST':
        raw_rating = request.form.get('rating', str(movie.rating))
        rating_str = raw_rating.replace(',', '.')

        try:
            movie.rating = float(rating_str)
            if movie.rating < 0.0 or movie.rating > 10.0:
                raise ValueError("Rating must be between 0 and 10")
        except (ValueError, TypeError):
            return render_template('edit_movie.html', movie=movie,
                                   error="Please enter a valid rating between 0 and 10.")

        error, result = data_manager.update_movie(movie)
        if not error:
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('edit_movie.html', movie=movie, error=error)

    return render_template('edit_movie.html', movie=movie)


@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    director = request.form.get('director')
    year = request.form.get('year')
    rating = request.form.get('rating')
    poster = request.form.get('poster')

    if all([title, director, year]):
        try:
            year = int(year)

            if rating is None or rating.strip().lower() == "n/a":
                rating = None
            else:
                rating = float(rating.replace(",", "."))
        except (ValueError, TypeError):
            return render_template('error.html',
                                   error="Invalid rating or year format.")

        new_movie = Movie(title=title, director=director, year=year, rating=rating, poster=poster)
        error = data_manager.add_movie(new_movie)
        if not error:
            user_movie = UserMovies(user_id=user_id, movie_id=new_movie.id)
            error = data_manager.add_element(user_movie)
            if not error:
                return redirect(url_for('user_movies', user_id=user_id))
        return render_template('error.html', error=error)
    return render_template('error.html', error="Missing movie data")



@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    result, status = data_manager.delete_movie(movie_id)
    if not status == 200:
        return render_template('error.html', error=result.get('error')), status
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    result, status = data_manager.delete_user(user_id)
    if not status == 200:
        return render_template('error.html', error=result.get('error')), status
    return redirect(url_for('home'))


@app.route('/fetch_movie', methods=['GET', 'POST'])
def fetch_movie():
    user_id = request.args.get('user_id', type=int)  # für GET

    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int) or user_id
        movie_title = request.form.get('title')
        if movie_title:
            movie_data = get_movie_data(movie_title)
            if 'error' in movie_data:
                return render_template('fetch_movie.html',
                                       error=movie_data['error'], user_id=user_id)
            return render_template('fetch_movie.html',
                                   movie=movie_data, user_id=user_id)

    return render_template('fetch_movie.html', user_id=user_id)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html',
                           error="Seite nicht gefunden (404)"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                           error="Interner Serverfehler (500)"), 500


@app.route('/test-error')
def test_error():
    return render_template('error.html',
                           error="Dies ist ein gezielt ausgelöster Testfehler."), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)