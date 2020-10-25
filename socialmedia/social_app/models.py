from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

# Create your models here.

class Address(models.Model):
	address_line_1 = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	address_line_2 = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	city = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	state = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	country = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	zip_code = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	phone_1 = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	phone_2 = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	fax = models.CharField(max_length=150, default=None, blank=True, null=True)


class AppUser(AbstractUser): 		
	ROLE_CHOICES = (
		('ADMIN', 'ADMIN'),
		('TUTOR', 'TUTOR'),
		('LEANER', 'LEANER'),
		)
	address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
	primary_role = models.CharField(
		max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
	dob = models.DateTimeField(default=None, null=True, blank=True)
	email_verified = models.BooleanField(default=False)
	GENDER_CHOICES = (
		('MALE', 'MALE'),
		('FEMALE', 'FEMALE'),
		('OTHERS', 'OTHERS'),
	)
	gender = models.CharField(
		max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

	def get_users(self):
		return User.objects.filter(id=self.id)

	def __str__(self):
		return self.username + "__user"

class Post(models.Model):
	subject = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	descripton = models.CharField(
		max_length=150, default=None, null=True, blank=True)
	weight = models.IntegerField(null=True, default=0)
	liked_users = models.ManyToManyField(AppUser, blank=True)
	time_created = models.DateTimeField(auto_now_add=True)
	time_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subject

class Image(models.Model):
	post = models.ForeignKey(
		Post, on_delete=models.CASCADE, default=None, null=False)
	image = models.ImageField(upload_to='uploads/')