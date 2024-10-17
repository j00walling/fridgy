# Fridgy

Fridgy is a Refrigerator Assistant Chatbot that helps users manage their refrigerator inventory and provides recipe suggestions based on the items available. The UI is built using the Next.js framework with React, and the backend is developed using Flask.

## Prerequisites

- **Node.js**: Install [Node.js](https://nodejs.org/) (version 20.12.0 or higher).
- **pnpm**: Install [pnpm](https://pnpm.io/) globally if you haven't already:

  ```bash
  npm install -g pnpm
  ```

## Setting Up the Project

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
```bash
pip install python-dotenv
```
```bash
pip install --upgrade openai
```
```bash
pip install uvicorn
```

3. Make a ".env" file in your working directory and paste:  OPENAI_API_KEY=YOUR KEY HERE

4. Run the Development Server

```bash
pnpm run dev
```
```bash
python main.py
```

4. Open Your Browser

Visit http://localhost:3000 in your browser to see the application.
