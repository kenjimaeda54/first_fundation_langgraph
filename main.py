from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState,END

from nodes import run_agent_reasoning, tool_node

ACT = "act"
AGENT_REASONING = "reasoning"
LAST = -1


def should_continue(state: MessagesState) -> str:
    """Determine whether to continue reasoning or act."""
    last_message = state["messages"][LAST].tool_calls
    if not last_message:
        return END
    return ACT


flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASONING, run_agent_reasoning)

flow.add_node(ACT,tool_node)

flow.set_entry_point(AGENT_REASONING)

flow.add_conditional_edges(AGENT_REASONING,should_continue,{
    END:END,
    ACT:ACT
})

flow.add_edge(ACT,AGENT_REASONING)

app = flow.compile()

app.get_graph().draw_mermaid_png(output_file_path="flow.png")


if __name__ == "__main__":
    res = app.invoke({"messages": HumanMessage(content="Qual e a temperatura de hoje em São Paulo me traga é multipla por 2")})
    print(res["messages"][LAST].content)
