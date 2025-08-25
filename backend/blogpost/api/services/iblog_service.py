# api/services/IBlogPostService.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class IBlogPostService(ABC):

    @abstractmethod
    async def list_posts(self,author_id:int) -> list[Dict[str, Any]]:
        """Return  blog posts"""
        pass

    @abstractmethod
    async def list_all_posts(self) -> list[Dict[str, Any]]:
        """Return all blog posts"""
        pass

    @abstractmethod
    async def get_post(self, post_id: int) -> Dict[str, Any] | None:
        """Return a single blog post"""
        pass

    @abstractmethod
    async def create_post(self, data: dict, files: dict, author_id: int) -> Any:
        """Create a new blog post"""
        pass

    @abstractmethod
    async def update_post(self, id: int, data: dict, files: dict) -> Any:
        """Update an existing blog post"""
        pass

    @abstractmethod
    async def delete_post(self, post_id: int) -> None:
        """Delete a blog post"""
        pass
