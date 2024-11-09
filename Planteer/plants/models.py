from django.db import models

# Create your models here.

class Plant (models.Model):
    name=models.CharField(max_length=124)
    about=models.TextField()
    used_for=models.TextField()
    image=models.FileField(upload_to="images/",default='images/default.jpg')
    is_edible=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)

    class CategoryChoices(models.TextChoices):
        INDOOR='IN',"Indoor Plants"
        OUTDOOR='OUT',"Outdoor Plants"
        FRUITSVEGETABLES='FV',"Fruit & Vegetable"
        SUCCULENTCACTI='SC',"Succulents & Cacti"
        FLOWERS='FL',"Flowers"

    category=models.CharField(max_length=64,choices=CategoryChoices.choices,default=CategoryChoices.INDOOR)

