# Thai Legal Multi-Agent, Recursive RAG
This simple RAG system traverses through the agents below to answer Thai legal questions.
For now, the used vector store contains only CCC, but it can be easily expanded.

# Graph
The system first fetches relevant chunks (chunked by Section). Then, it generates an answer, and checks if it is a valid answer. If not, it transforms the
query and traverses the graph again. It recursively does this until the answer grader agent decides the answer is valid.

<img  width="350" src="https://github.com/user-attachments/assets/7f741caa-613c-43cd-9c3e-2e73cc838986" />

# Example

<img width="500" alt="chat" src="https://github.com/user-attachments/assets/edf40e64-a41d-423e-aa46-4f9dc95280fe" />
