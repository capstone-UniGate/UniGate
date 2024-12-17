set dotenv-load

venv := if os_family() == "windows" { ".venv/Scripts" } else { ".venv/bin" }
python := if os_family() == "windows" { "/python.exe" } else { "/python3" }

backend_venv := "backend" / venv
backend_python := backend_venv + python

burndown_venv := "scripts/burndown" / venv
burndown_python := burndown_venv + python

frontend_venv := "frontend" / venv
frontend_python := frontend_venv + python

@_default:
    just --list


# docker commands

docker-up:
    docker compose up --watch --build

docker-stop:
    docker compose stop

docker-down:
    docker compose down -v

reset-database:
    docker compose exec postgres-unigate psql -U $POSTGRES_USER -d $POSTGRES_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"
    docker compose exec postgres-unigate psql -U $POSTGRES_USER -d $UNIGATE_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"
    docker compose exec postgres-unigate psql -U $POSTGRES_USER -d $AUTH_DB -c "DO \$\$ BEGIN EXECUTE 'DROP SCHEMA public CASCADE'; EXECUTE 'CREATE SCHEMA public'; END \$\$;"

init-database-docker: reset-database
    docker compose exec --workdir /app/alembic_unigate backend-unigate alembic upgrade head
    docker compose exec --workdir /app/alembic_auth backend-unigate alembic upgrade head

seed-real-docker:
    docker compose exec backend-unigate python3 seeders/real.py

backend-only-test-docker:
    docker compose exec backend-unigate pytest tests/

backend-test-docker: init-database-docker seed-real-docker backend-only-test-docker

backend-only-test-single-docker FILE:
    docker compose exec backend-unigate pytest tests/routes/{{ FILE }}


init-database: reset-database
    cd backend/alembic_unigate && ../../{{ backend_venv }}/alembic upgrade head
    cd backend/alembic_auth && ../../{{ backend_venv }}/alembic upgrade head

backend-test-single-docker FILE: init-database-docker seed-real-docker (backend-only-test-single-docker FILE)

frontend-only-test-docker:
    docker compose exec frontend-unigate pytest tests/

frontend-test-docker: init-database-docker seed-real-docker frontend-only-test-docker

frontend-only-test-single-docker FILE:
    docker compose exec frontend-unigate pytest tests/test_cases/{{ FILE }}

frontend-test-single-docker FILE: init-database-docker seed-real-docker (frontend-only-test-single-docker FILE)

# backend commands

backend-deps:
    cd backend && uv sync

pre-commit: backend-deps
    {{ backend_venv }}/pre-commit run --all-files

backend-fix: backend-deps
    {{ backend_venv }}/ruff check backend --config backend/pyproject.toml
    {{ backend_venv }}/ruff format backend --config backend/pyproject.toml

backend-python FILE *ARGS: backend-deps
    {{ backend_python }} backend/{{ FILE }} {{ ARGS }}

seed-real:
    {{ backend_python }} backend/seeders/real.py

seed-fake:
    {{ backend_python }} backend/seeders/fake.py

backend-dev: backend-deps
    {{ backend_venv }}/fastapi dev backend/unigate/main.py

backend-only-test:
    cd backend && ../{{ backend_venv }}/pytest tests/

backend-test: backend-deps init-database seed-real backend-only-test

backend-only-test-single FILE:
    cd backend && ../{{ backend_venv }}/pytest tests/routes/{{ FILE }}

backend-test-single FILE: init-database seed-real (backend-only-test-single FILE)

# frontend commands

frontend-deps:
    cd frontend && pnpm install
    cd frontend && uv sync

frontend-fix:
    cd frontend && npx prettier . --write
    cd frontend && npx eslint --fix

frontend-dev: frontend-deps
    cd frontend && pnpm run dev

frontend-prod: frontend-deps
    cd frontend && pnpm run build && pnpm run preview

frontend-only-test:
    cd frontend && ../{{ frontend_venv }}/pytest tests/

frontend-test: init-database seed-real frontend-only-test

frontend-only-test-single FILE:
    cd frontend && ../{{ frontend_venv }}/pytest tests/test_cases/{{ FILE }}

frontend-test-single FILE: init-database seed-real (frontend-only-test-single FILE)

# burndown commands

burndown-deps:
    cd scripts/burndown && uv sync

burndown-fix: burndown-deps
    {{ burndown_venv }}/ruff check scripts/burndown --config scripts/burndown/pyproject.toml
    {{ burndown_venv }}/ruff format scripts/burndown --config scripts/burndown/pyproject.toml

burndown *ARGS: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py {{ ARGS }}

burndown-sprint1: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py --start-date 2024-11-10 --end-date 2024-11-27 --milestone eos1 --org capstone-UniGate --project-number 5

burndown-sprint2: burndown-deps
    {{ burndown_python }} scripts/burndown/main.py --start-date 2024-12-02 --end-date 2024-12-19 --milestone eos2 --org capstone-UniGate --project-number 5
