# projects/models.py

from django.db import models

class Project(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    salesRep = models.CharField(max_length=100)
    client = models.CharField(max_length=200)
    creationDate = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=20)
    probability = models.IntegerField(null=True, blank=True)
    estimatedValue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    estimatedCloseDate = models.DateField(null=True, blank=True)
    contractValue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    contractDate = models.DateField(null=True, blank=True)
    total_received_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'projects_project'
        unique_together = ('code',)

    def __str__(self):
        return self.name
