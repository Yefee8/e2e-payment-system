from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, List

# MARK: Accounts
class AccountCreate(BaseModel):
    currency: str = Field(default="TRY", min_length=3, max_length=3)
    type: str = Field(default="user_wallet", description="user_wallet, external_world, comission_revenue")

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        return v.upper()

class AccountResponse(AccountCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# MARK: Entries
class EntryCreate(BaseModel):
    account_id: UUID
    amount: int = Field(..., description="Girişler (borç) pozitif, çıkışlar (alacak) negatif olmalıdır.")

    @field_validator("amount")
    @classmethod
    def amount_cannot_be_zero(cls, v: int) -> int:
        if v == 0:
            raise ValueError("Miktar (amount) 0 olamaz.")
        return v

class EntryResponse(EntryCreate):
    id: UUID
    transaction_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# MARK: Transactions
class TransactionCreate(BaseModel):
    description: Optional[str] = None
    entries: List[EntryCreate] = Field(..., min_length=2, description="Bir işlem en az 2 hesabı etkilemelidir.")

    # FastAPI seviyesinde ilk güvenlik duvarı: Toplam 0 mı?
    @field_validator("entries")
    @classmethod
    def validate_entries_balance(cls, entries: List[EntryCreate]) -> List[EntryCreate]:
        total_balance = sum(entry.amount for entry in entries)
        if total_balance != 0:
            raise ValueError(f"Gönderilen hareketlerin (entries) toplamı 0 olmalıdır. Mevcut toplam: {total_balance}")
        return entries

class TransactionResponse(BaseModel):
    id: UUID
    description: Optional[str]
    status: str
    created_at: datetime
    entries: Optional[List[EntryResponse]] = None

    class Config:
        from_attributes = True
