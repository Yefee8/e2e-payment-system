# e2e-payment-system - FastAPI & Supabase

## Motto
I always wanted to be better at system, database and back-end design. This is why I'm doing this end to end payment system.
No code written by AI, not even one single line.
I'm not against using AI while writing code or designing a system. At my job I use AI agents a lot. But it's impossible to learn something or develop yourself, if you let AI doing all the work.

## How to run?
Firstly, you need uv, pythonv3.11.9+, docker and node.js/npm.

### Creating the DB
```bash
npm init -y && npm install -D supabase
npx supabase init
npx supabase start
```

This project uses custom Supabase CLI ports (see `supabase/config.toml`) instead of the defaults, to avoid clashing with other local Supabase projects on the same machine:

| Service | Default port | This project |
|---|---|---|
| API | 54321 | 54421 |
| DB | 54322 | 54422 |
| Shadow DB | 54320 | 54420 |
| Pooler | 54329 | 54429 |
| Studio | 54323 | 54423 |
| Mailpit | 54324 | 54424 |
| Analytics | 54327 | 54427 |

After creating the DB, the DB runs on ```postgresql://postgres:postgres@127.0.0.1:54422/postgres``` and the DB address should be in a ~.env file.
So create a .env file in root and add:

```.env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54422/postgres
SUPABASE_URL=http://127.0.0.1:54421
SUPABASE_KEY=<supabase start çıktısındaki Secret key>
```

or you can check the .env.example file.

### First Migration
```bash
npx supabase migration new init_ledger # creates a empty .sql file in supabase/migations/
npx supabase db reset # Re-installs the DB from the start, applies all migrations and seed.sql.
```

### Running the project
```bash
uv run fastapi dev app/main.py # main app
uv run fastapi dev provider_sim/main.py --port 8001 # bank simulator
```

### Docs
Swagger:
```
http://127.0.0.1:8000/docs
```