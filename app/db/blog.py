import os
import psycopg2
import psycopg2.extras
from typing import List, Optional
import json
from datetime import datetime
from app.models.blog import BlogPost, BlogPostData
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BlogDatabase:
    @staticmethod
    def _get_connection():
        """Create a database connection using environment variables"""
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', 5432),
                database=os.getenv('DB_NAME', 'blog_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'password')
            )
            return conn
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return None

    @staticmethod
    def get_all_posts() -> List[BlogPost]:
        """Fetch all blog posts from PostgreSQL database"""
        conn = BlogDatabase._get_connection()
        if not conn:
            return []

        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, created_at, data 
                    FROM blog 
                    ORDER BY created_at DESC
                """)
                rows = cur.fetchall()
                
                posts = []
                for row in rows:
                    # Convert row to BlogPost object
                    data_dict = row['data'] if isinstance(row['data'], dict) else json.loads(row['data'])
                    blog_data = BlogPostData(**data_dict)
                    
                    post = BlogPost(
                        id=row['id'],
                        created_at=row['created_at'],
                        data=blog_data
                    )
                    posts.append(post)
                
                return posts
        except psycopg2.Error as e:
            print(f"Error fetching posts: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_post_by_id(post_id: int) -> Optional[BlogPost]:
        """Fetch a specific blog post by ID from PostgreSQL database"""
        conn = BlogDatabase._get_connection()
        if not conn:
            return None

        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, created_at, data 
                    FROM blog 
                    WHERE id = %s
                """, (post_id,))
                row = cur.fetchone()
                
                if row:
                    # Convert row to BlogPost object
                    data_dict = row['data'] if isinstance(row['data'], dict) else json.loads(row['data'])
                    blog_data = BlogPostData(**data_dict)
                    
                    return BlogPost(
                        id=row['id'],
                        created_at=row['created_at'],
                        data=blog_data
                    )
                return None
        except psycopg2.Error as e:
            print(f"Error fetching post by ID {post_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_posts_by_tag(tag: str) -> List[BlogPost]:
        """Fetch blog posts that contain a specific tag"""
        conn = BlogDatabase._get_connection()
        if not conn:
            return []

        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, created_at, data 
                    FROM blog 
                    WHERE data->'tags' @> %s
                    ORDER BY created_at DESC
                """, (json.dumps([tag]),))
                rows = cur.fetchall()
                
                posts = []
                for row in rows:
                    # Convert row to BlogPost object
                    data_dict = row['data'] if isinstance(row['data'], dict) else json.loads(row['data'])
                    blog_data = BlogPostData(**data_dict)
                    
                    post = BlogPost(
                        id=row['id'],
                        created_at=row['created_at'],
                        data=blog_data
                    )
                    posts.append(post)
                
                return posts
        except psycopg2.Error as e:
            print(f"Error fetching posts by tag {tag}: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def search_posts(search_term: str) -> List[BlogPost]:
        """Search blog posts by text content"""
        conn = BlogDatabase._get_connection()
        if not conn:
            return []

        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, created_at, data 
                    FROM blog 
                    WHERE data->>'text' ILIKE %s
                    ORDER BY created_at DESC
                """, (f'%{search_term}%',))
                rows = cur.fetchall()
                
                posts = []
                for row in rows:
                    # Convert row to BlogPost object
                    data_dict = row['data'] if isinstance(row['data'], dict) else json.loads(row['data'])
                    blog_data = BlogPostData(**data_dict)
                    
                    post = BlogPost(
                        id=row['id'],
                        created_at=row['created_at'],
                        data=blog_data
                    )
                    posts.append(post)
                
                return posts
        except psycopg2.Error as e:
            print(f"Error searching posts: {e}")
            return []
        finally:
            conn.close()

    # Note: Removed create_post, update_post, and delete_post methods 
    # as requested - only read operations are implemented