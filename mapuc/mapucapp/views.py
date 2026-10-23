from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from .forms import MovieForm

def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movie_form.html', {'form': form, 'title': 'Registrar filme'})

def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movie_form.html', {'form': form, 'title': 'Atualizar filme'})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movie_confirm_delete.html', {'movie': movie})
