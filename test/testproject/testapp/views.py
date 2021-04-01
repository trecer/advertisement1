from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # чтобы после регистрации не нужно юыло авторизоваться
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'testapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'testapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(ListView):
    model = News # модель из которой получать будем данные
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

class NewsByCategory(ListView):
    model = News
    # используем тотже шаблон
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self): # Корретрует отправляемый запрос в шаблон
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        context: object = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

class ViewNews(DetailView):
    model = News
    pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = NewsForm
    template_name = 'testapp/add_news.html'
    # success_url = reverse_lazy('home')

