from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.utils.html import mark_safe


from PIL import Image
from shortuuid.django_fields import ShortUUIDField



RELATIONSHIP = (
    ("single","Single"),
    ("married","married"),
    ("inlove","In Love"),
)


GENDER = (
    ("female", "Female"),
    ("male", "Male"),
)

WHO_CAN_SEE_MY_FRIENDS = (
    ("Only Me","Only Me"),
    ("Everyone","Everyone"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)

    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover.jpg", blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.CharField( max_length=1000,null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP, null=True, blank=True, default="single")
    friends_visibility = models.CharField(max_length=100, choices=WHO_CAN_SEE_MY_FRIENDS, null=True, blank=True, default="Everyone")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    working_at = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.URLField(default="https://instagram.com/", null=True, blank=True)
    whatsApp = models.CharField(default="+123 (456) 789", max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    followings = models.ManyToManyField(User, blank=True, related_name="followings")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    groups = models.ManyToManyField("core.Group", blank=True, related_name="groups")
    pages = models.ManyToManyField("core.Page", blank=True, related_name="pages")
    blocked = models.ManyToManyField(User, blank=True, related_name="blocked")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)


    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #     if img.height > 700 or img.width > 700:
    #         output_size = (700, 700)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    #     super().save(*args, **kwargs)

    
    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image))

    
    
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

