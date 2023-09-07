from django.db import models
from django.utils.translation import gettext as _


class SocialMedia(models.Model):
    """
    Model for storing social media profiles.
    """
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Medias"

    def __str__(self) -> str:
        return self.name


class AppStoreLink(models.Model):
    """
    Model for storing links to mobile apps on the App Store and Google Play Store.
    """
    app_name = models.CharField(max_length=255)
    ios_url = models.URLField(blank=True, null=True)
    android_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "App Store Link"
        verbose_name_plural = "App Store Links"

    def __str__(self) -> str:
        return self.app_name


class CompanyInfo(models.Model):
    """
    Model for storing company information, including contact details and app links.
    """
    phone_number = models.CharField(max_length=20)

    social_media = models.ManyToManyField(SocialMedia, blank=True)
    app_links = models.ManyToManyField(AppStoreLink, blank=True)

    logo = models.FileField(upload_to="company/logo")

    class Meta:
        verbose_name = "Company Info"
        verbose_name_plural = "Company Info"

    def __str__(self) -> str:
        return "Company Info"


class Banner(models.Model):
    """
    Model for storing banners with titles, descriptions, images, and URLs.
    """
    title = models.CharField(max_length=150)
    short_description = models.CharField(max_length=350)
    image = models.FileField()
    url = models.URLField()

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title


class AdTypeAttribute(models.Model):
    """
    Model for storing attributes of advertisement types.
    """
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Ad Type Attribute"
        verbose_name_plural = "Ad Type Attributes"

    def __str__(self):
        return self.name


class AdType(models.Model):
    """
    Model for defining advertisement types with names, validity periods, and attributes.
    """
    VALIDITY_CHOICES = (
        ('1d', _('1 day')),
        ('7d', _('7 days')),
        ('30d', _('40 days')),
    )

    name = models.CharField(max_length=250)
    validity_period = models.CharField(max_length=3, choices=VALIDITY_CHOICES)
    attributes = models.ManyToManyField(AdTypeAttribute, blank=True)

    class Meta:
        verbose_name = "Ad Type"
        verbose_name_plural = "Ad Types"

    def __str__(self):
        return self.name
