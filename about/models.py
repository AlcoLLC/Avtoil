from django.db import models

class AboutAvtoil(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about_avtoil/')
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class AboutContent(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about_content/')
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

class DocumentsCertification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Sustainability(models.Model):
     title = models.CharField(max_length=255)
     description = models.TextField()
     image = models.ImageField(
        upload_to='sustainability/', blank=True, null=True)
     def __str__(self):
        return f"{self.title}"