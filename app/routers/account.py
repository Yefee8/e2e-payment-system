from fastapi import APIRouter, Depends
from schemas import AccountCreate, AccountResponse
from services.account.accountService import AccountService

router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@router.post("/create", response_model=AccountResponse, status_code=201)
def create_transaction(payload: AccountCreate):
    return AccountService.create_account(payload)

