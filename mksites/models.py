from django.db import models

# Create your models here.
from subdomains.models import Subdomain

class SubModelManager(models.Manager):
    
    def of_domain(self):
        pass


class SubModel(models.Model):
    subdomain = models.ForeignKey(Subdomain,blank=True,null=True)
    
    class Meta:
        abstract = True
        
    