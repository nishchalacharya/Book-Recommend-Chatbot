# from transformers import T5Tokenizer, T5ForConditionalGeneration

# # Load model and tokenizer
# t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
# t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

# # ✅ Build the prompt
# def build_t5_prompt(query, top_books):
#     book_blocks = []

#     for book in top_books:
#         desc = book.get("text", "No Description available")[:400].replace("\n", " ")
#         book_blocks.append(
#             f"Title: {book['title']}\n"
#             f"Author: {book['authors']}\n"
#             f"Rating: {book['average_rating']}\n"
#             f"Description: {desc}"
#         )

#     full_context = "\n\n".join(book_blocks)

#     prompt = (
#         f"You are a friendly book recommendation assistant.\n"
#         f"A user asked: \"{query}\"\n\n"
#         f"Here are the top books retrieved:\n\n"
#         f"{full_context}\n\n"
#         f"Based on these books, recommend and explain them in a conversational tone. "
#         f"Summarize what each book is about and why it might interest the user."
#     )

#     return prompt


# # ✅ Example usage
# # Simulated query and top_books from vector DB
# query = "I want a thrilling mystery novel"
# top_books = [
#     {
#         "title": "Gone Girl",
#         "authors": "Gillian Flynn",
#         "average_rating": 4.11,
#         "text": "A thrilling story about a woman who disappears and the secrets of a toxic marriage unfold."
#     },
#     {
#         "title": "The Girl with the Dragon Tattoo",
#         "authors": "Stieg Larsson",
#         "average_rating": 4.15,
#         "text": "An investigative journalist and a brilliant hacker team up to solve a decades-old disappearance."
#     }
# ]

# # # ✅ Generate T5-based response
# # prompt = build_t5_prompt(query, top_books)
# # input_ids = t5_tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=768)

# # output_ids = t5_model.generate(
# #     input_ids,
# #     max_length=500,
# #     num_beams=4,
# #     early_stopping=True,
# #     no_repeat_ngram_size=2
# # )

# # chatbot_reply = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)

# # # ✅ Print result
# # print("📚 Chatbot Recommendation:\n")
# # print(chatbot_reply)

# for book in top_books:
#     desc = book.get("text", "")
#     input_text = f"Summarize this book in 3 sentence and add "Perfect choice": {desc}"
#     input_ids = t5_tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)
#     output_ids = t5_model.generate(input_ids, max_length=50)
#     summary = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)
#     print(f"{book['title']} — {summary}")

from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load model and tokenizer
t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

# Simulated book list
top_books = [
    {
        "title": "Gone Girl",
        "authors": "Gillian Flynn",
        "average_rating": 4.11,
        "text": "Gone Girl by Gillian Flynn"
    },
    # {
    #     "title": "The Girl with the Dragon Tattoo",
    #     "authors": "Stieg Larsson",
    #     "average_rating": 4.15,
    #     "text": "This novel follows journalist Mikael Blomkvist and hacker Lisbeth Salander as they investigate the disappearance of a young girl from decades ago. It uncovers dark family secrets and a tangled web of crime and corruption."
    # }
]

# Loop and summarize each book
for book in top_books:
    desc = book.get("text", "No description available")[:400].replace("\n", " ")
    input_text = f"Summarize this book in 3 sentences and end with: 'Perfect choice.': {desc}"
    
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)
    output_ids = t5_model.generate(input_ids, max_length=100)
    summary = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print(f"\n📚 {book['title']} by {book['authors']} (Rating: {book['average_rating']})\n{summary}")
