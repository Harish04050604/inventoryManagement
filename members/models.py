from django.db import models

# Signup Model
class Signup(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, default="staff")

    class Meta:
        db_table = 'members_signup'

    def __str__(self):
        return self.username


# Item Model
class Item(models.Model):
    ItemName = models.CharField(max_length=255, unique=True)
    NumberOfItems = models.IntegerField()
    SellingPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ItemName


# Sale Model
class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.ItemName}"


# AddItem Model (Tracks Production)
class AddItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Foreign Key from Item
    date_of_production = models.DateField()
    total_items_produced = models.PositiveIntegerField()
    total_production_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.total_items_produced} produced for {self.item.ItemName} on {self.date_of_production}"


# SellItem Model (Tracks Sales)
class SellItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Foreign Key from Item
    date_of_sales = models.DateField()
    total_items_sold = models.PositiveIntegerField()
    total_sales_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.total_items_sold} sold for {self.item.ItemName} on {self.date_of_sales}"
