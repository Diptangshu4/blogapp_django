from django.contrib import admin
from .models import Post, Tag, Author, Comment, User, Category

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Category)