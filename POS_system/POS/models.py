from django.db import models

class Product(models.Model):
    PID = models.CharField(max_length= 12)
    Prd_Name = models.CharField(max_length= 200)
    stck_qnty = models.IntegerField(default= 0)
    prc = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    prdct = models.ForeignKey(Product, on_delete=models.CASCADE)
    Item_qnty = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.Item_qnty * self.prdct.prc

class Order(models.Model):
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        self.total = sum(item.get_total_price() for item in self.items.all())
        self.save()