from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Categories """
    name = models.CharField(verbose_name='Category', max_length=150)
    description = models.TextField(verbose_name='Description', null=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """ Actors and directors """
    name = models.CharField(verbose_name='Name', max_length=100)
    age = models.PositiveSmallIntegerField(verbose_name='Age', default=0)
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(verbose_name='Image', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actors and directors'
        verbose_name_plural = 'Actors and directors'

class Genre(models.Model):
    """ Genres """
    name = models.CharField(verbose_name='Genre', max_length=100)
    description = models.TextField(verbose_name='Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

class Movie(models.Model):
    """ Films """
    title = models.CharField(verbose_name='Title', max_length=100)
    tagline = models.CharField(verbose_name='Slogan', max_length=100, default='')
    description = models.TextField(verbose_name='Description')
    poster = models.ImageField(verbose_name='Poster', upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name='Release date', default=2020)
    country = models.CharField(verbose_name='Country', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Directors', related_name='Film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Actors', related_name='Film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Genres')
    world_premiere = models.DateField(verbose_name='World release', null=True, blank=True)
    budget = models.PositiveIntegerField(verbose_name='Budget', default=0, help_text="Please mention in $")
    fees_in_usa = models.PositiveIntegerField(
        verbose_name='US Box office', default=0, help_text="Please mention in $"
    )
    fees_in_world = models.PositiveIntegerField(
        verbose_name='World Box office', default=0, help_text="Please mention in $"
    )
    category = models.ForeignKey(
        Category, verbose_name='Category', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(verbose_name='Draft', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull = True)

    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Films'


class MovieShots(models.Model):
    """ Movie shots """
    title = models.CharField(verbose_name='Title', max_length=100)
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(verbose_name='Image', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie shot'
        verbose_name_plural = 'Movie shots'

class RatingStar(models.Model):
    """ Rating stars """
    value = models.PositiveSmallIntegerField(verbose_name='Value', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'

class Rating(models.Model):
    """ Ratings """
    ip = models.CharField(verbose_name='IP address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Star')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Film')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

class Reviews(models.Model):
    """ Reviews """
    email = models.EmailField()
    name = models.CharField(verbose_name='Name', max_length=100)
    text =  models.TextField(verbose_name='Message', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Parent', on_delete=models.SET_NULL, blank = True, null = True
    )
    movie = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'