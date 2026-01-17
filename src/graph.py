from typing import Literal
from langgraph.graph import StateGraph, START, END
from src.nodes import llm_node, tool_node
from src.state import AgentState
from langchain.messages import ToolMessage

def should_continue(state: AgentState) -> Literal["tool_node", END]:
    """Karar mekanizmasi: Tool mu cagirilacak yoksa bitecek mi"""
    messages = state["messages"]
    last_message = state["messages"][-1]



    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tool_node"
    return END

builder = StateGraph(AgentState)

builder.add_node("llm_node", llm_node)
builder.add_node("tool_node", tool_node)

builder.add_edge(START, "llm_node")
builder.add_conditional_edges(
    "llm_node",
    should_continue,
    {
        "tool_node": "tool_node",
        END: END
    }
)
builder.add_edge("tool_node", "llm_node")

graph_app = builder.compile()