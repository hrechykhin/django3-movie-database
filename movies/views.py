from django.shortcuts import render
from django.views.generic.base import View

from django.views.generic import ListView, DetailView

from .models import Movie

class MoviesView(ListView):
    """ Films list """
    model = Movie
    queryset = Movie.objects.filter(draft=False)

class MovieDetailView(DetailView):
    """ Description of the film """
    model = Movie
    slug_field = "url"