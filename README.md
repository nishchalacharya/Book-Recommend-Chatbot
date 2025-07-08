# 📚 Book Recommendation Chatbot

A semantic search-powered book recommendation system built using **FastAPI**, **Sentence Transformers**,** T5 and OpenAI Transformers** and **Supabase**. The chatbot takes natural language queries like _"suggest me some romantic books"_ and returns relevant book recommendations from the [Goodbooks-10k dataset](https://github.com/zygmuntz/goodbooks-10k)/ my cleaned_book_dataset.csv inside data folder

---

## 🚀 Features

- 🔍 Semantic search using Sentence Transformers (`all-MiniLM-L6-v2`)
- 🧠 Top-k book recommendations based on vector similarity
- 🤖 LLM-powered chatbot that crafts user-friendly responses
- 📡 FastAPI backend to handle queries and return results
- 🛢️ Supabase PostgreSQL with `pgvector` extension for vector storage
- 🔄 n8n workflow integration (for automation and logging)

---

## 🗂️ Project Structure

Recommendation_Engine/
│
├── app/ # Core logic
│ ├── model.py # Embedding model & Supabase sync
│ ├── recommender.py # Top-k recommendation logic
├── Screenshots   # see screenshots inside it 
├── data/ # Dataset and preprocessed files
│ └── cleaned_book_dataset.csv (many but final csv file this in use)
│
├── main.py # FastAPI entry point
├── requirements.txt # Python dependencies
├── README.md # This file
└── .env # Environment variables (API keys, DB URL)



## 📱 Screenshots

### 🧾 1. Database Table in Supabase

<img width="521" height="444" alt="Image" src="https://github.com/user-attachments/assets/86ac4dad-ecc8-4c19-a899-d5d20f12b350" />














### 💬 2. Chat UI Interface
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/2e0482a2-52e3-4bdb-903f-52e5d0e8ecdc" />

### 📊 3. Recommendation Output by sentence transformer
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/35d2fd52-7c26-45e1-8d9d-9ca2db75a4f3" />

### 🔄 4. t8 chatbot answer
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/cac67b39-ca58-4652-861b-3023de19238a" />

### 5.similarly deepseek also results query



## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/nishchalacharya/Book-Recommend-Chatbot.git
cd Book-Recommend-Chatbot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the App
uvicorn main:app --reload


