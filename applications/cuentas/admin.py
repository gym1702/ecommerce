from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 
                    'last_login', 'date_joined', 'is_active',)
    
    list_display_links = ('email', 'username', 'first_name','last_name',)

    readonly_fields = ('last_login', 'date_joined', 'password',)

    ordering = ('-date_joined',)

    search_fields = ['email', 'username', 'phone',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()    


admin.site.register(Account, AccountAdmin)