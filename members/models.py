from django.db import models

# Create your models here.
class Signup(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    designation=models.CharField(max_length=255,default="staff")

    class Meta:
        db_table = 'members_signup'
    
    def __str__(self):
        return self.username
    
class Item(models.Model):
    #id = models.AutoField(primary_key=True)  # Add this
    ItemName = models.CharField(max_length=255, unique=True)  # Remove primary_key
    NumberOfItems = models.IntegerField()
    SellingPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ItemName
    
class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"{self.quantity} x {self.item.ItemName}"

