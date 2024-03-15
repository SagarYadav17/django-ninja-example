from typing import List
from asgiref.sync import sync_to_async

from ninja import NinjaAPI
from config.authenticator import AuthBearer

# schemas
from authentication.schema import LoginUserSchema, RegisterUserSchema, UsersOut

# models
from authentication.models import User


api = NinjaAPI(title="Authentication API", version="1.0.0")


@api.post("/register")
def create_user(request, data: RegisterUserSchema):
    User.objects.create_user(**data.dict())
    return data.dict()


@api.post("/login")
async def login(request, data: LoginUserSchema):
    user = await User.objects.aget(email=data.email)

    if user.check_password(data.password):
        return {"token": user.token}
    else:
        return "Invalid credentials"


@api.get("/users", auth=AuthBearer(), response=List[UsersOut])
async def list_users(request):
    print(request.user)
    users = await sync_to_async(list)(User.objects.all())
    return users


@api.get("/user/me", auth=AuthBearer(), response=UsersOut)
async def get_me(request):
    return request.user
