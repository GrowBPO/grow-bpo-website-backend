from django.core.exceptions import ValidationError



def validate_email(data):
    email = data['email'].strip()

    if not email:
        raise ValidationError("Informe um email")
    
    return True


def validate_username(data):
    username = data['username'].split()

    if not username:
        raise ValidationError("Informe um email")
    
    return True


def validate_password(data):
    password = data['password'].split()

    if not password:
        raise ValidationError("Informe uma Senha")
    
    return True

