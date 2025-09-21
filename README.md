# Blog Integration with PostgreSQL

This project has been updated to integrate with a PostgreSQL database for displaying blog posts. The blog functionality is read-only and does not include features for adding, editing, or deleting posts through the web interface.

## Database Schema

The blog posts are stored in a Supabase PostgreSQL table with the following structure:

```sql
CREATE TABLE blog (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data JSONB NOT NULL
);
```

The `data` field contains a JSONB object with:
- `text`: The blog post content (string)
- `tags`: An array of tags (string array)

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Supabase Database**:
   - Ensure you have a Supabase project with a `blog` table
   - Optionally run the setup script in your Supabase SQL editor: copy content from `setup_database.sql`

3. **Configure Environment Variables**:
   - Update the `.env` file with your Supabase connection details:
     ```
     DB_HOST=aws-1-us-east-2.pooler.supabase.com
     DB_PORT=6543
     DB_NAME=postgres
     DB_USER=postgres.ijlsfqvzqbiytnnsxwrc
     DB_PASSWORD=your_actual_supabase_password
     ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Features

- **Read-only blog display**: View blog posts stored in PostgreSQL
- **Tag filtering**: Filter posts by specific tags using `?tag=tagname`
- **Search functionality**: Search posts by content using `?search=term`
- **Responsive design**: Mobile-friendly interface
- **Dark/Light theme**: Toggle theme support

## API Endpoints

- `GET /blog`: List all blog posts (supports `?tag=` and `?search=` query parameters)
- `GET /blog/{post_id}`: View a specific blog post
- `GET /section/scribblings`: View blog posts within the main site layout

## Data Model

### BlogPost
```python
{
    "id": int,
    "created_at": datetime,
    "data": {
        "text": str,
        "tags": List[str]
    }
}
```

### Example JSONB Data
```json
{
    "text": "This is my blog post content...",
    "tags": ["python", "fastapi", "web-development"]
}
```

## Adding Blog Posts

Since this is a read-only interface, blog posts need to be added directly to the Supabase database:

```sql
INSERT INTO blog (data) VALUES 
('{"text": "Your blog post content here", "tags": ["tag1", "tag2"]}');
```

The application will automatically pick up new posts and display them in chronological order (newest first).