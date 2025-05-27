# Full-Text-Search-on-Documents

---

```markdown
# 🧠 Full-Text Search (FTS) API using FastAPI & PostgreSQL

This project is a robust document search API built with **FastAPI** and **PostgreSQL Full-Text Search (FTS)**. It enables users to **upload documents**, **extract text**, and **perform efficient full-text searches** across large corpora of PDFs. Matched documents can be downloaded directly or as a zip archive.

---

## 📑 Table of Contents

- [🚀 Features](#-features)
- [📂 Project Structure](#-project-structure)
- [⚙️ Tech Stack](#️-tech-stack)
- [📦 Setup Instructions](#-setup-instructions)
- [🔍 How It Works](#-how-it-works)
- [📌 API Endpoints](#-api-endpoints)
- [🧪 Running Tests](#-running-tests)
- [📌 Future Improvements](#-future-improvements)

---

## 🚀 Features

- Upload PDFs and extract searchable text
- Full-text search using PostgreSQL's native FTS engine
- Download matched files individually or as a zip archive
- Logging, exception handling, and modular architecture
- Token-based security integration ready (optional)

---

## 📂 Project Structure

```bash
FTS/
├── app/
│   ├── api/v1/endpoints/         # FastAPI routes
│   │   ├── search_routes.py
│   │   └── upload_routes.py
│   ├── core/
│   │   ├── config.py             # App config and env loading
│   │   └── constants/            # All constants used in app
│   ├── dao/
│   │   └── search_dao.py         # DB access layer (DAO pattern)
│   ├── database/
│   │   ├── models/               # ORM Models (SearchIndex)
│   │   └── rds.py                # DB connection setup
│   ├── services/
│   │   ├── implementation/
│   │   │   ├── file_service.py   # File extraction and handling
│   │   │   └── search_service.py # FTS logic and ZIP streaming
│   └── utils/
│       ├── file_utils.py         # File utilities
│       └── text_extraction.py    # PDF -> Text logic
│   └── main.py                   # FastAPI app entrypoint
```

---

## ⚙️ Tech Stack

| Layer            | Tech                          |
|------------------|-------------------------------|
| Backend          | Python, FastAPI               |
| Full-Text Search | PostgreSQL (TSVector, TSQuery)|
| ORM              | SQLAlchemy                    |
| PDF Processing   | PyMuPDF                       |
| File Streaming   | zipstream, StreamingResponse  |
| Deployment       | Uvicorn                       |

---

## 📦 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourname/Full-Text-Search-on-Documents.git
cd Full-Text-Search-on-Documents
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL**

Make sure PostgreSQL is running and create a database. Configure connection in `.env`.

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
```

4. **Start the app**

```bash
uvicorn app.main:app --reload
```

---

## 🔍 How It Works

- **Upload**: PDFs are uploaded via the `/upload` endpoint, text is extracted and stored in a PostgreSQL table with a TSVector column for full-text search.
- **Search**: Queries hit the `/search` endpoint and use `websearch_to_tsquery` to match phrases, operators (AND, OR, etc.), and phrases like a Google-style search.
- **Download**: Single file? Serve via `FileResponse`. Multiple matches? Stream as a zip via `StreamingResponse` without writing to disk.

---

## 📌 API Endpoints

### 🔼 Upload

```http
POST /api/v1/upload
```
**Form-data**: `file=<pdf>`

### 🔍 Search

```http
GET /api/v1/search/?query=branch+head
```
**Response**:
- 200: File / Zip
- 404: No match found

---
