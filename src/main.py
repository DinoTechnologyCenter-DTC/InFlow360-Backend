from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import and include routers
from src.routes import africastalking, auth, invoice

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to InFlow360 API!"}


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(invoice.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(
    africastalking.router, prefix="/africastalking", tags=["AfricasTalking"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
