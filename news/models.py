from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True) 
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class News_Content(models.Model):
    news = models.ForeignKey(
        News, related_name='contents', on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True, null=True) 
    image = models.ImageField(upload_to='news/', blank=True, null=True)


    def __str__(self):
        return f"{self.news.title} Content"
