import ollama

MEME_DIR = 'meme-directory/'

response = ollama.chat(
    model = 'llama3.2-vision',
    messages = [
        {
            "role": "user",
            "content": "Classify this meme",
            'images': ['meme-directory/vagege-size.png']
        }
    ]
)

print(response)