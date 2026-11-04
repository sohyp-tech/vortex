# Vortex Backend

A lightweight blog-style REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**. The backend exposes endpoints for managing users, posts, and comments, and includes interactive API documentation through Swagger UI.

## Features

- User registration, lookup, profile updates, and deletion
- Create, list, edit, and delete posts
- Create, list, edit, and delete comments
- Request validation with Pydantic
- Password hashing with Passlib
- Separate SQLite databases for users, posts, and comments
- Interactive OpenAPI documentation

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Passlib (`pbkdf2_sha256`)

## Project structure

```text
vortex/
├── backend/
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schema.py
│   ├── routers/
│   │   ├── comments.py
│   │   ├── posts.py
│   │   └── users.py
│   └── main.py
└── README.md
```

## Getting started

### Prerequisites

- Python 3
- `pip`

### Install dependencies

From the repository root, create and activate a virtual environment, then install the backend packages:

```bash
python -m venv .venv
```

 macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install fastapi uvicorn sqlalchemy pydantic passlib
```

### Run the API

Start the server from the `backend` directory so the project imports resolve correctly:

```bash
cd backend
uvicorn main:app --reload
```

By default, the API is available at `http://127.0.0.1:8000`.

> **Current code status:** `backend/routers/posts.py` contains missing commas in dictionary literals. Python will raise a syntax error while importing the posts router, preventing the application from starting. Fix those syntax errors before running the server.

## API documentation

When the server is running, visit:

- Swagger UI: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- ReDoc: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)
- OpenAPI schema: [`http://127.0.0.1:8000/openapi.json`](http://127.0.0.1:8000/openapi.json)

The API root (`/`) serves a simple HTML welcome page.

## Endpoints

All paths below are relative to `http://127.0.0.1:8000`. Interactive docs show request schemas and parameters.

### Users

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/users/add_user` | Create a user (`user_name`, `user_age`, `user_password`) |
| `GET` | `/users/get_user/{name}/{age}` | Find a user by name and age |
| `PUT` | `/users/update_user/{user_name}/{user_password}/update_age/{new_age}/update_name/{new_name}` | Update a user's name and age after password verification |
| `DELETE` | `/users/delete_user/{user_name}/{user_age}?password={password}` | Delete a user after password verification |

### Posts

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/posts/add_post` | Create a post (`poster_name`, `post_content`) |
| `GET` | `/posts/get_posts` | List posts |
| `GET` | `/posts/get_user_posts/{poster_name}` | List posts by author |
| `PUT` | `/posts/edit_post/{poster_name}/{post_id}?new_content={content}` | Edit a post |
| `PUT` | `/posts/remove_post/{poster_name}/{post_id}?new_content={content}` | Delete a post (the current handler also declares `new_content`) |

### Comments

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/comments/add_comment` | Create a comment (`commenter_name`, `comment_content`) |
| `GET` | `/comments/get_comments` | List comments |
| `PUT` | `/comments/edit_comment/{commenter_name}/{comment_id}?new_content={content}` | Edit a comment |
| `DELETE` | `/comments/remove_comment/{commenter_name}/{comment_id}` | Delete a comment |

### Example request

Create a post:

```bash
curl -X POST "http://127.0.0.1:8000/posts/add_post" \
  -H "Content-Type: application/json" \
  -d '{"poster_name":"Alex","post_content":"Hello from Vortex!"}'
```

## Database

The application uses SQLite and creates the following database files in the working directory when the corresponding routers initialize:

- `users.db`
- `posts.db`
- `comments.db`

These local database files are excluded from Git by `.gitignore`.

## Security and production notes

This project is currently a development-stage example. Before deploying it publicly:

- Restrict CORS to trusted origins instead of allowing every origin.
- Avoid sending passwords or sensitive values in URL paths or query strings; URLs can be recorded in logs and browser history.
- Add proper authentication and authorization for actions on posts and comments.
- Configure production-grade database management, secret handling, and error responses.

## License

No license is currently specified. Add a `LICENSE` file before redistributing this project.
