from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are acting as a skilled university examiner in the field of {topic}.
Your goal is to help the student practice for an oral exam by:
- Asking follow-up questions based on their answers
- Challenging them on important or subtle points
- Providing hints or small nudges if the student struggles
- Offering clear explanations only after the student has tried to answer

Here is the previous conversation history: {context}

Based on the student's last answer or question, continue the exam practice.
Be strict but encouraging. Keep your replies focused on the exam topic.

Student's input: {question}

Your next examiner question or guidance:
"""


model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation(topic):
    context = ""
    print("Welcome to the AI Chatbot! Type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"topic": topic, "context": context, "question": user_input})
        print(f"Chatbot: {result}")
        context += f"\nUser: {user_input}\nAi:{result}\n"

if __name__ == "__main__":
    handle_conversation("advanced database")