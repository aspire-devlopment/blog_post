# api/views/blogpostViews.py
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..services.blog_service import BlogPostService
from ..utils.request_logger import RequestLogger
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

blog_service = BlogPostService()

@csrf_exempt
async def blog_list(request):
    req_logger = RequestLogger()
    try:
        if request.method == "GET":
            author_id = request.user.id                          
            posts = await blog_service.list_posts(author_id)

            return JsonResponse(posts, safe=False)

        if request.method == "POST":
            data = request.POST.dict()
            files = request.FILES
            author_id = request.user.id 
            post = await blog_service.create_post(data, files, author_id)
            logger.info(f"Post successful in {req_logger.duration_ms():.2f}ms")
            return JsonResponse({"message": "Post created", "id": post.id})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        logger.error(f"ERROR {request.method} {request.path} after {req_logger.duration_ms():.2f}ms: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
async def blog_list_all(request):
    req_logger = RequestLogger()
    try:
        if request.method == "GET":
            posts = await blog_service.list_all_posts()
            return JsonResponse(posts, safe=False)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        logger.error(f"ERROR {request.method} {request.path} after {req_logger.duration_ms():.2f}ms: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def blog_detail(request, id):
    req_logger = RequestLogger()
    try:
        post = blog_service.get_post(id)
        if not post:
            return JsonResponse({"error": "Post not found"}, status=404)

        # GET → return post
        if request.method == "GET":
            return JsonResponse(post)

        # UPDATE → PUT, PATCH, or POST
        if request.method in ["PUT", "PATCH", "POST"]:
            if request.content_type and request.content_type.startswith("application/json"):
                data = json.loads(request.body.decode("utf-8"))
                files = None
            else:
                data = request.POST.dict()
                files = request.FILES if request.FILES else None

            logger.info(f"Update data received: {data}")
            logger.info(f"Update files received: {files}")

            updated_post = blog_service.update_post(id, data, files)
            logger.info(f"Post update successful in {req_logger.duration_ms():.2f}ms")
            return JsonResponse({"message": "Post updated", "id": updated_post.id})

        # DELETE
        if request.method == "DELETE":
            blog_service.delete_post(id)
            logger.info(f"Post deleted successful in {req_logger.duration_ms():.2f}ms")
            return JsonResponse({"message": "Post deleted"})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(
            f"ERROR {request.method} {request.path} after {req_logger.duration_ms():.2f}ms: {str(e)}",
            exc_info=True,
        )
        return JsonResponse({"error": str(e)}, status=500)
