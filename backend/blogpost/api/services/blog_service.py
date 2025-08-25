# api/services/blogpost_service.py
import json
import os
import urllib.request as request
from venv import logger
from django.conf import settings
from asgiref.sync import sync_to_async
from ..models.blog_post_models import BlogPost
from ..models.user_models import UserInfo
from .iblog_service import IBlogPostService

class BlogPostService(IBlogPostService):

    async def list_posts(self, author_id: int):
        posts = await sync_to_async(list)(
        BlogPost.objects.filter(author_id=author_id)
        .select_related("author")
        .values(
            "id", "title", "content", "image", "author__id", "created_at"
        )
    )
    
    
    # Fix image URLs
        for post in posts:
            if post["image"]:
                post["image"] = settings.MEDIA_URL + post["image"]
        
        return posts


    async def list_all_posts(self):
        posts = await sync_to_async(list)(
            BlogPost.objects.select_related("author").values(
                "id", "title", "content", "image", "author__id", "created_at"
            )
        )
    
        # Fix image URLs
        for post in posts:
            if post["image"]:
                post["image"] = settings.MEDIA_URL + post["image"]
        
        return posts


    def get_post(self, post_id: int):
        try:
            post =  (BlogPost.objects.get)(id=post_id)
            return {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "image": f"{settings.MEDIA_URL}{post.image}" if post.image else None,
                "author_id": post.author.id,
                "created_at": post.created_at
            }
        except BlogPost.DoesNotExist:
            return None

    async def create_post(self, data: dict, files: dict, author_id: int):
        author = await sync_to_async(UserInfo.objects.get)(id=author_id)

        image_url = None
        if "image" in files:
            image = files["image"]
            image_path = os.path.join(settings.MEDIA_ROOT, "blog_images", image.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, "wb+") as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_url = f"blog_images/{image.name}"

        post = BlogPost(
            title=data.get("title","").strip(),
            content=data.get("content","").strip(),
            author= author,
            image=image_url
        )
        await sync_to_async(post.save)()
        return post

    def update_post(self, post_id: int, data: dict, files: dict):
        try:
            post = BlogPost.objects.get(id=post_id)

            # Debug logging
            logger.info(f"Update data received: {data}")
            logger.info(f"Update files received: {list(files.keys()) if files else 'None'}")

            # Update fields
            if "title" in data and data["title"]:
                post.title = data["title"].strip()

            if "content" in data and data["content"]:
                post.content = data["content"].strip()

            # Handle image upload
            if files and "image" in files:
                image = files["image"]
                image_path = os.path.join(settings.MEDIA_ROOT, "blog_images", image.name)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, "wb+") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                post.image = f"blog_images/{image.name}"  # <--- Assign to post.image

            post.save()
            return post

        except BlogPost.DoesNotExist:
            raise ValueError("Post not found")
        except Exception as e:
            logger.error(f"Error updating post {post_id}: {str(e)}")
            raise


        
    def delete_post(self, post_id: int):
            post =  (BlogPost.objects.get)(id=post_id)
            (post.delete)()
