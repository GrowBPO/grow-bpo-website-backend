from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import *


class ListingPasswordReset(admin.ModelAdmin):
    """
    Classe de administração personalizada para o modelo UserProfile.

    Esta classe define as opções de exibição para a listagem de perfis de usuário no painel administrativo.
    """

    list_display = ('email', 'token', 'created_at', 'expires_at')
    list_display_links = ('email', 'token',)
    search_fields = ('email', 'token',)
    list_per_page = 25


class CustomUserAdmin(UserAdmin):
    """
    Classe de administração personalizada para o modelo CustomUser.

    Esta classe define as opções de exibição e edição para os usuários no painel administrativo.
    """
    
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'first_login', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'first_login')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)



admin.site.register(PasswordReset, ListingPasswordReset)
admin.site.register(CustomUser, CustomUserAdmin)
