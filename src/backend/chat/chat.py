from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .template import chat_template


class Chat:
    def __init__(self, topic: str, model_name="llama3.2:latest"):
        self.topic = topic
        self.context = "New chat, no previous context."
        self.llm = OllamaLLM(model=model_name)
        template = chat_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)

    def _format_prompt(self, user_input: str) -> str:
        return self.prompt_template.format_prompt(
            topic=self.topic,
            context=self.context,
            user_input=user_input,
        ).to_string()

    def ask(self, user_input):
        prompt = self.prompt_template.format_prompt(
            topic=self.topic,
            context=self.context,
            user_input=user_input,
        ).to_string()
        full_output = ""
        for chunk in self.llm.stream(prompt):
            yield chunk
            print(chunk, end="", flush=True)
            full_output += chunk
        self.context += f"\nYou: {user_input}\nChatbot: {full_output.strip()}"
        return True
