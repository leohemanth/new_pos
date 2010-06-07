from django.db import models
from mksites.models import SubModel


class SaleInvoice(SubModel):
    customer = models.ForeignKey('customer.Customer')
    datetime = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return str(self.pk)

    
class SaleInvoiceItem(SubModel):
    invoice = models.ForeignKey(SaleInvoice)
    product = models.ForeignKey('product.Product')
    quantity = models.PositiveSmallIntegerField()
    sold_at_price = models.DecimalField(max_digits=7,decimal_places=2)

    def __unicode__(self):
        return "%s:%s"%(self.invoice.id,self.product.name)


