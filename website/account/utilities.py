import hashlib
import hmac
import base64

def generate_signature(secret_key, message):
    return base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()