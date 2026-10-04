from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import ledger
from routers import account

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== [E2E Payment System] is starting... ===")
    yield
    print("=== [E2E Payment System] is stopping... ===")

app = FastAPI(
    title="E2E Payment System API",
    description="e2e payment system",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ledger.router)
app.include_router(account.router)

@app.get("/", tags=["Root"])
def root_check():
    return {"status": "healthy", "service": "e2e-payment-system"}