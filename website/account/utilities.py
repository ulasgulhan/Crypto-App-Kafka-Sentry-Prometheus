import hashlib
import hmac
import base64
import json



def decode(data):
    return  base64.b64decode(data).decode()


def generate_signature(secret_key, message):
    return base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()


def bybit_signature(secret_key, message):
    hash = hmac.new(bytes(secret_key, "utf-8"), message.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    return signature


def okx_signature(secret_key, message):
    hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), digestmod='sha256')
    signature = hash.digest()
    return base64.b64encode(signature)


def kafka_producer_serializer(message):
    return json.dumps(message).encode('utf-8')


