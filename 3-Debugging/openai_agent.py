## using messages as state
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START,END,StateGraph
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.tools  import tool
from langchain_core.messages import BaseMessage
from typing import Annotated
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KAY")

## we will end up adding messages as inputed and add_messages will help us in appending the message

class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model = ChatOpenAI(temperature=0)


def make_default_graph():
    graph_workflow = StateGraph(State)
    def call_model(state:State):
        return {"messages":[model.invoke(state["messages"])]}
    
    graph_workflow.add_node("agent",call_model)
    graph_workflow.add_edge(START,"agent")
    graph_workflow.add_edge("agent",END)
    agent = graph_workflow.compile()
    return agent

def make_alternative_graph():
    """ Make a tool calling agent"""
    @tool
    def add(a:float,b:float):
        """add two numbers"""
        return a+b
    tool_node = ToolNode([add])
    model_with_tools = model.bind_tools([add])
    def call_model(state):
        return {"message":[model_with_tools.invoke(state["messages"])]}
    def should_continue(state:State):
        if state["messages"][-1].tools_calls:
            return "tools"
        else:
            return END
    graph_workflow.add_node("agent",call_model)

    graph_workflow.add_node("tools",tool_node)
    graph_workflow.add_edge("tools","agent")
    graph_workflow.add_edge(START,"agent")
    graph_workflow.add_conditional_edges("agent",should_continue)

    agent = graph_workflow.compile()
    return agent
    




agent=make_alternative_graph()
    
    