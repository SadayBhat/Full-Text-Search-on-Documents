# Full-Text Search (FTS) API using FastAPI & PostgreSQL

This project implements a **Full-Text Search (FTS) API** that allows users to upload PDF documents, perform efficient searches, and retrieve results based on matching text content. It uses **FastAPI** for handling API requests and **PostgreSQL** for storing the data and handling the search functionality.

## Introduction

This project is a document search system that allows users to upload documents (specifically PDF files), search through them using **Full-Text Search (FTS)** capabilities in **PostgreSQL**, and download the results in various formats (individually or as a zip file). The main goal of this system is to efficiently handle large document collections with the ability to search text within these documents.

## Project Flow

The flow of the project is designed to efficiently handle the process of uploading documents, storing them in a searchable format, performing searches, and responding with the appropriate files. Here is the general flow of how the system works:

### Uploading Documents:
1. The user uploads a PDF file through the `/upload` API endpoint.
2. The file is processed, and text is extracted using libraries like **PyMuPDF** or **pdfminer.six**.
3. The extracted text is stored in a PostgreSQL database in a searchable format (using PostgreSQL's Full-Text Search (FTS) functionality).

### Performing a Search:
1. A user submits a query through the `/search` API endpoint.
2. The query is processed by the **SearchService** where the query is sanitized, cleaned, and formatted to be compatible with PostgreSQL’s Full-Text Search.
3. The cleaned query is then used to perform a search in the PostgreSQL database using the `tsquery` feature, which helps find matches based on the indexed text data stored in the database.
4. The results are ranked by relevance using the `ts_rank` function in PostgreSQL, which orders the results by the degree of relevance to the query.

### Returning Results:
1. If only one document is found, it is returned directly to the user via a `FileResponse`.
2. If multiple documents are found, they are bundled together into a zip archive and returned to the user using **StreamingResponse**, allowing for efficient download of multiple files without having to save the zip file on disk.

### Error Handling:
- If no documents match the query, a `404 Not Found` response is returned.
- If an unexpected error occurs, a `500 Internal Server Error` response is returned.

## How Full-Text Search Works

### Full-Text Search (FTS) in PostgreSQL

PostgreSQL's Full-Text Search is an advanced mechanism for efficiently searching through large amounts of text-based data. It supports:
- **Text Search Configuration**: A predefined method of handling linguistic variations, stop words, and stemming.
- **Text Search Operators**: A set of operators (`AND`, `OR`, `NOT`) and ranking features to help users refine their searches.
- **Indexes (TSVector)**: Full-text search requires indexing the documents using `TSVector`, which allows for fast searches.
- **Search Queries (TSQuery)**: The search queries are written using the `TSQuery` format and executed against the indexed text.

In the context of this project:
1. When a PDF is uploaded, the extracted text is stored in a PostgreSQL table with a column of type `TSVector`, which contains the vectorized representation of the document's text.
2. When a search query is received, the system first cleans the text (removes special characters, spaces, etc.) and converts it into a valid `TSQuery`.
3. This `TSQuery` is then matched against the indexed data in the `TSVector` columns of the PostgreSQL table.
4. The results are ranked using `ts_rank` based on relevance, and the top results are returned to the user.

This approach is efficient as PostgreSQL can leverage its optimized indexing system to provide fast search results even for large datasets.

### Example Search Flow:
1. **Step 1**: User uploads a PDF containing text like: "The boundaries of Plot No. 28 are clearly defined as South, North, East, and West."
2. **Step 2**: The extracted text is stored in a `TSVector` column in the database.
3. **Step 3**: User submits a query like `boundaries: plot 28`.
4. **Step 4**: The system converts the query into a `TSQuery` (i.e., `to_tsquery('boundaries & plot & 28')`).
5. **Step 5**: PostgreSQL performs the search and returns the relevant document(s) based on the ranked results.

## Detailed System Components

### 1. **API Endpoints**
- **POST /upload**: Uploads a PDF, extracts text, and stores it in the database.
- **GET /search**: Searches for documents based on a query string.

### 2. **Service Layer**
- **SearchService**: Handles search query formatting, execution, and result ranking.
- **FileService**: Manages the logic for file handling, including text extraction and file streaming (including zip creation for multiple file downloads).

### 3. **DAO Layer (Data Access Object)**
- **SearchDAO**: Provides database interaction for searching and retrieving results from PostgreSQL.
  - It queries the `SearchIndex` table for matches using FTS functionality.

### 4. **Database Layer**
- **PostgreSQL**: Stores the documents and their corresponding text in a searchable format. It uses `TSVector` for full-text indexing.
- **SearchIndex Model**: Represents the table that stores the document text and metadata in PostgreSQL.

### 5. **File Handling**
- **PyMuPDF/pdfminer.six**: These libraries are used for extracting text from the uploaded PDF documents.
- **zipstream**: A utility to stream the matching documents as a zip file.

## API Endpoints

### 1. **Upload PDF Document**
```http
POST /api/v1/upload
