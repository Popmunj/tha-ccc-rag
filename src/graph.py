from typing_extensions import TypedDict
from typing import Annotated
from nodes import similarity_search, transform_query, generate
from edges import grade_answer

from langchain_core.documents.base import Document
from langgraph.graph.message import add_messages

from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]
    documents: list[Document]

workflow = StateGraph(State)


workflow.add_node("similarity_search", similarity_search)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)



workflow.add_edge(START,
                  "similarity_search")
workflow.add_edge("similarity_search",
                  "generate")



workflow.add_conditional_edges("generate",
                               grade_answer,
                               {
                                   "yes": END,
                                   "no": "transform_query"
                               }
                              )

workflow.add_edge("transform_query", "similarity_search")
app = workflow.compile()

def get_app():
    return app