from django.db import models
from login.models import CustomUser


class Company(models.Model):
    """
    Modelo que representa uma empresa.

    Atributos:
    - company_cnpj: CNPJ da empresa (opcional).
    - company_name: Nome da empresa (obrigatório).
    - link_dashboard: Link para o dashboard da empresa (opcional).
    - is_active: Indica se a empresa está ativa ou inativa (padrão: ativa).

    Métodos:
    - __str__(): Retorna uma representação string do objeto, utilizando o nome da empresa como identificador.
    """

    company_cnpj = models.CharField(max_length=30, blank=True, null=True, unique=True)
    company_name = models.CharField(max_length=30, blank=False)
    link_dashboard = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.company_name


class UserCompany(models.Model):
    """
    Modelo que representa o perfil de um usuário.

    Este modelo está vinculado a um usuário do sistema e a uma empresa associada.

    Atributos:
    - user: Campo de chave estrangeira que se refere a um usuário do sistema.
    - company: Campo de chave estrangeira que se refere a uma empresa associada ao usuário.

    Métodos:
    - __str__(): Retorna uma representação string do objeto, utilizando o nome de usuário do usuário como identificador.
    """

    user = models.ManyToManyField(CustomUser)
    company = models.ManyToManyField(Company)

    def __str__(self) -> str:
        users_str = ", ".join([user.username for user in self.user.all()])
        companies_str = ", ".join([company.company_name for company in self.company.all()])
        return f"Users: {users_str}, Companies: {companies_str}"
    