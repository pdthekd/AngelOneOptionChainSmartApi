import pyotp
from SmartApi.smartConnect import SmartConnect
from typing import Optional

class User:
    def __init__(self, api_key: str, client_code: str, mpin: str, otp_secret: str) -> None:
        self.__API_KEY = api_key
        self.__ID = client_code
        self.__MPIN = mpin
        self.__OTP_SECRET = otp_secret

        self.__JWT = None
        self.__FEED = None
        self.__session = None
        self.__obj = SmartConnect(api_key=api_key)

    """
    Getters
    """
    @property
    def client_code(self) -> str:
        return self.__ID

    @property
    def mpin(self) -> str:
        return self.__MPIN

    @property
    def totp(self) -> str:
        return pyotp.TOTP(self.__OTP_SECRET).now()

    @property
    def jwt(self) -> Optional[str]:
        return self.__JWT

    @property
    def feed(self) -> Optional[str]:
        return self.__FEED

    @property
    def session(self) -> Optional[dict]:
        return self.__session

    @property
    def connection(self):
        return self.__obj

    """
    Methods
    """
    def login(self) -> bool:
        try:
            self.__session = self.__obj.generateSession(self.__ID, self.__MPIN, self.totp)
            self.__JWT = self.__session["data"]["jwtToken"]
            self.__FEED = self.__session["data"]["feedToken"]
            print("✅ Login successful.")
            return True
        except Exception as e:
            print("❌ Login failed:", e)
            return False

    def logout(self):
        try:
            self.__obj.terminateSession(self.__ID)
            print("👋 Logged out.")
        except Exception as e:
            print("⚠️ Logout failed:", e)
