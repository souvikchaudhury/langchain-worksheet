from pyclbr import Class
from xxlimited import Str
from dotenv import load_dotenv
import os
from typing import List

from pydantic import Field
from pydantic_core import Url
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# from langchain_ollama import ChatOllama
from pydentic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
load_dotenv()

# def dmain():
#     print("Hello from langchain-course!")
#     # print(os.getenv("OPENAI_API_KEY"))
#     # print(os.getenv("GOOGLE_API_KEY"))
#     information = """
#         Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, co-inventor, 
#         and investor. A pioneer of the personal computer revolution of the 1970s and 1980s, 
#         Jobs co-founded Apple Inc. (as Apple Computer Company) with Steve Wozniak and Ronald Wayne in 1976.
#         After the company's board of directors fired him in 1985, he founded NeXT the same year and purchased Pixar in 1986, 
#         becoming its chairman and majority shareholder until 2007. Jobs returned to Apple in 1997 as CEO, where he was closely 
#         involved with the creation and promotion of many of the company's most influential products until his resignation in 2011.
#         Jobs was born in San Francisco in 1955 and adopted shortly afterwards. He attended Reed College in 1972 before withdrawing 
#         that same year. In 1974, he traveled through India, seeking enlightenment before later studying Zen Buddhism. He and Wozniak 
#         co-founded Apple in 1976 to further develop and sell Wozniak's Apple I personal computer. Together, the duo gained fame and 
#         wealth a year later with production and sale of the Apple II, one of the first highly successful mass-produced microcomputers.
#         Jobs saw the commercial potential of the Xerox Alto in 1979, which was mouse-driven and had a graphical user interface (GUI). 
#         This led to the development of the largely unsuccessful Apple Lisa in 1983, followed by the breakthrough Macintosh in 1984, 
#         the first mass-produced computer with a GUI. The Macintosh launched the desktop publishing industry in 1985 (for example, 
#         the Aldus PageMaker) with the addition of the Apple LaserWriter, the first laser printer to feature vector graphics and PostScript.
#         In 1985, Jobs departed Apple after a long power struggle with the company's board and its then-CEO, John Sculley. That same year, 
#         Jobs took some Apple employees with him to found NeXT, a computer platform development company that specialized in computers for 
#         higher-education and business markets, serving as its CEO. In 1986, he bought the computer graphics division of Lucasfilm, 
#         which was spun off independently as Pixar.[2] Pixar produced the first computer-animated feature film, Toy Story (1995), 
#         and became a leading animation studio, producing dozens of commercially successful and critically acclaimed films.
#         In 1997, Jobs returned to Apple as CEO after the company's acquisition of NeXT. He was largely responsible for reviving Apple, 
#         which was on the verge of bankruptcy. He worked closely with British designer Jony Ive to develop a line of products and services 
#         that had larger cultural ramifications, beginning with the "Think different" advertising campaign, and leading to the iMac, iTunes, 
#         Mac OS X, Apple Store, iPod, iTunes Store, iPhone, App Store, and iPad. Jobs was also a board member at Gap Inc. from 1999 to 2002.[3] In 2003, 
#         Jobs was diagnosed with a pancreatic neuroendocrine tumor. He died of tumor-related respiratory arrest in 2011; in 2022, 
#         he was posthumously awarded the Presidential Medal of Freedom. Since his death, he has won 141 patents; Jobs holds over 450 patents in total.[4]
#     """

#     summary_template = """
#         Given the following {input_text} about a person from history, I want to create:
#         1) A short summary
#         2) Two fun facts about the person
#     """

#     summary_prompt_template = PromptTemplate(
#         input_variables=["input_text"],
#         template=summary_template
#     )

#     # llm = ChatOllama(model="gemma3:270m", temperature=0)
#     llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
#     #The | operator chains two components so the output of the first becomes the input of the second:
#     chain = summary_prompt_template | llm  
    
#     # Chain.invoke(...) runs the chain once with the given input and returns the result.
#     # {"information": information} is the input dictionary that the chain expects:
#     response = chain.invoke(input={"input_text": information})

#     print(response.content)

class Source(BaseModel):
    """ Schema for a source used by Agent"""
    Url:str = Field(description="The URL of the Source")

class AgentResponse(BaseModel):
    """ Schema for agent respose with Answer and sources"""
    answer:str = Field(description="The agent answer to the query")
    sources:List[Source] = Field(default_factory=list, description="List of sources used to generate answer")

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    return f"Searching Wikipedia for: {query}"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search_wikipedia]
agent = create_agent(model=llm, tools=tools, response_format=ToolStrategy(AgentResponse))

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages": [HumanMessage(content="What is MVVM?")]})
    print(result)
    print("structured_response:", result.get("structured_response"))
    

if __name__ == "__main__":
    main()
