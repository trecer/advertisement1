from django.db import models
from django.urls import reverse
from PIL import Image


# Вторичная модель
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент') # blank поле не обязательно к заполнению. будет записана пустая строка
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликованно')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновленно')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)  # upload_to куда будет сохроняться картинка
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Наименование категории', related_name='get_news') # models.PROTECT  - это callable функция. Она сама вызывается поэтому после PROTECT скобки не нужны
    #null=True - ставит значение null при отсутствии значения в поле
    views = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk})

    def __str__(self):
        return self.title




    class Meta: # класс внутри класса News
        verbose_name = 'Новость' # Наименование модели в единственном числе
        verbose_name_plural = 'Новости' # Название во множественном числе
        ordering = ['-created_at'] # Сортировка в админке и в пользовательской части

# Первичная модель
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Наименование")

    def get_absolute_url(self): # данный метод выстраивает ссылку автоматичкски
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:  # класс внутри класса News
        verbose_name = 'Категория'  # Наименование модели в единственном числе
        verbose_name_plural = 'Категории'  # Название во множественном числе
        ordering = ['title']  # Сортировка в админке и в пользовательской части

