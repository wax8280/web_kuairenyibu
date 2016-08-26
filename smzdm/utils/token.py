from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re

class Token():

    def __init__(self,security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('ascii'))

    def generate_validate_token(self,username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username,self.salt)

    def confirm_validate_token(self,token,expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token,salt=self.salt,max_age=expiration)