from django.shortcuts import render, get_object_or_404
from . models import Genre, Movie, Review

# Create your views here.

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = Review.objects.filter(movie_id=movie_pk)
    context = {
        'movie': movie,
        'reviews': reviews
    }
    return render(request, 'movies/detail.html', context)
