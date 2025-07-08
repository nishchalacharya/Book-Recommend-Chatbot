

# openai.api_base = "https://openrouter.ai/api/v1"
# openai.api_key = "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"  # Replace with your actual OpenRouter API key



# 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






from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def pass_value(query):
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content



# a=pass_value("Hello Deepseek,can you recommend me 3 books to story.my query is books should be of type motivation that gives me motivation to investment  and it should not contain any asterik values,avoid it"
             
#              )

# print(a)


#    # Step 2: Build prompt for DeepSeek
# def build_prompt_for_deepseek(query, books):
#         book_blocks = []
#         for book in books:
#             desc = book.get("text", "No description available")[:400].replace("\n", " ")
#             book_blocks.append(
#                 f"Title: {book['title']}\n"
#                 f"Author: {book['authors']}\n"
#                 f"Rating: {book['average_rating']}\n"
#                 f"Description: {desc}"
#             )
#         context = "\n\n".join(book_blocks)
#         prompt = f"Here are some recommended books:\n\n{context}\n\nBased on the above, respond to this query: '{query}'"
#         return prompt






