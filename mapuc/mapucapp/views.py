from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import MovieForm
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})

@login_required(login_url='/login/')
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})

@login_required(login_url='/login/')
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movie_form.html', {'form': form, 'title': 'Registrar filme'})

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movie_confirm_delete.html', {'movie': movie})

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {
                    "action": "Adicionar",
                    "error": "Esse nome de usuário já está em uso. Escolha outro.",
                    "username": username,
                    "email": email,
                },
            )

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('movie_list')
    return render(request,"register.html",context={"action":"Adicionar"})

def login_user(request):
    next_url = request.POST.get('next') or request.GET.get('next', '')
    context = {'next': next_url}
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')

        
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)

        if user is not None:
            login(request, user)
            if url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('movie_list')
        else:
            context['error_message'] = 'Usuário não existe ou senha incorreta.'

    return render(request, 'registration/login.html', context)

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('login')