from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import url_scanner, file_scanner, email_scanner

app = FastAPI(
    title="Cybersecurity Analyzer API",
    description="API to scan URLs, files, and emails to detect malware.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React frontend
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(url_scanner.router, prefix="/scan/url", tags=["URL Scanner"])
app.include_router(file_scanner.router, prefix="/scan/file", tags=["File Scanner"])
app.include_router(email_scanner.router, prefix="/scan/email", tags=["Email Scanner"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Cybersecurity Analyzer API 🚀"}
