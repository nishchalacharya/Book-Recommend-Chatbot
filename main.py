from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.schemas import BookQuery
from app.recommender import get_top_k_similar_books
from app.deepseek import pass_value

# from app.chatbotmodel import format_books_for_prompt


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.post("/recommend")
def recommend_books(query: BookQuery):
    return get_top_k_similar_books(query.query, query.top_k)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
 
 
   # Step 2: Build prompt from top_books
def build_prompt_for_deepseek(query, books):
    book_blocks = []
    for book in books:
            desc = book.get("text", "No description available")[:400].replace("\n", " ")
            book_blocks.append(
                f"Title: {book['title']}\n"
                f"Author: {book['authors']}\n"
                f"Rating: {book['average_rating']}\n"
                f"Description: {desc}"
            )
    context = "\n\n".join(book_blocks)  
    print('context is',context)
    prompt = (
    f"The user is interested in: '{query}'\n\n"
    f"Here is a list of relevant books with details:\n\n"
    f"{context}\n\n"
    f"Now, choose the 3 most relevant books and respond with recommendations using this exact format:\n\n"
    f"---\n"
    f"Book Title by Author Name(s)\n"
    f"Short 1–2 sentence summary of the book.\n"
    f"(Leave a full blank line below each entry)\n"
    f"---\n\n"
    f"Start your response with:\n"
    f"Based on your query, here are the recommended books:\n\n"
    f"Ensure there is exactly **one blank line** between each book summary — no markdown, no bullet points, no asterisks.\n"
)


    return prompt
 
   
@app.post("/deepseek",response_class=HTMLResponse)
def chatbotapi(request:Request,query:str=Form(...)):
    print('received query successfully',query)
    response=get_top_k_similar_books(query,top_k=3)
    top_books=response['results']
    
 
  # Step 3: Call DeepSeek model
    prompt = build_prompt_for_deepseek(query, top_books)
    print('prompt is',prompt)
    result = pass_value(prompt)
    print('deepseek result is',result)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chatbot_reply": result,
        "results": top_books,
        "precision": response.get("precision")
    })
    
    
        
        
        
        
            
            
    
    





  

from transformers import T5Tokenizer, T5ForConditionalGeneration
from app.recommender import get_top_k_similar_books






# Load T5 model
t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")


@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, query: str = Form(...)):
    print(f"✅ Received query: {query}")

    # Step 1: Get recommended books from vector DB
    response = get_top_k_similar_books(query, top_k=3)  # or 5
    top_books = response["results"]

    if not top_books:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": [],
            "precision": response.get("precision"),
            "chatbot_reply": "Sorry, no books found for your interest."
        })

    # Step 2: Build prompt from top_books
    def build_t5_prompt(query, books):
        book_blocks = []
        for book in books:
            desc = book.get("text", "No description available")[:400].replace("\n", " ")
            book_blocks.append(
                f"Title: {book['title']}\n"
                f"Author: {book['authors']}\n"
                f"Rating: {book['average_rating']}\n"
                f"Description: {desc}"
            )
        print(book_blocks)
        context = "\n\n".join(book_blocks)
        prompt = (
            # f"You are a friendly book recommendation assistant.\n"
            # f"A user asked: \"{query}\"\n\n"
            # f"Here are the top books retrieved:\n\n"
            # f"{context}\n\n"
            # f"Summarize what each book is about in 2–3 sentences and explain why it might interest the user. "
            # f"Speak in a warm, conversational tone like a friendly librarian."
                f"Summarize this book in 3 sentences and end with: 'Perfect choice.': {context}"
            
        )
        return prompt

    prompt = build_t5_prompt(query, top_books)

    # Step 3: Generate chatbot reply using T5
    input_ids = t5_tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
    output_ids = t5_model.generate(
        input_ids,
        max_length=100,
        # num_beams=4,
        # early_stopping=True,
        # no_repeat_ngram_size=2
    )
    chatbot_reply = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print("💬 Chatbot reply:", chatbot_reply)

    # Step 4: Return response to UI
    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": top_books,
        "precision": response.get("precision"),
        "chatbot_reply": chatbot_reply
    })

# ---------------------------------------------------------

