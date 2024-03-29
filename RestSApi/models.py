from django.db import models

# Create your models here.


class City(models.Model):
    city = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.city

class Customer(models.Model):
    city = models.ForeignKey(City,null = True,blank = True,on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
