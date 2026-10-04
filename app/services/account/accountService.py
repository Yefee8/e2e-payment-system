from fastapi import HTTPException
from db import supabase
from schemas import AccountCreate

class AccountService:
    @staticmethod
    def create_account(payload: AccountCreate):
        try:
            tx_response = supabase.table("accounts").insert({
                            "currency": payload.currency,
                            "type": 'user_wallet',
                            "balance": 0,
                        }).execute()
            if not tx_response.data:
                    raise HTTPException(status_code=400, detail="Account could not be created.")
            return {
                "currency": tx_response.data[0]["currency"],
                "type": "user_wallet",
                "id": tx_response.data[0]["id"],
                "created_at": tx_response.data[0]["created_at"],
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")