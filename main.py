from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import chainlit as cl

# ALL CONSTANTS
IMAGE_NAME = "llama3.2-vision"
MODEL_NAME = "llama3.2"
MEME_DIR = "meme-directory/"

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Hello! I am a meme classifier. Send me a meme and I will classify it for you."
    ).send()

    model = OllamaLLM(model=IMAGE_NAME)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a meme classifier. Classify this meme."),
            ("human", "{question} : {meme}"),
        ]
    )
    chain = prompt | model
    cl.user_session.set("chain", chain)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    msg = cl.Message(content="")
    async for chunk in chain.astream(
        {"meme": [message.elements[0].path],
        "question": message.content}
    ):
        await msg.stream_token(chunk)
    await msg.send()