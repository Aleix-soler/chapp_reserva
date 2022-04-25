import json
import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Book(models.Model):
    
    class TypeRoom(models.TextChoices):
        SINGLE = 'SINGLE',
        DOUBLE = 'DOUBLE',
        TRIPLE = 'TRIPLE',
        QUADRUPLE = 'QUADRUPLE'
    
    localizador = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    date_entry = models.DateField()
    date_exit = models.DateField()
    type_room = models.TextField(max_length=20, choices=TypeRoom.choices, default=TypeRoom.DOUBLE)
    price = models.FloatField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = PhoneNumberField(max_length=20)
    
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
