from django.contrib import admin
from todo_app.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)





