from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from utils import get_llm

def grade_answer(state):
    """
    Decides whether the answer satisfies the question
    """
    messages = state['messages']
    question = messages[-2]
    answer = messages[-1]

    class GradeAnswer(BaseModel):
        binary_score: Literal["yes", "no"] = Field(description="Answer addresses the question, 'yes' or 'no'")

    system = """You are a grader assessing whether an answer addresses / resolves a question about Thai laws.\n
    If the answer resolves the question, answer 'yes'. Otherwise, answer 'no'.
    """
    grading_prompt = ChatPromptTemplate.from_messages(
        [("system", system),
         ("human", "User question:\n\n{question}\n\nAnswer: {generation}")]
    )
    llm = get_llm().with_structured_output(GradeAnswer)
    chain = grading_prompt | llm


    score = chain.invoke({
        "question": question,
        "generation": answer
    }).binary_score

    return score


def pre_generate(state):
    """
    Decides whether the given question requires the history
    """
    pass