import uuid
import textwrap

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


def slug():
    return str(uuid.uuid4())


class BaseModel:
    
    def img_url(self):
        return self.image.url
    

class OrderOnCreate(models.Model):
    created_when = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ["-created_when"]


class User(BaseModel, AbstractUser):
    profile_pic = models.ImageField(upload_to="admin_profiles", blank=True)
    description = models.CharField(max_length=1000, blank=True)
    
    def img_url(self):
        pass
    
    def get_name(self):
        return self.get_full_name() or self.username

class Blog(BaseModel, OrderOnCreate):
    slug = models.SlugField(default=slug, editable=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images", null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="articles", null=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_when']
    
    def pre_save(self, _, blog, *a, **kw):
        "Set the blog author to the current active user"
        pass
    
    def pub_date(self):
        return self.created_when
    
    def get_short_post(self):
        return textwrap.shorten(self.content, 350, placeholder="...")
    
    def c_len(self):
        # return comment len string eg. 3 comment(s)
        len = self.comments.count()
        s = 's' if len > 1 else ''
        return '{} Comment{}'.format(len, s)
    
    def cover_img(self):
        return self.image.url


class Comment(OrderOnCreate):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    
    username = models.CharField(max_length=150, blank=True, default='anonymous')
    comment_text = models.CharField(max_length=3000, default="")
    
    class Meta:
        ordering = ['created_when']

    def get_username(self):
        if self.user:
            return self.user.username
        return self.username
    
    def __str__(self):
        return self.comment_text
    
    def __repr__(self):
        return '[%s: %s...]' % (self.username, self.comment_text[:10])


# sync feed

class SyncFeed(models.Model):
    email = models.EmailField(unique=True)