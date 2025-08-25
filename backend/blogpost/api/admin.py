from django.contrib import admin
from .models.user_models import UserInfo
from .models.blog_post_models import BlogPost
from django.utils.html import format_html

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone_number","email","password","created_at")  # show these columns in admin list
    search_fields = ("id","phone_number", "email","first_name")  # add search bar
    list_filter =   ("first_name",)    # add sidebar filter

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "image_preview")
    list_filter = ("author", "created_at")
    search_fields = ("title", "content", "author__username")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;"/>', obj.image.url) # pyright: ignore[reportUndefinedVariable]
        return "No Image"

    image_preview.short_description = "Preview"

admin.site.register(UserInfo)
admin.site.register(BlogPost)