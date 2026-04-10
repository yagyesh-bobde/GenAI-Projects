# 🤖 Joyful Chatbot using LangChain + Ollama

This is a simple terminal-based chatbot built using **LangChain** and **Ollama**. The chatbot maintains a conversational flow and responds in a joyful tone.

---

## 🚀 Features

* 💬 Interactive command-line chatbot
* 😊 Joyful personality using system prompts
* 🧠 Uses local LLMs via Ollama (no API cost)
* 📜 Maintains chat history (basic implementation)

---

## 🛠️ Tech Stack

* Python
* LangChain
* Ollama
* dotenv

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies

```bash
pip install langchain langchain-core langchain-ollama python-dotenv
```

### 3. Install Ollama

Download and install Ollama from:
https://ollama.com

---

## ⚙️ Setup Model

Pull the model you want to use:

```bash
ollama pull qwen2.5-coder
```

Or use another model like:

```bash
ollama pull llama3.2
```

---

## ▶️ Run the Chatbot

```bash
python your_script_name.py
```

---

## 💡 Usage

* Type your message after `I :`
* Type `exit` to end the conversation

Example:

```
I : Hello
Deepseek bhai : Hey there! 😊 How are you doing today?
```

---

## 🧾 Code Overview

```python
llm = ChatOllama(
    model='qwen2.5-coder'
)
```

* Initializes the local LLM via Ollama

```python
chatHistory = [
    SystemMessage(content='You are a joyful chatbot')
]
```

* Sets chatbot personality

```python
result = llm.invoke(userInput)
```

* Sends user input to the model and gets response

---

## ⚠️ Limitations

* Chat history is stored but not passed into the model context
* No memory persistence across sessions
* Runs only in terminal (no UI)

---

## 🔥 Future Improvements

* Add memory (ConversationBufferMemory)
* Build a web UI (HTML/CSS/JS or React)
* Add voice support (Speech-to-Text)
* Use RAG (Retrieval-Augmented Generation)

---

## 👨‍💻 Author

Abir Majumdar

---

## 📄 License

This project is open-source and free to use.

---
