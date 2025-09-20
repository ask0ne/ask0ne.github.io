from typing import List, Optional
from app.models.blog import BlogPost

# In-memory database (replace with a real database in production)
blog_posts = [
    {
        "id": 1,
        "title": "Building with FastAPI and HTMX",
        "content": "Recently I've been exploring the combination of FastAPI with HTMX for rapid web development. The experience has been quite refreshing - being able to build interactive UIs without writing JavaScript feels almost magical.",
        "date": "2025-09-15",
        "slug": "fastapi-htmx-experience"
    },
    {
        "id": 2,
        "title": "Why I Love Python Backend Development",
        "content": "Python has always been my go-to for backend development. The ecosystem is rich, the syntax is clean, and the community is amazing.",
        "date": "2025-09-10",
        "slug": "python-backend-love"
    }
]

class BlogDatabase:
    @staticmethod
    def get_all_posts() -> List[dict]:
        return blog_posts

    @staticmethod
    def get_post_by_id(post_id: int) -> Optional[dict]:
        return next((post for post in blog_posts if post["id"] == post_id), None)

    @staticmethod
    def create_post(post: BlogPost) -> dict:
        new_id = max([p["id"] for p in blog_posts]) + 1 if blog_posts else 1
        new_post = {
            "id": new_id,
            **post.dict(),
        }
        blog_posts.append(new_post)
        return new_post

    @staticmethod
    def update_post(post_id: int, post_update: dict) -> Optional[dict]:
        for post in blog_posts:
            if post["id"] == post_id:
                post.update({k: v for k, v in post_update.items() if v is not None})
                return post
        return None

    @staticmethod
    def delete_post(post_id: int) -> bool:
        initial_length = len(blog_posts)
        blog_posts[:] = [p for p in blog_posts if p["id"] != post_id]
        return len(blog_posts) < initial_length