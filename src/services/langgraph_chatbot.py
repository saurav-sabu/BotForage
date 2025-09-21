from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict
from src.core.config import settings
from src.schemas.chat_schemas import ChatQuestion

# LLM model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=settings.GOOGLE_API_KEY
)

# State
class ChatState(TypedDict):
    question: str
    context: str
    answer: str

# RAG steps
def retrieve(state: ChatState, retriever):
    docs = retriever.get_relevant_documents(state["question"])
    print(docs)
    context = "\n".join([doc.page_content for doc in docs])
    state["context"] = context
    print("Done with retrieve")
    return state

def generate(state: ChatState, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}\n\nContext:\n{context}")
    ])
    chain = prompt | model
    state["answer"] = chain.invoke(
        {"question": state["question"], "context": state["context"]}
    ).content
    print("Done with generate")
    return state

def build_graph(system_prompt: str, retriever):
    graph = StateGraph(ChatState)

    # Use lambdas to pass extra arguments
    graph.add_node("retrieve", lambda state: retrieve(state, retriever))
    graph.add_node("generate", lambda state: generate(state, system_prompt))

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    print("Done with graph")

    return graph.compile()

def chat(question: str, system_prompt: str, retriever):
    state: ChatState = {"question": question, "context": "", "answer": ""}
    graph = build_graph(system_prompt, retriever)
    result = graph.invoke(state)
    print("Done with chat")
    return result["answer"]
