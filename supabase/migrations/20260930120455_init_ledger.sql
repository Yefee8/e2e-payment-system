CREATE TABLE accounts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
    balance BIGINT NOT NULL DEFAULT 0 CHECK (balance > -1),
    currency VARCHAR(3) NOT NULL DEFAULT 'TRY',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    type VARCHAR(30) NOT NULL DEFAULT 'user_wallet' -- user_wallet, external_world, comission_revenue
);

CREATE TABLE transactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, completed, failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE entries(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
    transaction_id UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    amount BIGINT NOT NULL CHECK (amount <> 0), -- Entries are positive, exits are negative.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_entries_transaction ON entries(transaction_id);
CREATE INDEX idx_entries_account ON entries(account_id);

CREATE OR REPLACE FUNCTION verify_and_update_ledger() 
RETURNS TRIGGER AS $$
DECLARE
    entry_list JSONB;        -- All rows going to be contained in this entry_list
    total_amount BIGINT := 0;
    entry_count INTEGER := 0 ;-- Row count
    item JSONB;
BEGIN
    IF NEW.status = 'completed' THEN
        SELECT 
            jsonb_agg(jsonb_build_object('account_id', account_id, 'amount', amount)),
            COALESCE(SUM(amount), 0),
            COUNT(*)
        INTO entry_list, total_amount, entry_count
        FROM entries 
        WHERE transaction_id = NEW.id;

        IF entry_count = 0 OR entry_list IS NULL THEN
            RAISE EXCEPTION 'TRANSACTION ERROR: Transaction % has no entries.', NEW.id;
        END IF;

        IF total_amount <> 0 THEN
            RAISE EXCEPTION 'TRANSACTION ERROR: Entries do not balance to 0. Sum: %', total_amount;
        END IF;

        FOR item IN SELECT * FROM jsonb_array_elements(entry_list)
        LOOP
            UPDATE accounts 
            SET balance = balance + (item->>'amount')::BIGINT
            WHERE id = (item->>'account_id')::UUID;
        END LOOP;

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verify_and_update
BEFORE INSERT OR UPDATE ON transactions
FOR EACH ROW
EXECUTE FUNCTION verify_and_update_ledger();