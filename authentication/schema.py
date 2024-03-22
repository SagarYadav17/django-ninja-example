from ninja import ModelSchema, Schema
from pydantic import EmailStr, Field, model_validator
from authentication.models import User
from uuid import UUID


class RegisterUserSchema(ModelSchema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100, frozen=True)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    @model_validator(mode="after")
    def validate_email(self):
        email = self.email
        if User.objects.filter(email=email).exists():
            raise ValueError("User with this email already exists.")

        return self


class UsersOut(Schema):
    id: UUID
    email: EmailStr
    name: str | None
    is_superuser: bool
    is_staff: bool


class LoginUserSchema(Schema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100, frozen=True)
