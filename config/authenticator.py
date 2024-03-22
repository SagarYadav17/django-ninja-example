from ninja.security import HttpBearer
from ninja.errors import HttpError
import jwt


class AuthBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HttpError(403, "Invalid token")

        request.user.id = payload["id"]

        return token
