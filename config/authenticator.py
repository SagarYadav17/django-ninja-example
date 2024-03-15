from ninja.security import HttpBearer
from ninja.errors import HttpError
from authentication.models import User
import jwt


class AuthBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HttpError(403, "Invalid token")

        request.user = await User.objects.aget(
            id=payload["id"],
            email=payload["email"],
        )

        return token
