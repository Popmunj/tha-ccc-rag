import streamlit as st
from graph import get_app
import re

def create_state():

    messages = ["AI: " + m['content'] if m['role'] == "user" else "User: " + m['content'] for m in st.session_state.messages]
    state = {"messages": messages}
  

    return state

def process_response(response) -> tuple[str, list[dict]]:
    answer = res['messages'][-1].content

    docs = res['documents']


    with st.chat_message("Assistant"):
        st.markdown(answer)
   
    return answer, docs

@st.cache_resource
def load_app():
    return get_app()

app = load_app()

st.title("Civil and Commercial Code")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        docs = message.get('documents')
      
        st.markdown(message["content"])
        if docs:
            for doc in docs:
                meta = doc.metadata
                with st.expander(f"{meta.get('Section')}"):
                    st.write(meta)
                    con = doc.page_content
                    try:
                        i = re.search(r"##### มาตรา \d+  \n",con).span()[-1]
                        con = con[i:]
                        st.markdown(f"**เนื้อหา**: {con}")
                    except:
                        st.markdown(con)
        
        

prompt = st.chat_input("Ask away!")
if prompt:
    with st.chat_message("User"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user",
                                      "content": prompt})
    

    res = app.invoke(create_state())
    answer, docs = process_response(res)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "documents": docs,
    })




        




