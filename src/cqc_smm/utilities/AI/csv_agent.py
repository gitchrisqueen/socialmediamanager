import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonAstREPLTool
from langchain_openai import ChatOpenAI
from pandas import Series


def get_top_n_question(csv_file, n_results: int = 5) -> list:
    df = pd.read_csv(csv_file)
    df_filtered = df[df['Modifier Type'] == 'Questions']
    df_sorted = df_filtered.sort_values('Search Volume', ascending=False)
    top_5_suggestions = Series(df_sorted['Suggestion'].unique()).head(n_results).tolist()
    #print(top_5_suggestions)
    return top_5_suggestions



def get_csv_response(csvs: list[str], question: str) -> str:
    # Setup memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_kwargs = {
        "handle_parsing_errors": True,
        #"input_variables": ["input",
        #                    "agent_scratchpad",
        #                    # "chat_history"
        #                    ],
        # "memory": memory,
    }

    """
    # --- HACK: From  https://github.com/langchain-ai/langchain/issues/6166#issuecomment-1823085910
    PythonAstREPLTool_init = PythonAstREPLTool.__init__

    def PythonAstREPLTool_init_wrapper(self, *args, **kwargs):
        PythonAstREPLTool_init(self, *args, **kwargs)
        self.globals = self.locals

    PythonAstREPLTool.__init__ = PythonAstREPLTool_init_wrapper
    # --- END HACK
    """


    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        csvs,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #handle_parsing_errors=True,
        #pandas_kwargs=agent_kwargs,
        agent_executor_kwargs=agent_kwargs,
        # early_stopping_method="generate",
    )
    """

    # Working Nyt not correct results Below

    dfs = []
    for csv in csvs:
        dfs.append(pd.read_csv(csv))

    agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        df=dfs,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        agent_executor_kwargs=agent_kwargs,
        # number_of_head_rows=1 # TODO: Make sure this is correct or even needed
    )
        """

    return agent.invoke(
        input={"input": question},
        # chat_history=[memory]
    )


if __name__ == "__main__":
    csv_file_path = '//downloads/hair growth-en-us-suggestions-30-01-2024.csv'
    questions = get_top_n_question(csv_file_path)
    print(questions)

    """
    print(get_csv_response(
        [csv_file_path],
        "If you filter by Modifier Type=Questions then sort Search Volume in descending order What are the top 5 Suggestions?")
    )
    """
