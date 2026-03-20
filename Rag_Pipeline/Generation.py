
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def generate_answer(prompt):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    response = llm.invoke(prompt)
    return response.content
