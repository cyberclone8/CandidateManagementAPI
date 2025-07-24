from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, candidates, applications

app = FastAPI(title="Candidate Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(candidates.router, tags=["Candidates"])
app.include_router(applications.router, tags=["Applications"])
