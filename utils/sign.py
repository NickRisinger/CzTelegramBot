import base64
import win32com.client

from config.config import Config


def sign_data(data: str):
    base64_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')

    store = win32com.client.Dispatch("CAPICOM.Store")
    store.Open(2, "My", 0)

    signer = win32com.client.Dispatch("CAdESCOM.CPSigner")
    signer.Certificate = store.Certificates.Item(Config.CERTIFICATE_ID)

    signed_data = win32com.client.Dispatch("CAdESCOM.CadesSignedData")
    signed_data.ContentEncoding = 1
    signed_data.Content = base64_data

    signature = signed_data.SignCades(signer, 1, False)  # False = attached

    signature_cleaned = signature.replace('\r', '').replace('\n', '')

    with open("./data/signature.txt", "w", encoding="utf-8") as f:
        f.write(signature_cleaned)

    return signature_cleaned
