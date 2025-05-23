from social_core.backends.oauth import BaseOAuth2
from requests.exceptions import HTTPError


class SuapOAuth2(BaseOAuth2):
    name = 'suap'
    AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
    ID_KEY = 'identificacao'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'
    

    def user_data(self, access_token, *args, **kwargs):
        try:
            scope = kwargs.get('response', {}).get('scope', '')
            response = self.request(
                url=self.USER_DATA_URL,
                data={'scope': scope},
                method='GET',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            response.raise_for_status() 
            return response.json()
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid access token") 
            raise
        except Exception as e:
            print(f"Erro ao buscar dados do usuário: {e}")
            raise

    def get_user_details(self, response):
        splitted_name = response['nome'].split()
        first_name, last_name = splitted_name[0], ''
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        return {
            'username': response[self.ID_KEY],
            'first_name': first_name.strip(),
            'last_name': last_name.strip(),
            'email': response['email_google_classroom'],
            'identification': response['identificacao'],
            'role': response['tipo_usuario'],
            'avatar': response['foto'],
            'social_name': response['nome_social'],
            'full_name': response['nome_registro']
        }