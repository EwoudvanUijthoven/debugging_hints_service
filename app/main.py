from fastapi import FastAPI
from app.routers import example_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Include routers for different endpoints
app.include_router(example_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - use this for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (e.g., Authorization)
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}