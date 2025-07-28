from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Partnership(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_image = models.ImageField(
        upload_to='partnership/main/',
        help_text=_("Main image (recommended size: 800x400px)")

    )
    secondary_image = models.ImageField(
        upload_to='partnership/secondary/',
        blank=True,
        null=True,
        help_text=_("Secondary image")
    )

    def __str__(self):
        return f"{self.title}"


class Partnership_Content(models.Model):
    Partnership = models.ForeignKey(
    Partnership, related_name='Partnership', on_delete=models.CASCADE)

    title = models.CharField()

    def __str__(self):
        return f"{self.title}"


class PartnerReview(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Name of the person giving the review"
    )
    position = models.CharField(
        max_length=100,
        help_text="Position of the person giving the review"
    )
    image = models.ImageField(
        upload_to='partner_reviews/',
        help_text="Image of the person giving the review"
    )
    review = models.TextField(
        help_text="Review text"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this review is active and should be displayed"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time when the review was created"
    )

    def __str__(self):
        return f"{self.name}"



class PartnerFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0, help_text="Order in which the PartnerFAQ should be displayed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "PartnerFAQ"
        verbose_name_plural = "PartnerFAQs"

    def __str__(self):
        return self.question



class BusinessType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Business Type Name")
    )
    value = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Value")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_("Order")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _("Business Type")
        verbose_name_plural = _("Business Types")

    def __str__(self):
        return self.name


class PartnershipForm(models.Model):
    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.CASCADE,
        verbose_name=_("Type of business")
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last name")
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    message = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Message")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(
        default=False,
        verbose_name=_("Is processed")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Partnership Application")
        verbose_name_plural = _("Partnership Applications")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.business_type.name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"