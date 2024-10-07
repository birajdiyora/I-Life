from django.db import models
from django.contrib.auth.models import User

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name

# Define other necessary models like ProductGallery if needed.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=False)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='products/')

    # class Meta:
    #     managed = False
    #     db_table = 'products'
    # def __str__(self):
    #     return self.name

class FailedJob(models.Model):
    uuid = models.CharField(max_length=255, unique=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class Inquiry(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    product_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.customer_name

