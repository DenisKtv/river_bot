from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    name = models.CharField('name group', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    news = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='images'
    )
    image_url = models.CharField('image for post', max_length=400)


class Post(models.Model):
    title = models.CharField('news title', max_length=150)
    text = models.TextField('text')
    image = models.CharField('image for title', max_length=400)
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def short_text(self):
        return self.text[:30]

    def get_formatted_text(self):
        formatted_text = self.text
        images = self.images.all()
        image_iter = iter(images)
        while '{img}' in formatted_text:
            try:
                image = next(image_iter)
            except StopIteration:
                break
            formatted_text = formatted_text.replace(
                '{img}', f'<img src="{image.image_url}">', 1
            )
        return formatted_text

    class Meta:
        verbose_name = 'New'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'{self.text} {self.title}'
