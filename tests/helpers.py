class AuthActions:
    """Authentication helper class. Adapted from:
    https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/#authentication
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password="password", remember_me=False, follow_redirects=True):
        data=dict(username=username, password=password, remember_me=remember_me)
        return self._client.post('/auth/login', data=data, follow_redirects=follow_redirects)

    def logout(self):
        return self._client.get('/auth/logout')
