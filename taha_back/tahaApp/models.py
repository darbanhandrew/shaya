from random import randint

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from treebeard.mp_tree import MP_Node

from tahaApp.smshelper import otp_send


class Category(MP_Node):
    name = models.CharField(max_length=30)

    node_order_by = ['name']

    def __unicode__(self):
        return 'Category: %s' % self.name


active_roles = (
    ("affiliate", "affiliate"),
    ("manager", "manager")
)


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=active_roles, default="affiliate")
    STATUSES = (
        ('a', 'Active'),
        ('d', 'Deactive'),
    )
    status = models.CharField(max_length=2, choices=STATUSES, default="d")

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    sheba = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=20, blank=True, null=True)
    transaction_status = models.CharField(max_length=2, choices=STATUSES, default="d")

    def save(self, *args, **kwargs):
        if self.full_name and self.bank_name and self.sheba:
            self.transaction_status = 'a'
        else:
            self.transaction_status = 'd'
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


class OTP(models.Model):
    message = models.CharField(max_length=7, default=str(random_with_N_digits(5)))
    VALID = (
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    )
    valid = models.CharField(max_length=10, choices=VALID, default="valid")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.phone_number = instance.username
        profile.save()


@receiver(post_save, sender=Profile)
def create_profile_otp(sender, instance, created, **kwargs):
    if created:
        otp_s = OTP.objects.create(profile=instance)
        otp_s.save()
        wallet = Wallet.objects.create(related_profile=instance, amount=0)
        wallet.save()
        instance.save()


@receiver(post_save, sender=OTP)
def send_otp(sender, instance, created, **kwargs):
    if created:
        phone_number = instance.profile.user.username
        otp_send(phone_number, instance.message)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Image(models.Model):
    image = models.ImageField()
    woo_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    name = models.CharField(max_length=1000, blank=True, null=True)
    alt = models.TextField(max_length=1000, blank=True, null=True)
    original_src = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    slug = models.SlugField(max_length=200)
    url = models.URLField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    STATUSES = (
        ('a', 'Active'),
        ('d', 'Deactive'),
    )
    status = models.CharField(max_length=2, choices=STATUSES)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Shop(BaseModel):
    address = models.TextField(max_length=1000)
    email = models.EmailField(blank=True, max_length=48, verbose_name='E Mail')
    shop_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commission = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    consumer_key = models.CharField(max_length=100, blank=True, null=True)
    consumer_secret = models.CharField(max_length=100, blank=True, null=True)
    last_sync_time = models.DateTimeField(blank=True, null=True)
    images = models.ManyToManyField(Image)


class Product(BaseModel):
    related_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    categories = models.ManyToManyField(Category)
    woo_id = models.IntegerField(blank=True, null=True)
    images = models.ManyToManyField(Image)


# class Variation(BaseModel):
#     product = ParentalKey(Product, related_name='product_variations', on_delete=models.CASCADE)
#     stock = models.IntegerField(blank=True, null=True)

class Wallet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True, default=0)


class Receipt(models.Model):
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_amount = models.IntegerField(blank=True, null=True)
    affiliate_amount = models.IntegerField(blank=True, null=True)
    related_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')


class Transaction(models.Model):
    amount = models.IntegerField(blank=True, null=True)
    related_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    Types = (
        ('a', 'Add'),
        ('m', 'Minus'),
    )
    types = models.CharField(max_length=2, choices=Types, default='m')
