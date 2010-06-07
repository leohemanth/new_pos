from django.db import models
from mksites.models import SubModel

class CompanyContact(SubModel):
    name = models.CharField(max_length=100)
    phone_number = models.fields.PositiveIntegerField()
    email = models.fields.EmailField()
    description = models.TextField()
    company = models.ForeignKey('Company')
    image = models.ImageField(upload_to="media/images",blank=True,null=True)

    def __unicode__(self):
        return self.name

class Company(SubModel):
    name = models.CharField(max_length=100)
    details = models.TextField()
    phone_number = models.CharField(max_length=11)

    def __unicode__(self):
        return self.name
