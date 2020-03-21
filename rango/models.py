from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0, validators=[MinValueValidator(limit_value=0)])
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)


    class Meta:
    	verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    url = models.URLField(max_length=250)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)

        website = models.URLField(blank=True)
        picture = models.ImageField(upload_to='profile_images', blank=True)

        def __str__(self):
            return self.user.username



