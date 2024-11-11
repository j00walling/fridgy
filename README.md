# Fridgy

Fridgy is a Refrigerator Assistant Chatbot that helps users manage their refrigerator inventory and provides recipe suggestions based on the items available. The UI is built using the Next.js framework with React, and the backend is developed using FastAPI, Open AI for LLM and Embedding models and Pinecone for Vector DB and RAG.

## Prerequisites

- **Node.js**: Install [Node.js](https://nodejs.org/) (version 20.12.0 or higher).
- **pnpm**: Install [pnpm](https://pnpm.io/) globally if you haven't already:

  ```bash
  npm install -g pnpm
  ```

## Setting Up the Frontend

Follow these steps to set up the project's UI locally

1. Clone the Repository

```bash
git clone git@github.com:j00walling/fridgy.git
cd fridgy/fridgy-ui
```

2. Install Dependencies

```bash
pnpm install
```

3. Run the UI Server

```bash
pnpm run dev
```

4. Open Your Browser

Visit http://localhost:3000 in your browser to see the application.


## Setting Up the Backend

Follow these steps to set up the project's backend locally

1. Navigate to the fridgy-api folder

```bash
cd fridgy/fridgy-api
```

2. Create a .env file with your OpenAI API key

```bash
OPENAI_API_KEY={your_key_here}
```

3. Install virtualenv (if not already installed)

```bash
pip install virtualenv
```

4. Create/activate a virtual environment

- For windows:

```bash
virtualenv venv
python -m venv venv
venv\Scripts\activate
```

- For macOS/Linux:

```bash
virtualenv venv
python -m venv venv
source venv/bin/activate
```

5. Install requirements

```bash
pip install -r requirements.txt
```

6. Run the server

```bash
uvicorn app.main:app --reload
```

## Setting Up PostgresDB Locally

Follow these steps to set up PostgresDB locally.

1. Install [Homebrew](https://brew.sh/) 
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Postgres

Tutorial: https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb

```bash
brew install postgresql
```

Start Postgres.

```bash
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

3. Configure Postgres
```bash
psql postgres
```

Once in Postgres client, create a user named rick with password 'rick'.

```postgres
CREATE ROLE rick WITH LOGIN PASSWORD 'rick';
```

Add CREATEDB permission to user rick to allow rick to create databases:

```postgres
ALTER ROLE rick CREATEDB;
```

4. Create database
```postgres
CREATE DATABASE fridgy;
```

Grant all database privileges to user rick. 
```postgres
GRANT ALL PRIVILEGES ON DATABASE fridgy TO rick;
```

Check tables in databases.
```postgres
\list
```

5. Make inventory table

Log out of Postgres client with 'exit'. Log back in using:
```bash
psql fridgy -U rick
```

Make user and inventory table.
```postgres
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

```postgres
CREATE TABLE inventory (
    user_id INTEGER REFERENCES users(id),
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    expiration_date DATE NOT NULL,
    PRIMARY KEY (user_id, item)
);
```

Run fridgy_postgres.ipynb notebook for testing.

## Setting Up Environment (.env file)
In order to successfully run Fridgy locally, create a .env file in the project base directory and include the following:
```
OPENAI_API_KEY=<Your OpenAI API Key>
PINECONE_API_KEY=<Your Pinecone API Key>
TOGETHER_API_KEY=<Your Together.ai API Key>
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX=fridgy
DB_HOST=localhost
DB_USER=<your postgres username>
DB_PASSWORD=<your postgres password>
DB_NAME=fridgy
```
