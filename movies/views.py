from django.shortcuts import render, get_object_or_404, redirect
from . models import Genre, Movie, Review
from django.contrib.auth.decorators import login_required
from . forms import ReviewForm
from IPython import embed

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
    form = ReviewForm()
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'movies/detail.html', context)

@login_required
def new(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()
    return redirect('movies:detail', movie.pk)
        
@login_required
def delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review.delete()
    return redirect('movies:detail', movie_pk)

@login_required
def like(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.user in movie.like_users.all():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return redirect('movies:detail', movie_pk)
