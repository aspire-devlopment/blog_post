from ..models.user_models import UserInfo
from ..services.ilogin_service import ILoginService
from ..utils.jwt_utils import generate_jwt
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import check_password


class LoginService(ILoginService):

    async def login_user(self, email: str, password: str) -> dict:

  

        # Fetch user from DB asynchronously
        try:
            user = await sync_to_async(UserInfo.objects.get)(email=email) # type: ignore
        except UserInfo.DoesNotExist:
            raise ValueError("Invalid email or password")

        # Check password
        if not check_password(password, user.password): # type: ignore
            raise ValueError("Invalid email or password")

        # Generate token
        token = generate_jwt(user.id)

        return {
            "message": "Login successful",
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "token": token
        }