from fastapi import APIRouter, Depends
from schemas import TransactionCreate, TransactionResponse
from services.ledger.ledgerService import LedgerService

router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"]
)

@router.post("/create", response_model=TransactionResponse, status_code=201)
def create_transaction(payload: TransactionCreate):
    return LedgerService.create_double_entry_transaction(payload)

@router.get("/transactions/{tx_id}", response_model=TransactionResponse)
def get_transaction(tx_id: str):
    return LedgerService.get_transaction_by_id(tx_id)
