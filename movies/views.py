from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.views.generic import ListView, DetailView

from .models import Movie
from .forms import ReviewForm

class MoviesView(ListView):
    """ Films list """
    model = Movie
    queryset = Movie.objects.filter(draft=False)

class MovieDetailView(DetailView):
    """ Description of the film """
    model = Movie
    slug_field = "url"


class AddReview(View):
    """ Review """
    def post(selfself,request,pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())