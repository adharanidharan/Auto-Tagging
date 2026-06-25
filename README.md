# Smart Similar Question Finder with Auto-Tagging

An AI-powered, full-stack EdTech application built to help students ask academic questions, find semantically similar historical questions, and automatically categorize queries into relevant subjects. Powered by a local-first Natural Language Processing (NLP) pipeline running directly on the backend.

---

## Selected Assignment Option
* **Option**: Option 2 - Smart Similar Question Finder with Auto-Tagging

---

## Key Features

* **JWT-Based Authentication**: Registration and login system using cryptographically secure `bcrypt` password hashing and stateless JSON Web Tokens (JWT).
* **Local-First AI Execution**: Real-time sentence embeddings and cosine similarity computed locally via `sentence-transformers` and `scikit-learn`—**no external paid API dependencies** (OpenAI, Gemini, etc.).
* **Dynamic AI Memory**: Every user query is automatically vectorized and stored as new searchable knowledge, enabling the similarity engine to grow and self-optimize.
* **Smart Semantic Search**: Matches new student queries against historical questions based on semantic context rather than strict keywords, returning the top 5 most relevant results.
* **Low-Confidence Discovery Flow**: Queries classified with confidence $< 50\%$ trigger a background discovery engine that runs online clustering, extracts keywords, and aggregates them into candidate topics.
* **Admin Promotion Dashboard**: Administrators can review AI-discovered topic candidates, assign them to categories (e.g., Technology, Education), and promote them to active vocabularies dynamically.
* **User Feedback Widget**: Students can rate topic classification accuracy and supply corrections, logging data to optimize the classification system.

---

## Architecture & Technology Stack

### Backend
* **FastAPI**: Asynchronous, high-performance Python REST framework.
* **MongoDB Atlas**: Cloud-hosted NoSQL database queried asynchronously via `motor`.
* **Pydantic v2**: High-speed, type-safe data validation and schema parsing.
* **Passlib & python-jose**: Robust JWT-based authentication system.

### Frontend
* **React (Vite)**: Modern, lightning-fast UI build tool.
* **Tailwind CSS v4**: Utility-first CSS styling framework.
* **React Router v7**: Declarative client-side routing with protected route guards.
* **Lucide React**: Clean, modern typography and visual iconography.
* **Axios**: Configured with request interceptors to automatically attach JWT authorization headers.

### AI / ML Core
* **Embeddings**: Pre-trained `sentence-transformers/all-MiniLM-L6-v2` converting query strings into dense 384-dimensional floating-point vectors.
* **Cosine Similarity**: Vector-space comparisons calculated locally using `scikit-learn` to identify semantically related questions and classify topics.

---

## Local Setup Guide

### Prerequisites
Make sure you have the following installed:
* **Node.js** (v18 or higher)
* **Python** (3.9 to 3.11 recommended)
* **MongoDB** (Local instance running at `mongodb://localhost:27017` or a MongoDB Atlas cloud URI)

---

### Step 1: Clone & Navigate to Project Root
```bash
git clone https://github.com/adharanidharan/Auto-Tagging.git
```

---

### Step 2: Backend Configuration & Start

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   * **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   * **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the `backend/` directory:
   ```env
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/techedu?retryWrites=true&w=majority
   JWT_SECRET=your_super_secret_jwt_key_change_in_production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=90
   ```
   *(Note: You can replace MONGODB_URI with `mongodb://localhost:27017/` if running MongoDB locally).*

6. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The Swagger interactive documentation will be available at:* **`http://localhost:8000/docs`**

---

### Step 3: Frontend Configuration & Start

1. Open a new terminal window/tab and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install UI dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The React web application will be accessible at:* **`http://localhost:5173`**

---

## Seeding & Test Executions

### Running Automated Test Suites
The project includes automated integration tests written in `pytest` utilizing `httpx` and `anyio` for asynchronous endpoint testing.

To run the backend tests:
1. Ensure your virtual environment is active in the `backend/` directory.
2. Execute the pytest command:
   ```bash
   python -m pytest tests/ -v
   ```

### Populating the Knowledge Base (Seeding)
To test the semantic search and topic classification capabilities immediately with realistic data, you can seed the database with over 5,000 academic questions:

1. Generate the initial JSON dataset:
   ```bash
   python scripts/generate_dataset.py
   ```
2. Batch-encode the queries and seed MongoDB with required database indexes:
   ```bash
   python scripts/seed_dataset.py
   ```

---
