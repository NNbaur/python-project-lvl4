from django.contrib import admin
from django import forms
from .models import MyUser

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('id', 'is_superuser', 'username', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'date_joined')
    fields = ('id', 'is_superuser', 'username', 'first_name', 'last_name', 'date_joined')
    list_filter = ('date_joined', )

admin.site.register(MyUser, UserAdmin)
