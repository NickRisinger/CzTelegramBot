import aiohttp
from config.config import Config
from typing import Optional
import time

from utils.sign import sign_data

class APIService:
    def __init__(self):
        self.api_url = Config.API_URL
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None


    async def get_auth_data(self):
        headers = {
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/auth/key",
                headers=headers
            ) as response:
                return await response.json()


    async def get_access_token(self):
        data = await self.get_auth_data() # {uuid, data}
        signed_data = sign_data(data.get("data"))

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{self.api_url}/auth/simpleSignIn",
                    json={
                        "uuid": data.get("uuid"),
                        "data": signed_data,
                    }
            ) as response:
                data = await response.json()
                self._access_token = data.get("token")
                self._token_expires_at = time.time() + 3600

    async def make_request(self, endpoint: str, method: str = "GET", data: dict = None):
        """Выполнение запроса с access_token в заголовках"""
        if not self._access_token:
            await self.get_access_token()

        # Проверяем, не истек ли токен
        if self._token_expires_at and time.time() >= self._token_expires_at:
            self._access_token = None
            await self.get_access_token()

        if not self._access_token:
            raise Exception("Не удалось обновить токен авторизации")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{self.api_url}{endpoint}", json=data, headers=headers) as response:
                return await response.json()

        # async with aiohttp.ClientSession() as session:
        #     async with session.request(
        #             method=method,
        #             url=f"{self.api_url}{endpoint}",
        #             json=data,
        #             headers=headers
        #     ) as response:
        #         data = await response.json()
        #         print('RESPONSE', response)
        #         print('STATUS', response.status)
        #         print('ERROR', await response.text())
        #         return data


    async def get_data(self, code):
        return await self.make_request('/cises/info', method="POST", data=[code])

