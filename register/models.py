from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ViewDoesNotExist
from django.db import models
from django.urls.base import reverse
from users.models import Categories
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

Categories = (
	('Self&Beauty Care', 'SELF&BEAUTY CARE'),
	('Education','EDUCATION'),
	('Software Services', 'SOFTWARE SERVICES'),
	('Home Services', 'HOME SERVICES'),
	('Handmade Products', 'HANDMADE PRODUCTS'),
	)

	Job_type = (	
	('self employed', 'Self Employed'),
	('employee', 'Employee'),
	('both', 'both'),
	)

	Handling = (
		('delivery', 'delivery'),
		('in place', 'in place'),
		('both','both'),
	)

class User(AbstractUser):
    is_specialist = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)


class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, primary_key=True)
	username = models.CharField(max_length=200, null=True)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	phone_number = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	password = models.CharField(max_length=128)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('client_account', kwargs={'client_account_slug': self.slug})


class Specialist(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, primary_key=True)
	username = models.CharField(max_length=200, null=True)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	phone_number = models.IntegerField(default=0)
	category = models.ForeignKey(Categories, max_length=6, choices=Categories, default='Self&Beauty Care', on_delete=models.PROTECT)
	job_type = models.CharField(max_length=3, choices=Job_type, default = 'Self Employeed')
	company_name = models.CharField(max_length=200, null=True, blank=True) 
	handling = models.CharField(max_length=3, choices=Handling, default = 'delivery')
	address = models.CharField(max_length=300, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	password = models.CharField(max_length=128)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('specialist_account', kwargs={'specialist_account_slug': self.slug})
    class Meta:
        ordering = ['is_read', '-created']
		

class Review(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    specialist = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.rating


    def avg_rating(self):
        sum = 0
        ratings = Review.objects.filter(rating=self)
        for rating in ratings:
            sum += rating
        if len(ratings) > 0:
            return sum / len(rating)
        else:
            return 0
