from django.db import models
from mksites.models import SubModel
from mksites.models import Subdomain

class Customer(SubModel):
    name = models.CharField(max_length=100)
    details = models.TextField()
    phone_number = models.fields.PositiveIntegerField()
    email = models.fields.EmailField()
    Category = models.ForeignKey('CustomerCategory')
    def __unicode__(self):
        return self.name


class CustomerCategory(SubModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name



