from fastapi import HTTPException
from db import supabase
from schemas import TransactionCreate

class LedgerService:
    @staticmethod
    def create_double_entry_transaction(payload: TransactionCreate):
        try:
            # MARK: Creating the transaction row
            tx_response = supabase.table("transactions").insert({
                "description": payload.description,
                "status": "pending"
            }).execute()

            if not tx_response.data:
                raise HTTPException(status_code=400, detail="Transaciton could not be created.")
            
            transaction_id = tx_response.data[0]["id"]

            entries_to_insert = []
            for entry in payload.entries:
                entries_to_insert.append({
                    "transaction_id": transaction_id,
                    "account_id": str(entry.account_id),
                    "amount": entry.amount
                })

            entries_response = supabase.table("entries").insert(entries_to_insert).execute()
            
            if not entries_response.data:
                supabase.table("transactions").update({"status": "failed"}).eq("id", transaction_id).execute()
                raise HTTPException(status_code=400, detail="Entries could not be saved.")

            # MARK: Changing status to completed for triggering the sql function.
            final_tx_response = supabase.table("transactions").update({
                "status": "completed"
            }).eq("id", transaction_id).execute()

            result = final_tx_response.data[0]
            result["entries"] = entries_response.data
            return result

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    @staticmethod
    def get_transaction_by_id(tx_id: str):
        tx_response = supabase.table("transactions").select("*, entries(*)").eq("id", tx_id).execute()
        if not tx_response.data:
            raise HTTPException(status_code=404, detail="İşlem bulunamadı.")
        return tx_response.data[0]