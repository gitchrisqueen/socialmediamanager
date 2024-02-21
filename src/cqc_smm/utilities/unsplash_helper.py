from unsplash.api import Api
from unsplash.auth import Auth

client_id = ""
client_secret = ""
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)