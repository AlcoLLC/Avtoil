from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
    
class News_Content(models.Model):
    news = models.ForeignKey(
        News, related_name='contents', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)


    def __str__(self):
        return f"{self.news.title} Content"
