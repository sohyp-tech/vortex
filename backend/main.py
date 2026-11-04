from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import users
from routers import posts
from routers import comments

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/", response_class=HTMLResponse)
def home_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Blog API</title>
            <style> * { margin: 0;padding: 0;box-sizing: border-box; } </style>
        </head>
        <body style="display: flex;justify-content: center;align-items: center;flex-direction: column;height: 100%;overflow: hidden;font-family: Arial;">
            <div style="display: flex;justify-content: center;align-items: center;flex-direction: column;width: 290px;height: auto;padding: 10px;border-radius: 10px;border: 0;box-shadow: 0 0 5px #1a1a1a;">
                <h1> This Is Home Page Of Blog API</h1>
            </div>
        </body>
    </html>
    """