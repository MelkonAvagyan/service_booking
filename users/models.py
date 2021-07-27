from django.db import models
from register.models import Specialist, Client
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

Categories = (
	('Self&Beauty Care', 'SELF&BEAUTY CARE'),
	('Education','EDUCATION'),
	('Software Services', 'SOFTWARE SERVICES'),
	('Home Services', 'HOME SERVICES'),
	('Handmade Products', 'HANDMADE PRODUCTS'),
	)

class Categories(models.Model):
	name = models.CharField(max_length=6, choices=Categories, default='Self&Beauty Care', db_index=True, verbose_name="Categories")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class SpecialistProfile(models.Model):
	specialist = models.OneToOneField(Specialist, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to='specialists/profile_pic/%Y/%m/%d/', null=True, blank=False)
	description_bio = models.CharField(max_length=200, null=True)
	average_price = models.FloatField(null=True)
	images = models.ImageField(upload_to='specialists/portfolio/%Y/%m/%d/', null=True, blank=True)
	additional_url = models.URLField(max_length=300, blank=True, null=True)
	tag = models.ManyToManyField('Tag')
	slug = slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	reviews = models.ForeignKey(Reviews,  on_delete=models.CASCADE)
	
	class Meta:
		order_with_respect_to = 'reviews'

	@property
	def imageURL(self):
		try:
			url = self.profile_pic.url
		except:
			url = ''
		return url

	@property
	def portfolio(self):
		try:
			return self.images.url
		except AttributeError:
			return 'There is nothing to show.'

    # def get_absolute_url(self):
    #     return reverse('specialist_account',kwargs={'specialist_account_slug':self.slug})



class ClientProfile(models.Model):
	client = models.OneToOneField(Client, on_delete=models.CASCADE)
	profile_pic = models.ImageField(default = 'profile.png', upload_to='clients/profile_pic/%Y/%m/%d/', null=True, blank=False)
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
	
	@property
	def profile_pic(self):
		try:
			return self.profile_pic.url
		except AttributeError:
			return 'There is nothing to show.'


	# def get_absolute_url(self):
    #     return reverse('client_account',kwargs={'client_account_slug':self.slug})



class Reviews(models.Model):
	VOTE_TYPE = (
		('UP','up'),
		('DOWN', 'down'),
	)
	reviewer = models.ForeignKey(Client,  on_delete=models.CASCADE)
	specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='reviews')
	review_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	description = models.TextField(null=True, blank=True)
	value = models.CharField(max_length=50, choices=VOTE_TYPE)
    reviews = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
		return self.value

	def avg_rating(self):
        sum = 0
        ratings = Reviews.objects.filter(rating=self)
        for rating in ratings:
            sum += rating
        if len(ratings) > 0:
            return sum / len(rating)
        else:
            return 0

class Tag(models.Model):
	name = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
		

# class Order(models.Model):
# 	STATUS = (
# 			('Pending', 'Pending'),
# 			('Out for delivery', 'Out for delivery'),
# 			('Completed', 'Completed'),
# 			)

# 	customer = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
# 	specialist = models.ForeignKey(Specialist, null=True, on_delete= models.SET_NULL)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	price = models.FloatField(null=True)
# 	status = models.CharField(max_length=200, null=True, choices=STATUS)
# 	notes = models.CharField(max_length=1000, null=True)

# 	def __str__(self):
# 		return f'Transaction between {self.specialist.username} and {self.client.username}'
	
	
# 	@property
# 	def get_cart_total(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.get_total for item in orderitems])
# 		return total 

# 	@property
# 	def get_cart_items(self):
# 		orderitems = self.orderitem_set.all()
# 		total = sum([item.quantity for item in orderitems])
# 		return total 


# 	class Meta:
# 		get_latest_by = 'date_created'


# class OrderItem(models.Model):
# 	specialist = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True)
# 	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
# 	quantity = models.IntegerField(default=0, null=True, blank=True)
# 	date_added = models.DateTimeField(auto_now_add=True)

# 	@property
# 	def get_total(self):
# 		total = self.order.price * self.quantity
# 		return total




# class Message(models.Model):
#     sender = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
#     recipient = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
#     name = models.CharField(max_length=200, null=True, blank=True)
#     email = models.EmailField(max_length=200, null=True, blank=True)
#     subject = models.CharField(max_length=200, null=True, blank=True)
#     body = models.TextField()
#     is_read = models.BooleanField(default=False, null=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.subject

#     class Meta:
#         ordering = ['is_read', '-created']