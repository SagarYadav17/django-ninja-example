from typing import List
from contextlib import suppress
from asgiref.sync import sync_to_async

from ninja import Router
from ninja.responses import codes_4xx, codes_2xx
from config.authenticator import AuthBearer

# schemas
from authentication.schema import LoginUserSchema, RegisterUserSchema, UsersOut

# models
from authentication.models import User


router = Router()


default_response = {codes_2xx: dict, codes_4xx: dict}


@router.post("/register", response=default_response)
def register_user(request, data: RegisterUserSchema):
    User.objects.create_user(**data.dict())
    return {"message": "User created"}


@router.post("/login", response=default_response)
async def login(request, data: LoginUserSchema):
    with suppress(User.DoesNotExist):
        user = await User.objects.aget(email=data.email)
        if user.check_password(data.password):
            return 200, {"token": user.token}

    return 401, {"message": "Invalid credentials"}


@router.get("/users", auth=AuthBearer(), response=List[UsersOut])
async def list_users(request):
    users = await sync_to_async(list)(User.objects.all())
    return users


@router.get("/user/me", auth=AuthBearer(), response=UsersOut)
async def get_me(request):
    return request.user
