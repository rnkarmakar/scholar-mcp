import asyncio

import streamlit as st
from mcp_agent.agents.agent import Agent
from mcp_agent.app import MCPApp
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM


async def setup_agent():
    if st.session_state.initialized:
        return

    try:
        st.session_state.mcp_context = st.session_state.mcp_app.run()
        st.session_state.mcp_agent_app = await st.session_state.mcp_context.__aenter__()

        agent = Agent(name="browser_agent")
        agent.instructions = "You are a helpful web browsing assistant that can fetch google scholar data"
        agent.server_names = ["scholar", "arxiv-mcp-server"]

        st.session_state.browser_agent = agent
        await st.session_state.browser_agent.initialize()

        st.session_state.llm = await st.session_state.browser_agent.attach_llm(
            OpenAIAugmentedLLM
        )

        logger = st.session_state.mcp_agent_app.logger
        tools = await st.session_state.browser_agent.list_tools()

        logger.info("Tools available:", data=tools)
        st.session_state.initialized = True

    except Exception as err:
        return f"Error initializing agent: {err}"


async def run_mcp_agent(message):
    try:
        if error := await setup_agent():
            return error

        return await st.session_state.llm.generate_str(
            message=message, request_params=RequestParams(use_history=True)
        )

    except Exception as err:
        return f"Error: {err}"


def main():
    st.set_page_config(
        page_title="MCP Agent",
        page_icon=":robot:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("<h1 class='main-header'>MCP Agent</h1>", unsafe_allow_html=True)
    st.markdown(
        "Interact with a powerful web browsing agent that can navigate and interact with websites."
    )

    with st.sidebar:
        st.markdown("### Example commands")
        st.markdown("**Navigation**")

    query = st.text_area("Your command", placeholder="Enter your command here...")

    if "initialized" not in st.session_state:
        st.session_state.initialized = False
        st.session_state.mcp_app = MCPApp(name="streamlit_mcp_agent")
        st.session_state.mcp_context = None
        st.session_state.mcp_agent_app = None
        st.session_state.browser_agent = None
        st.session_state.llm = None
        st.session_state.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(st.session_state.loop)

    if st.button("Run command", type="primary", use_container_width=True):
        with st.spinner("Processing your result...."):
            result = st.session_state.loop.run_until_complete(run_mcp_agent(query))

        st.markdown("### Response")
        st.markdown(result)


if __name__ == "__main__":
    if "__streamlitmagic__" not in locals():
        from streamlit.web.bootstrap import run

        run(__file__, False, [], {})

    else:
        main()
