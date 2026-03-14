"""
Movie Recommendation System — Flask Web App
Run:  python app.py
Then open:  http://localhost:5000
"""

from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# ── Load pre-trained model ──────────────────────────────────────────────────
movies     = pickle.load(open('model.pkl',      'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = sorted(movies['title'].tolist())   # for the dropdown

# ── Recommendation logic ─────────────────────────────────────────────────────
def recommend(movie_title, n=10):
    """Return top-n similar movies for the given title."""
    matches = movies[movies['title'] == movie_title]
    if matches.empty:
        return []

    idx     = matches.index[0]
    scores  = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    return [movies.iloc[i[0]].title for i in scores[1:n+1]]


# ── Routes ───────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', movie_list=movie_list)


@app.route('/recommend', methods=['GET', 'POST'])
def get_recommendations():
    selected_movie  = None
    recommendations = []
    error           = None

    if request.method == 'POST':
        selected_movie = request.form.get('movie_title', '').strip()

        if not selected_movie:
            error = 'Please select or type a movie title.'
        else:
            recommendations = recommend(selected_movie)
            if not recommendations:
                error = f'Movie "{selected_movie}" not found. Please try another title.'

    return render_template(
        'index.html',
        movie_list      = movie_list,
        selected_movie  = selected_movie,
        recommendations = recommendations,
        error           = error
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
