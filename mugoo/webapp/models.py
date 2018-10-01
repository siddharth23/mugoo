from django.db import models
from django.urls import reverse
# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=200,unique=True)
    version = models.CharField(max_length=20,blank=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100,blank=True)
    postedon = models.DateTimeField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
class Area(models.Model):
    pincode=models.IntegerField(max_length=6,unique=True,primary_key=True)
    area=models.CharField(max_length=200)
    def __str__(self):
        return self.area

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
    area = models.ForeignKey(Area)
    user=models.OneToOneField(User,related_name='user')
    def __str__(self):
        return self.user.name