from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..models.user_models import UserInfo

class IUserService(ABC):
    @abstractmethod
    async def list_users(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserInfo]:
        pass

    @abstractmethod
    async def create_user(self, data: dict) -> UserInfo:
        pass

    @abstractmethod
    async def update_user(self, user: UserInfo, data: dict) -> UserInfo:
        pass

    @abstractmethod
    async def delete_user(self, user: UserInfo) -> None:
        pass
    
 