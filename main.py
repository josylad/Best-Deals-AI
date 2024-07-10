from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

from tools.amazon import amazon_reader_engine
from tools.ebay import ebay_reader_engine
from decouple import config
import os
import streamlit as st


os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

llm = OpenAI(model="gpt-4o")


context = '''You are an AI best deal finder. 
You help people find the cheapest product price by comparing prices across multiple online marketplaces.. 
Return the cheapest products and prices from all the online marketplaces; also add a link to the product if available.'''

agent = ReActAgent.from_tools(
    tools=[
        amazon_reader_engine,
        ebay_reader_engine,
    ],
    llm=llm,
    verbose=True,
    context=context,
)


st.title("Best Deal AI")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Hello, Pls Enter a Product name:")
   
if prompt:
    with st.chat_message("user"):
         st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st.write("Finding the best deals for you...")

    answer = agent.chat(prompt)
    with st.chat_message("assistant"):
        st.write(answer.response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer.response})
    