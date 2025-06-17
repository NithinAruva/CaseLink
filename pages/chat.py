import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
load_dotenv()

VECTORSTORE_PATH = "vectorstore.index"

def load_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        try:
            embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")
            vectorstore = FAISS.load_local(VECTORSTORE_PATH,embeddings,allow_dangerous_deserialization=True)
            return vectorstore
        except Exception as e:
            st.error(f"Error loading vectorstore: {e}")
    return None

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template = """
        You are an assistant specialized in police investigations. You answer questions strictly related to police reports, criminal activities, suspects, or investigations based on the provided PDF context.
        Guidelines:
        - Only respond to questions relevant to the context of investigations, crime reports, suspects, or legal matters.
        - If the question is unrelated, politely decline to answer.
        - Refer to Indian law sections and articles based on your knowledge.
        - If the answer is unknown or the information is not available, respond with "I don't know."
        - Do not fabricate information or assumptions.
        - If the input is just a greeting or small talk, reply in a friendly and human-like way.
        - If the question is about a specific section of law, provide a brief explanation of that section.
        - If the question refers to a report or document not included in the provided context, state that the data is unavailable.
        - All responses must be in **English**, concise, factual, and directly relevant to the question.
        Use the following context to answer:
        {context}
        Question: {question}
        Answer:
        """

    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )

def handle_user_input(user_question):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.conversation.invoke({'question': user_question})
                bot_response = response['chat_history'][-1].content
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.markdown(bot_response)
            except Exception as e:
                st.error(f"Error generating response: {e}")

def main():
    st.set_page_config(page_title="CaseLink", layout="wide")
    st.title("Chat with Report")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "vectorstore" not in st.session_state:
        vectorstore = load_vectorstore()
        if vectorstore:
            st.session_state.vectorstore = vectorstore
            st.session_state.conversation = get_conversation_chain(vectorstore)
        else:
            st.warning("⚠️ No vectorstore found. Please upload and process documents first.")
            return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question:"):
        handle_user_input(prompt)

main()
