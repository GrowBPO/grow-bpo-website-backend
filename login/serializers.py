from django.core.exceptions import ValidationError
from django.contrib.auth import  authenticate
from rest_framework import serializers
from login.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo de usuário.

    Converte objetos do modelo de usuário em representações JSON e vice-versa.
    Este serializador define os campos que serão incluídos na representação JSON do usuário.

    Campos:
    - username: O nome de usuário do usuário.
    - email: O endereço de e-mail do usuário.
    - first_name: O primeiro nome do usuário.
    - last_name: O sobrenome do usuário.
    - first_login: Indica se é o primeiro login do usuário.
    """
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'first_login']
        
        
class LoginSerializer(serializers.Serializer):
    """
    Serializador para o processo de login do usuário.

    Realiza a validação dos dados de login do usuário e autentica o usuário correspondente.

    Campos:
    - username: Campo para inserir o nome de usuário do usuário.
    - password: Campo para inserir a senha do usuário.

    Métodos:
    - check_user(data): Verifica se as credenciais de login fornecidas correspondem a um usuário válido
      no sistema. Retorna o usuário autenticado se as credenciais forem válidas, caso contrário,
      levanta uma exceção de validação.
    """

    username = serializers.CharField()
    password =  serializers.CharField()
    
    def check_user(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise ValidationError('Usuário não encontrado')
        
        return user
    

class RedefinePasswordSerializer(serializers.Serializer):
    """
    Serializador para solicitação de redefinição de senha.

    Campos:
    - email: Campo para obrigatório para inserir o endereço de e-mail do usuário que deseja redefinir a senha.
    """

    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializador para redefinição de senha.

    Realiza a validação das novas senhas fornecidas pelo usuário durante o processo de redefinição de senha.

    Campos:
    - new_password: Campo para inserir a nova senha do usuário.
    - confirm_password: Campo para confirmar a nova senha do usuário.

    Atributos:
    - new_password: Campo obrigatório para inserir a nova senha, com estilo de entrada de senha.
      A senha deve ter no mínimo 8 caracteres.
    - confirm_password: Campo obrigatório para confirmar a nova senha, com estilo de entrada de senha.
      A senha deve ter no mínimo 8 caracteres.
    """

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8,
        error_messages={'min_length': 'A senha deve ter no mínimo 8 caracteres.'}
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8,
        error_messages={'min_length': 'A senha deve ter no mínimo 8 caracteres.'}
    )

