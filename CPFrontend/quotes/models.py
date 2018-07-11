from django.db import models


class Quote(models.Model):
    internalCode = models.PositiveIntegerField(blank=True)
    externalCode = models.PositiveIntegerField(blank=True)
    providerCode = models.CharField(max_length=255, blank=True)
    receivedDate = models.CharField(max_length=255, blank=True)
    sentDate = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, blank=True)
    providerId = models.CharField(max_length=255, blank=True)
    providerName = models.CharField(max_length=255, blank=True)
    contactName = models.CharField(max_length=255, blank=True)
    incoterms = models.CharField(max_length=255, blank=True)
    note = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')

