from langgraph.graph import StateGraph,START,END
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict,Literal,Annotated,Optional,Dict,List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from dotenv import load_dotenv


load_dotenv()

llm=HuggingFaceEndpoint(

    repo_id='meta-llama/Meta-Llama-3-8B-Instruct',

    task='text-generation',

)

model=ChatHuggingFace(llm=llm)
class ChatState(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]



def chat_node(state:ChatState)->ChatState:
    messages=state['messages']
    response=model.invoke(messages)

    return {'messages':[response]}


checkpoint=MemorySaver()

graph=StateGraph(ChatState)
graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)
chatbot=graph.compile(checkpointer=checkpoint)
