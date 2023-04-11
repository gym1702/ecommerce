from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

#
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


#
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Imagen de perfil'


    list_display = ('thumbnail', 'user', 'city', 'state', 'country', 'credit',)
    list_display_links = ('thumbnail', 'user',)
    search_fields = ['user',]
    list_editable = ('credit',)
    


#
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)