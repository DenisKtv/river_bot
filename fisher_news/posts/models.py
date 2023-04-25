from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    name = models.CharField('name group', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField('news title', max_length=150)
    text = models.TextField('text')
    image = models.ImageField('image of news', upload_to='posts/images')
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'New'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.text} {self.title}'
