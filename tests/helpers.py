

class AuthActions:
    """Authentication helper class. Adapted from:
    https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/#authentication
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password="password"):

        return self._client.post(
            '/auth/login',
            data=dict(username=username, password=password)
        )

    def logout(self):
        return self._client.get('/auth/logout')
