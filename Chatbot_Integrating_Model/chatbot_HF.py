from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='deepseek-ai/DeepSeek-R1',
    task='text-generation',
    temperature=1
)

model = ChatHuggingFace(llm = llm)

chatHistory = [
    SystemMessage(content='You are a joyful chatbot')
]
while True:
    userInput = input("I : ")
    chatHistory.append(HumanMessage(content=userInput))
    if userInput == 'exit':
        break
    result = model.invoke(userInput)
    chatHistory.append(AIMessage(result.content))
    print("Deepseek bhai : ", result.content)

print(chatHistory)