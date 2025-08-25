# api/services/async_user_service.py
from typing import Dict, List, Optional

from ..models.user_models import UserInfo
from asgiref.sync import sync_to_async

from .iuser_service import IUserService

class UserService(IUserService):
    """Async implementation using sync_to_async for ORM operations"""

    async def list_users(self) -> List[Dict]:
        return await sync_to_async(list)(
            UserInfo.objects.values("id", "first_name", "last_name", "phone_number", "email")
        )

    async def get_user(self, user_id: int) -> Optional[UserInfo]:
        return await sync_to_async(UserInfo.objects.filter(id=user_id).first)()

    async def create_user(self, data: dict) -> UserInfo:
        email_exists = await sync_to_async(UserInfo.objects.filter(email=data["email"]).exists)()
        phone_exists = await sync_to_async(UserInfo.objects.filter(phone_number=data["phone_number"]).exists)()
        if email_exists:
            raise ValueError("Email already registered")
        if phone_exists:
            raise ValueError("Phone number already registered")
        return await sync_to_async(UserInfo.objects.create)(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            password=data.get("password")  # hashed in model
        )

    async def update_user(self, user: UserInfo, data: dict) -> UserInfo:
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.email = data.get("email", user.email)
        if "password" in data:
            user.password = data["password"]
        await sync_to_async(user.save)()
        return user

    async def delete_user(self, user: UserInfo) -> None:
        await sync_to_async(user.delete)()
