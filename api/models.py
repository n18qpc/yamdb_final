from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import generate_confirmation_code


class CustomUser(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты')
    role = models.CharField(max_length=20, choices=UserRole.choices,
                            default='user')
    confirmation_code = models.CharField(max_length=100, null=True,
                                         verbose_name='Код подтверждения',
                                         default=generate_confirmation_code())
    username = models.CharField(
        null=False, unique=True, max_length=100, verbose_name='Username'
    )
    bio = models.TextField(
        max_length=300, null=True, blank=True, verbose_name='О себе'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.IntegerField("Год")
    description = models.TextField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles", null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="reviews")
    text = models.TextField(max_length=300)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    score = models.PositiveSmallIntegerField(
        "Рейтинг", default=None, validators=[MaxValueValidator(10),
                                             MinValueValidator(0)])
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_review_per_author'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField(max_length=300)
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return self.text
