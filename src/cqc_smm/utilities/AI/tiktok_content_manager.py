# Create AI agent that will use some templat wtih specifics from account type/user to create content
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI


class Config:
    """
    Contains the configuration of the LLM.
    """
    model = 'gpt-3.5-turbo-16k-0613'
    llm = ChatOpenAI(temperature=0, model=model)

    # Setup memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    system_message = ""

    agent_kwargs = {
        # "extra_prompt_messages": [chat_history],
        "system_message": system_message,
        # "memory_prompts": [memory],
        "handle_parsing_errors": True,
        # "memory_variables": "chat_history",
        "input_variables": ["input",
                            "agent_scratchpad",
                            "chat_history"],
        # "verbose": get_verbose(),
        "memory": memory,
    }


def setup_agent():
    cfg = Config()

    agent = initialize_agent(
        # tools=tools,
        llm=cfg.llm,
        # agent=AgentType.OPENAI_FUNCTIONS,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=cfg.agent_kwargs,
        memory=cfg.memory,
        handle_parsing_errors=True,
        max_iterations=5,
        # early_stopping_method="generate"
    )

    return agent


def get_next_content():
    # Use previous content as guide
    prev_content_db = []

    # Follow prompt to get  (i.e tite, caption, purpose, post date time)