from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service/')
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Service_Content(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_content/')
    in_home = models.BooleanField(default=False, verbose_name="In Home")

    def __str__(self):
        return f"{self.title}"


class ServiceHighlight(models.Model):
    title1 = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='service_highlight/')

    title2 = models.CharField(max_length=255, null=True, blank=True)
    image2 = models.ImageField(upload_to='service_highlight/', null=True, blank=True)

    title3 = models.CharField(max_length=255, null=True, blank=True)
    image3 = models.ImageField(upload_to='service_highlight/', null=True, blank=True)

    def __str__(self):
        return f"{self.title1} / {self.title2 or ''} / {self.title3 or ''}"
