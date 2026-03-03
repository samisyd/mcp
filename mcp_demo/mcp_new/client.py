from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
import os

import asyncio

async def main():

    load_dotenv()    
    groq_client = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    openai_client = ChatOpenAI(
        model="gpt-5-nano",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    # Use normal context manager (NOT async)
    mcp_client =  MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http",
            }
        }
    ) 
    try:
        tools = await mcp_client.get_tools()
    except Exception as e:
        print("Error loading tools:", e)
        tools = []
    
    react_agent = create_agent(
        tools=tools,
        model=openai_client
    )

    # Example usage of the agent to call the "add" tool from mathserver

    # -------------------------
    # Helper for sending questions with system prompt
    # -------------------------
    async def ask(question: str):
        response = await react_agent.ainvoke(
            {
                "messages": [
                    {"role": "system", "content": "Always try to use the appropriate tool to "
                    "answer the user's question. Only use your own knowledge if a tool cannot "
                    "provide the answer."},
                    {"role": "user", "content": question}
                ]
            }
        )
        return response

    # -------------------------
    # Example usage
    # -------------------------
    math_result = await ask("What is (3 + 5) and then multiply by 12?")
    weather_result = await ask("What is the weather in California?")

    print("Math response:", math_result["messages"][-1].content)
    print("Weather response:", weather_result["messages"][-1].content)
    
if __name__ == "__main__":    
    asyncio.run(main())
