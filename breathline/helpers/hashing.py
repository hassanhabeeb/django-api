from django.conf import settings
from django.core.signing import Signer

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ENCRYPTION_EXPIRE_MINUTES = 10





signer = Signer()
class URLEncryptionDecryption():
    def enc(data: any):
        return signer.sign(data)

    def dec(data: any):
        try:
            return signer.unsign(data)
        except Exception as e:
            return None