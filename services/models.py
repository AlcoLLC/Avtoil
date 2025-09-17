from django.db import models



class Service(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='services/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class ServiceContent(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service', null=True, blank=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service_content/')
    description = models.TextField()
    in_home = models.BooleanField(default=False, verbose_name="In Home")

    def __str__(self):
        return f"{self.title}"


class ServiceLastContent(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='service_last/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"