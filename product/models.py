from django.db import models
from mksites.models import SubModel

class Product(SubModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    shortcut = models.CharField(max_length=100)
    category = models.ForeignKey("ProductCategory")
    image = models.ImageField(upload_to="media/images",blank=True,null=True)
    def __unicode__(self):
        return self.name



class ProductCategory(SubModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name



