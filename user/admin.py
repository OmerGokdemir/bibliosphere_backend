from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "firstName", "lastName", "builtIn"]
    list_display_links = ["firstName"]
    list_editable = ["builtIn"]