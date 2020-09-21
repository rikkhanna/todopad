from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('createddate',) # msut be a list or tuple

admin.site.register(Todo, TodoAdmin)
