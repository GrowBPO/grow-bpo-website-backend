from django.contrib.auth import login, logout
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from login.validations import *
from login.serializers import *
from login.models import *
from email.mime.image import MIMEImage
import pytz
import os



class CheckAuthView(APIView):
    """
    
    """

    # Define as permissões e autenticações necessárias
    permission_classes = (AllowAny, )
    authentication_classes = (SessionAuthentication, )
    

    # Retorna as informações do usuário autenticado
    def get(self, request):

        # Recebe e valida os dados do usuário
        user = request.user
        
        if user.is_authenticated:
            return Response({'auth': 'true'}, status=status.HTTP_200_OK)
        
        return Response({'auth': 'false'}, status=status.HTTP_200_OK)



class UserView(APIView):
    """
    Classe de visualização para recuperar informações do usuário autenticado.

    Permite que usuários autenticados obtenham informações sobre si mesmos.
    Esta visualização requer que os usuários estejam autenticados e usa a autenticação de sessão
    para garantir que apenas usuários autenticados possam acessá-la.

    Métodos:
    - get(request): Obtém informações sobre o usuário autenticado. Retorna um objeto JSON
    contendo os detalhes do usuário autenticado, junto com uma resposta HTTP 200 OK.
    """

    # Define as permissões e autenticações necessárias
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    # Retorna as informações do usuário autenticado
    def get(self, request):

        # Recebe e valida os dados do usuário
        user = request.user
        serializer = UserSerializer(user)

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    Classe de visualização para lidar com a autenticação de usuários.

    Permite que os usuários façam login fornecendo um nome de usuário e senha. Esta visualização
    é acessível a todos (não requer autenticação) e usa autenticação de sessão para manter o estado de login.

    Métodos:
    - post(request): Executa o processo de login. Recebe os dados de login do usuário, valida-os
      e, se bem-sucedido, autentica o usuário e retorna os dados do usuário autenticado.
      Retorna uma resposta HTTP 200 OK em caso de sucesso.
    """

    # Define as permissões e autenticações necessárias
    permission_classes = (AllowAny, )
    authentication_classes = (SessionAuthentication, )

    # Realiza o Login do Usuário
    def post(self, request):

        # Recebe e valida os dados do usuário
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = LoginSerializer(data=data)

        # Verifica se os dados são válidos
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Classe de visualização para lidar com o processo de logout de usuários.

    Permite que os usuários realizem logout da sessão atual. Esta visualização
    é acessível a todos (não requer autenticação).

    Métodos:
    - post(request): Executa o processo de logout. Encerra a sessão do usuário atual
    e retorna uma resposta HTTP 200 OK.
    """

    # Define as permissões e autenticações necessárias
    permission_classes = (AllowAny, )
    authentication_classes = ()

    # Realiza o Logout do usuário
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

 
class RedefinePasswordView(GenericAPIView):
    """
    Classe de visualização para o processo de redefinição de senha.

    Permite que os usuários solicitem a redefinição de sua senha fornecendo seu endereço de e-mail.
    Esta visualização é acessível a todos (não requer autenticação) e utiliza um token de redefinição de senha
    para gerar um URL exclusivo para a redefinição de senha, que é enviado ao usuário por e-mail.

    Atributos:
    - permission_classes: Lista de classes de permissão que permitem acesso a esta visualização.
    - serializer_class: Classe de serialização usada para validar e processar os dados da solicitação.

    Métodos:
    - post(request): Executa o processo de redefinição de senha. Recebe o endereço de e-mail do usuário,
      gera um token de redefinição de senha, cria um registro de redefinição de senha no banco de dados,
      envia um e-mail ao usuário contendo um URL exclusivo para a redefinição de senha e retorna uma resposta HTTP 200 OK.
      Retorna um erro HTTP 404 Not Found se o endereço de e-mail fornecido não estiver associado a nenhum usuário.
    """

    # Define as permissões e autenticações necessárias
    permission_classes = (AllowAny, )
    serializer_class = RedefinePasswordSerializer

    # Realiza a requisição para redefinição da senha
    def post(self, request):
        # Recebe e valida os dados do usuário
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        user = CustomUser.objects.filter(email__iexact=email).first()

        # Se o email estiver correto faz o envio do email
        if user:

            # Gera o token de redefinição de senha
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            fuso_horario = pytz.timezone('America/Sao_Paulo')
            expiry_date = datetime.now().astimezone(fuso_horario) + timedelta(hours=1)

            # Cria o registro de redefinição no banco de dados
            reset = PasswordReset(email=email, token=token, expires_at=expiry_date)
            reset.save()

            # Constrói a url exclusiva para a redefinição de senha
            reset_url = f"http://growbpo.com.br/api/auth/reset-password/{token}"
            reset_url_front = f"http://growbpo.com.br/reset-password/{token}"

            # Lógica para envio do email de redefinição de senha
            subject = 'GROW BPO - Redefinição de senha'
            html_message = render_to_string('email/reset_password.html', {'reset_url': reset_url, 'reset_url_front': reset_url_front })
            plain_message = strip_tags(html_message)
            from_email = 'noreply@growbpo.com'
            to = email

            # email_message = EmailMultiAlternatives(subject, plain_message, from_email, [email])
            # email_message.attach_alternative(html_message, "text/html")

            # image_path = os.path.join(settings.STATIC_ROOT, 'email/grow-nome-degrade.png')
            # try:
            #     with open(image_path, 'rb') as img:
            #         mime_image = MIMEImage(img.read(), _subtype="png")
            #         mime_image.add_header('Content-ID', '<logo_image>')
            #         email_message.attach(mime_image)
            #         print("enviado")
            # except FileNotFoundError:
            #     print("Erro: Arquivo de imagem não encontrado.")
            
            # except Exception as e:
            #     # Outros erros ao abrir ou anexar a imagem
            #     print("Erro ao abrir ou anexar a imagem:", e)

            # Envia o email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            return Response({'success': 'Enviamos um link por email para a redefinição de senha'}, status=status.HTTP_200_OK)
        
        # Retorna um erro caso o email não esteja associado a nenhum usuário
        else:
            return Response({"error": "Email não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

class ResetPasswordView(GenericAPIView):
    """
    Classe de visualização para o processo de redefinição de senha.

    Permite que os usuários redefinam sua senha usando um token exclusivo enviado por e-mail.
    Esta visualização é acessível a todos (não requer autenticação) e recebe um token de redefinição de senha
    como parte do URL da solicitação.

    Atributos:
    - permission_classes: Lista de classes de permissão que permitem acesso a esta visualização.
    - serializer_class: Classe de serialização usada para validar e processar os dados da solicitação.

    Métodos:
    - post(request, token): Executa o processo de redefinição de senha. Recebe o token de redefinição de senha
      como parte do URL da solicitação e os novos dados de senha do corpo da solicitação.
      Valida as senhas, verifica se o token é válido, atualiza a senha do usuário correspondente
      e retorna uma resposta HTTP 200 OK em caso de sucesso. Retorna um erro HTTP 400 Bad Request
      se as senhas não coincidirem ou o token for inválido, e um erro HTTP 404 Not Found se nenhum
      usuário correspondente for encontrado.
    """

    # Define as permissões e autenticações necessárias
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    # Realiza a requisição para redefinição da senha
    def post(self, request, token):

        # Recebe e valida os dados do usuário
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        

        # Obtém a nova senha e a confirmação da senha
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        # Verifica se as senhas coincidem
        if new_password != confirm_password:
            return Response({"error:": "As senhas não coincidem."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Busca o objeto de redefinição de senha com base no token
        reset_obj = PasswordReset.objects.filter(token=token).first()
        expires_at = reset_obj.expires_at


        # Verifica se o token é válido
        if not reset_obj or expires_at < timezone.now():
            return Response({"error": "Token Inválido"}, status=status.HTTP_400_BAD_REQUEST)

         # Busca o usuário associado ao e-mail do objeto de redefinição de senha
        user = CustomUser.objects.filter(email=reset_obj.email).first()
        
        # Se o usuário associado ao email for válido define a nova senha para o usuário, desmarca a opção de primeiro login e salva
        if user:
            user.set_password(request.data['new_password'])
            user.first_login = False
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Senha Alterada.'})
        
        # Retorna um erro se nenhum usuário for encontrado
        else: 
            return Response({'error':'Nenhum usuário encontrado.'}, status=status.HTTP_404_NOT_FOUND)

