from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances
from datetime import date
class Book(models.Model):
    title=models.CharField(max_length=200,unique=True)
    version = models.CharField(max_length=20,blank=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100,blank=True)

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
    area = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True)
    user=models.OneToOneField(User,related_name='user',on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.user.username


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True)
    postedon = models.DateTimeField()

    ACTION_STATUS = (
        ('sell', 'Sell'),
        ('rent', 'Rent'),
        ('buy', 'Buy'),
        ('borrow', 'Borrow'),
    )

    role = models.CharField(max_length=6, choices=ACTION_STATUS, help_text='task')

    class Meta:
        ordering = ["postedon"]
        permissions = (("authorized_user", "only authorized user"),)

    def __str__(self):
        """
        String for representing the Model object.
        """
        # return '%s (%s)' % (self.id,self.book.title)
        return '{0} ({1})'.format(self.user, self.book)
