from django.db import models

class ProductMaster(models.Model):
    product_code = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class Shipment(models.Model):
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    shipment_date = models.DateField()

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
