from django.contrib import admin

from .models import *


class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title']
    
    class Media:
        css = {
            'all': ['core/assets/vendor/bootstrap/css/bootstrap.min.css',  'core/plugin/summernote/summernote-bs4.min.css', 'core/plugin/summernote/complete.scss']
        }
        js = (
            'core/assets/vendor/jquery/jquery.min.js',
            'core/assets/vendor/popper/js/popper.min.js',
            'core/assets/vendor/bootstrap/js/bootstrap.min.js',
            'core/plugin/summernote/summernote-bs4.min.js',
            'core/assets/js/main.js')


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username',)
    
    class Media:
        js = ('core/assests/js/main.js',)

# def main(models):
#     # automaticaly register's models in the admin with model admins
#     # if presents
#     for model in models:
#         model_name = model.__name__
#         model_admin_name = model_name + 'ModelAdmin'
        
#         modelAdmin = globals().get(model_admin_name) # return None
        
#         # register
#         admin.site.register(model, modelAdmin)


# main([Blog, User, Post, Comment, Category])

# main([Blog, User])

admin.site.register(User)
admin.site.register(Blog, BlogModelAdmin)