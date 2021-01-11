from django.contrib import admin
from .models import *

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    class Meta:
        model = Note

    list_display = ['id', 'user', 'create_date', 'group']


admin.site.register(Note, NoteAdmin)
admin.site.register(Group)
