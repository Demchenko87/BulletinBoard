from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestramp_path

class AdvUser(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Аватар', null=True, blank=True,)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел Активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Снять оповещение о новых комментариях?')

    def delete(self, *args, **kvargs):
        for bb in self.bb_set.all():
            bb.delete()
        super.delete(*args, **kvargs)
    class Meta(AbstractUser.Meta):
        pass

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')

class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'





class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.CharField(verbose_name='Телефон', max_length=40)
    city = models.CharField(verbose_name='Город', max_length=40, blank=True, null=True)
    street = models.CharField(verbose_name='Улица или проспект', max_length=150, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to=get_timestramp_path, verbose_name='Изображения')

    delivery1 = models.BooleanField(default=False, verbose_name='Новая почта')
    comment1 = models.CharField(max_length=40, verbose_name='Комментарий', blank=True, null=True)
    delivery2 = models.BooleanField(default=False, verbose_name='Укр почта')
    comment2 = models.CharField(max_length=40, verbose_name='Комментарий', blank=True, null=True)
    delivery3 = models.BooleanField(default=False, verbose_name='Доставка Justin')
    comment3 = models.CharField(max_length=40, verbose_name='Комментарий', blank=True, null=True)

    money = models.BooleanField(default=False, verbose_name='Наличный')
    сashless = models.BooleanField(default=False, verbose_name='Безналичный')
    invoce = models.BooleanField(default=False, verbose_name='Оплата по счету')
    visa = models.BooleanField(default=False, verbose_name='Visa')
    mastercard = models.BooleanField(default=False, verbose_name='Mastercard')



    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявлений')

    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Публиковать')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опублековано')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']

class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestramp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные илюстрации'
        verbose_name = 'Дополнительная илюстрация'

class Stars(models.Model):
    star = models.CharField(max_length=1, verbose_name='Звезда', blank=True, null=True)
    def __str__(self):
        return self.star
    class Meta:
        verbose_name_plural = 'Звезды рейтинга'
        verbose_name = 'Звезда'

class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опублекован')

    star = models.CharField(max_length=30, verbose_name="звезда", blank=True, null=True)
    user = models.CharField(max_length=200, verbose_name="Пользователь", blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']



class Rating(models.Model):
    login = models.CharField("Логин гостя", max_length=150, blank=True, null=True)
    star = models.ForeignKey(Stars, on_delete=models.CASCADE, verbose_name="звезда")
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f"{self.star} - {self.user}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


