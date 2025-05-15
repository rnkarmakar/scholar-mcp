import asyncio
import os
import streamlit as st
from textwrap import dedent

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

st.set_page_config(
    page_title="Scholar Agent",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("<h1 class='main-header'>Google Scholar MCP Agent</h1>", unsafe_allow_html=True)
st.markdown("Interact with a powerful web agent that can scrape data from Google Scholar.")

with st.sidebar:
    st.markdown("### Example commands")
    st.markdown("**Navigation**")

query = st.text_area("Your command", placeholder="Enter your command here...")

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.mcp_app = MCPApp(name="streamlit_mcp_agent")
    st.session_state.mcp_context = None
    st.session_state.mcp_agent_app = None
    st.session_state.browser_agent = None
    st.session_state.llm = None
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)

async def setup_agent():
    if not st.session_state.initialized:
        try:
            st.session_state.mcp_context = st.session_state.mcp_app.run()
            st.session_state.mcp_agent_app = await st.session_state.mcp_context.__aenter__()

            # Create agent with minimal configuration
            agent = Agent(name="browser_agent")
            agent.instructions = """You are a helpful web browsing assistant that can fetch google scholar data.
                """
            agent.server_names = ["scholar", "arxiv-mcp-server"]
            st.session_state.browser_agent = agent    

            await st.session_state.browser_agent.initialize()
            st.session_state.llm = await st.session_state.browser_agent.attach_llm(OpenAIAugmentedLLM)

            logger = st.session_state.mcp_agent_app.logger
            tools = await st.session_state.browser_agent.list_tools()
            logger.info("Tools available:", data=tools)

            st.session_state.initialized = True
        except Exception as e:
            return f"Error initializing agent: {e}"
    return None        

async def run_mcp_agent(message):
    

    try:
        error = await setup_agent()
        if error:
            return error
        
        result = await st.session_state.llm.generate_str(
            message=message,
            request_params=RequestParams(use_history=True)
        )

        return result
    except Exception as e:
        return  f"Error: {str(e)}"
    
if st.button("Run command", type="primary", use_container_width=True):
    with st.spinner("Processing your result...."):
        result = st.session_state.loop.run_until_complete(run_mcp_agent(query))  

    st.markdown("### Response")
    st.markdown(result)
