from django.db import models
import datetime
import os

# Create your models here.
def get_file_path(request, filename):
    original_filename = filename
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (now_time, original_filename)
    return os.path.join('uploads/', filename)

class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to="uploads/products/", null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False, help_text="default = 0, Hidden = 1")
    trending = models.BooleanField(default=False, help_text="default = 0, Trending = 1")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to= 'uploads/products/', null=True, blank=True)
    small_description = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    on_sale = models.BooleanField(default=False)
    description = models.TextField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="default = 1, Hidden")
    trending = models.BooleanField(default=False, help_text="default = 1, Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

