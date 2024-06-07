from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    """
    Modelo personalizado de usuário que estende a classe AbstractUser do Django.

    Este modelo adiciona um campo adicional para rastrear se é o primeiro login do usuário.

    Atributos:
    - first_login: Um campo booleano que indica se este é o primeiro login do usuário.
                   O padrão é True, indicando que o usuário está fazendo login pela primeira vez.

    Métodos:
    - __str__(): Retorna uma representação string do objeto, utilizando o nome de usuário como identificador.
    """
    
    first_login = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.username
    

class PasswordReset(models.Model):
    """
    Modelo que representa uma solicitação de redefinição de senha.

    Este modelo armazena informações sobre uma solicitação de redefinição de senha, incluindo o endereço de e-mail do usuário,
    o token gerado para a redefinição de senha e a data e hora em que a solicitação foi criada.

    Atributos:
    - email: Endereço de e-mail associado à solicitação de redefinição de senha.
    - token: Token gerado para a redefinição de senha.
    - created_at: Data e hora de criação da solicitação de redefinição de senha.
    """
     
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, default=None)


