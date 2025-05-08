from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import requests

class SUAPTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            response = requests.get(
                'https://suap.ifrn.edu.br/api/eu/',
                headers={'Authorization': f'Bearer {token}'}
            )

            if response.status_code != 200:
                raise exceptions.AuthenticationFailed('Invalid SUAP token')

            user_data = response.json()
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            splitted_name = user_data['nome'].split()
            first_name = splitted_name[0]
            last_name = splitted_name[-1] if len(splitted_name) > 1 else ''

            user, created = User.objects.get_or_create(
                username=user_data['identificacao'],
                defaults={
                    'first_name': first_name.strip(),
                    'last_name': last_name.strip(),
                    'email': user_data.get('email_google_classroom', ''),
                    'identification': user_data['identificacao'],
                    'role': user_data['tipo_usuario'],
                    'avatar': user_data['foto'],
                    'usual_name': user_data.get('nome_social', user_data['nome']),
                    'full_name': user_data['nome_registro']
                }
            )

            if not created:
                user.first_name = first_name.strip()
                user.last_name = last_name.strip()
                user.email = user_data.get('email_google_classroom', '')
                user.identification = user_data['identificacao']
                user.role = user_data['tipo_usuario']
                user.avatar = user_data['foto']
                user.usual_name = user_data.get('nome_social', user_data['nome'])
                user.full_name = user_data['nome_registro']
                user.save()

            return (user, None)

        except Exception as e:
            print(f"Erro na autenticação: {str(e)}")
            return None