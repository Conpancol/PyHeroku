from django.db import models


class RFQ(models.Model):
    internalCode = models.PositiveIntegerField(blank=True)
    externalCode = models.PositiveIntegerField(blank=True)
    sender = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    receivedDate = models.CharField(max_length=255, blank=True)
    note = models.CharField(max_length=255, blank=True)
    processedDate = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')


class RFQMaterial(models.Model):
    orderNumber = models.PositiveIntegerField(blank=True)
    itemCode = models.CharField(max_length=255, blank=True)
    quantity = models.FloatField(blank=True)
    unit = models.CharField(max_length=255, blank=True)

