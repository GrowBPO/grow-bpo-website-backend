from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from bi_report.models import *
from bi_report.serializers import *
from rest_framework.response import Response



class UserCompanyView(APIView):

    # Define as permissões e autenticações necessárias
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    # Retorna as informações do usuário autenticado
    def get(self, request, user_id):
        try:
            # Verificar se o usuário autenticado é o mesmo que está sendo solicitado
            if request.user.id != int(user_id):
                return Response({'detail': 'Você não tem permissão para acessar estas informações.'}, status=status.HTTP_403_FORBIDDEN)

            # Buscar todas as instâncias de UserCompany associadas ao usuário
            user_companies = UserCompany.objects.filter(user__id=user_id)
            
            # Extrair as empresas de todas as instâncias de UserCompany
            companies = []
            for user_company in user_companies:
                companies.extend(user_company.company.all())
            
            # Serializar os dados
            serializer = UserCompanySerializer(companies, many=True)
            return Response({'user_companies': serializer.data}, status=status.HTTP_200_OK)
        
        except UserCompany.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

