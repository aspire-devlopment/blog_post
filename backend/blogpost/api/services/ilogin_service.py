from abc import ABC, abstractmethod
from typing import  Optional

from ..models.user_models import UserInfo

class ILoginService(ABC):
   

    @abstractmethod
    async def login_user(self, email: str, password: str) -> Optional[UserInfo]:
        pass

   
 