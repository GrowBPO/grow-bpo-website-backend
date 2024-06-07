from django.contrib import admin
from bi_report.models import *


class ListingCompany(admin.ModelAdmin):
    """
    Classe de administração personalizada para o modelo Company.

    Esta classe define as opções de exibição para a listagem de empresas no painel administrativo.
    """
    
    list_display = ('company_name', 'company_cnpj', 'link_dashboard', 'is_active')
    list_display_links = ('company_name', 'company_cnpj')
    search_fields = ('company_name', 'company_cnpj')
    list_per_page = 25

class ListingUserCompany(admin.ModelAdmin):
    """
    Classe de administração personalizada para o modelo UserProfile.

    Esta classe define as opções de exibição para a listagem de perfis de usuário no painel administrativo.
    """
    

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.user.all()])

    def get_companies(self, obj):
        return ", ".join([company.company_name for company in obj.company.all()])

    list_display = ('get_users', 'get_companies')



admin.site.register(Company, ListingCompany)
admin.site.register(UserCompany, ListingUserCompany)