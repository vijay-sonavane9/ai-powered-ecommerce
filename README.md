# 🛍️ AI-Powered Semantic E-Commerce Platform

![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A full-stack, next-generation e-commerce storefront that replaces traditional keyword matching with deep **Semantic Vector Search**. 

Instead of searching for exact product names (e.g., "Ergonomic Chair"), users can describe their problems, needs, or desired vibes (e.g., *"My back hurts from sitting all day"*), and the platform's AI evaluates the conceptual meaning to retrieve the perfect product.

## ✨ Key Features

* **🧠 Semantic AI Search:** Powered by Google's `gemini-embedding-001` model, converting user queries into mathematical vectors to understand intent rather than just keywords.
* **⚡ High-Performance Backend:** Built with Python and FastAPI for lightning-fast API responses and asynchronous processing.
* **🗄️ Dual-Database Architecture:** * **ChromaDB:** A specialized vector database to store and calculate AI "brain patterns" (embeddings).
  * **SQLite:** A standard relational database to store concrete product details (prices, names, image URLs).
* **🌐 Automated Data Ingestion:** Includes a custom pipeline (`mega_ingest.py`) that fetches real-world product data from an external API, generates AI embeddings on the fly, and populates both databases automatically.
* **🛒 Modern Frontend UI:** A responsive, client-side rendered storefront built with Next.js, React, and Tailwind CSS, featuring live search and dynamic shopping cart state management.

---

## 🏗️ Project Architecture

```text
📦 ai-powered-ecommerce
 ┣ 📂 backend                 # Python FastAPI Server & AI Logic
 ┃ ┣ 📂 chroma_data           # Local Vector Database Storage
 ┃ ┣ 📜 main.py               # Core API Server & Search Endpoints
 ┃ ┣ 📜 mega_ingest.py        # Automated Data Fetching & Vector Generation
 ┃ ┣ 📜 ecommerce.db          # Standard Relational Database
 ┃ ┗ 📜 .env                  # Environment Variables (API Keys)
 ┗ 📂 frontend                # Next.js User Interface
 ┃ ┣ 📂 src/app               
 ┃ ┃ ┣ 📜 page.tsx            # Main Storefront UI & Search Logic
 ┃ ┃ ┗ 📜 layout.tsx          # Global Layout
 ┃ ┣ 📜 tailwind.config.ts    # Styling Configuration
 ┃ ┗ 📜 package.json          # Node Dependencies
