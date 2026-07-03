from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from dotenv import load_dotenv
load_dotenv()
import os
from langchain.agents import create_agent
from tavily import TavilyClient

from langchain.tools import tool


loader=PyPDFLoader('Resume.pdf',mode='single')
docs=loader.load()
story=docs[0].page_content

tavily_client=TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

job_des=input('Enter Your JD :- ')

@tool
def surfInternet(query:str):
    """Search the web for the candidate's GitHub profile,
    LinkedIn profile, portfolio, or any public information
    when it helps evaluate the resume."""

    result=tavily_client.search(query=query)
    return str(result['results'])


model=ChatMistralAI(model='mistral-small-latest')

agent=create_agent(model=model,tools=[surfInternet])

res=agent.invoke({

    'messages': [
    SystemMessage("""You are a experience hiring manager and your task is check resume of user
    and JD of user and analysis of both of ATS SCore strength weakness of user based on JD and resume.
    If you need to check github or linkdin of user you have a surfInternet tool that can search github or kinkdin based on url that is
    in resume mentioned so you must be check once for better response.
    If the resume contains GitHub, LinkedIn, or portfolio URLs,
use the tool once to inspect them before generating the report.
Otherwise, continue without using the tool."""),
    SystemMessage('<resume>'+story+'</resume>'),
    HumanMessage('Job Description'+job_des),
    ]
})

print(res["messages"][-1].content)