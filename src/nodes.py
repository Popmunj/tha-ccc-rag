from utils import get_llm, get_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def transform_query(state):
    llm = get_llm()
    question = state['messages'][0]

    system = """You are a Thai legal question rewriter that converts an input to a better version that is optimized\n
    for Thai legal code retrieval. Look at the question and reason about the underlying semantic intent / meaning."""
    rewriting_prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Initial question\n\n{question}\n\nFormulate an improved one: ")
    ])

    chain = rewriting_prompt | llm | StrOutputParser()
    res = chain.invoke({"question": question})

    return {
        "messages": [res],
        "documents": state['documents']
    }

def generate(state):
    question = state['messages'][-1]
    documents = state['documents']

    llm = get_llm()
    template = """You are an assistant for question-answering tasks about Thai laws.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know. Keep the answer concise but comprehensive.
    If it is a procedural question, structure the answer as a numbered list.
    Keep a friendly, semi-formal tone, refer to yourself as 'ทนายดีดี้' and use คะ/ค่ะ when neccessary. 
    \nQuestion: {question}
    \nContext: {context} 
    \nAnswer:"""

    prompt = ChatPromptTemplate.from_template(
        template=template,
        input_variable=['context', 'question']
    )

    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    chain = prompt | llm | StrOutputParser()
    generation = chain.invoke({
        "context": formatted_docs,
        "question": question
    })

    return {
        "documents": state['documents'],
        "messages": [generation]
    }
    
def similarity_search(state):
   retriever = get_retriever("CCC")
   question = state['messages'][-1].content

   return {"documents": retriever.invoke(question, k=3)}