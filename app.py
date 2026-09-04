from langchain_core.tools import tool
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent


@tool
def calculator(expression: str) -> str:
    """A tool for answering math-related questions.
    Input should be a mathematical expression, for example: 25 * 4 + 10.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating expression: {e}"


## Set upi the Stramlit app
st.set_page_config(page_title="Text To MAth Problem Solver And Data Serach Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Uing Google Gemma 2")

groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


if not groq_api_key:
    st.info("Please add your Groq APPI key to continue")
    st.stop()

llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)


## Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()

@tool
def wikipedia_tool(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    return wikipedia_wrapper.run(query)


## Reasoning prompt
prompt = """
You are an agent tasked with solving users' mathematical questions.
Logically arrive at the solution and provide a detailed explanation.
Display the solution point-wise for the question below.

Question: {question}

Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)


## Create reasoning chain using the modern Runnable API
reasoning_chain = prompt_template | llm


## Create reasoning tool
@tool
def reasoning_tool(question: str) -> str:
    """A tool for answering logic-based and reasoning questions."""
    response = reasoning_chain.invoke({"question": question})
    return response.content


## Combine all tools
tools = [
    wikipedia_tool,
    calculator,
    reasoning_tool
]


## Initialize the agent using LangChain 1.x
assistant_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are a helpful math assistant.
    Use the calculator tool for mathematical calculations.
    Use the reasoning tool for logic-based questions.
    Use the Wikipedia tool when general factual information is required.
    """
)


## Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a Math chatbot who can answer your maths questions."
        }
    ]


## Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


## Start interaction
question = st.text_area(
    "Enter your question:",
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. "
    "Then I buy a dozen apples and 2 packs of blueberries. "
    "Each pack of blueberries contains 25 berries. "
    "How many total pieces of fruit do I have at the end?"
)
if st.button("Find my answer"):

    if question:
        with st.spinner("Generating response..."):

            # Add user message
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            st.chat_message("user").write(question)

            # Invoke the agent
            response = assistant_agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
            )

            # Get final response
            final_response = response["messages"][-1].content

            # Add assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": final_response
                }
            )

            # Display response with Markdown + LaTeX support
            st.write("### Response:")
            st.markdown(final_response)

    else:
        st.warning("Please enter the question")