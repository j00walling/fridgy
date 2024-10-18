# Fridgy

Fridgy is a Refrigerator Assistant Chatbot that helps users manage their refrigerator inventory and provides recipe suggestions based on the items available. The UI is built using the Next.js framework with React, and the backend is developed using Flask.

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

For windows:

```bash
virtualenv venv
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

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
