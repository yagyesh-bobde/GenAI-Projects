from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(
    model='qwen2.5-coder' #or use --llama3.2-- steps to follow : run in local machine-- -ollama pull <model> -ollama run <model>
)

chatHistory = [
    SystemMessage(content='You are a joyful chatbot')
]
while True:
    userInput = input("I : ")
    chatHistory.append(HumanMessage(content=userInput))
    if userInput == 'exit':
        break
    result = llm.invoke(userInput)
    chatHistory.append(AIMessage(result.content))
    print("Deepseek bhai : ", result.content)

print(chatHistory)