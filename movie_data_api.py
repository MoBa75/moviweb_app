import os
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()

API_KEY = os.getenv('API_KEY')

def get_movie_data(movie):
    """
    Retrieves selected movie data from the OMDb API by movie title.
    :param movie: Title of the movie to search for as String.
    :return: Filtered movie data as dictionary.
    """
    if not API_KEY:
        return {'error': 'API_KEY not found. Did you load the .env file and set it correctly?'}

    try:
        api_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie}"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get('Response') == 'False':
            return {'error': data.get('Error', 'Movie not found')}

        return {
            'Title': data.get('Title'),
            'Director': data.get('Director'),
            'Year': data.get('Year'),
            'imdbRating': data.get('imdbRating'),
            'Poster': data.get('Poster')
        }
    except ValueError:
        return {'error': 'Response is not valid JSON'}
    except RequestException as error:
        return {'error': f'Network error: {str(error)}'}


result = get_movie_data('Predator')
print(result)