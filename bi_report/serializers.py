from django.core.exceptions import ValidationError
from django.contrib.auth import  authenticate
from rest_framework import serializers
from bi_report.models import *



class UserCompanySerializer(serializers.ModelSerializer):
    """
    Serializer para a relação entre usuários e empresas.

    Este serializer é responsável por serializar e desserializar os dados da relação entre usuários e empresas.
    Ele define os campos que serão expostos na API e valida os dados de entrada.

    Atributos:
        user (IntegerField): O ID do usuário relacionado.
        company (IntegerField): O ID da empresa relacionada.
    """
    
    class Meta:
        model = Company
        fields = ("company_name", "link_dashboard", "is_active")