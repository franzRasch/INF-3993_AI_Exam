from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from template import create_template
from vectorstore import load_vectorstore


class ExamTrainer:
    def __init__(self, topic: str, model_name="qwen:1.8b", k=3):
        self.topic = topic
        self.k = k
        self.context = ""
        self.weak_topics = []

        self.llm = OllamaLLM(model=model_name)
        template = create_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)

        self.db = load_vectorstore()


    def _format_prompt(self, question: str, retrieved_context: str) -> str:
        return self.prompt_template.format_prompt(
            topic=self.topic,
            context=self.context,
            question=question,
            retrieved_context=retrieved_context,
            weak_topics=", ".join(self.weak_topics) or "None"
        ).to_string()

    def ask(self, question: str, debug=False) -> str:
        results = self.db.similarity_search(query=question, k=self.k)
        chunks = [doc.page_content for doc in results]

        if debug:
            print("\n🔍 Retrieved Chunks:\n" + "\n---\n".join(chunks))

        retrieved_context = "\n\n".join(chunks)
        prompt = self._format_prompt(question, retrieved_context)
        return self.llm.invoke(prompt)

    def update_context(self, user_input: str, ai_response: str):
        self.context += f"\nStudent: {user_input}\nExaminer: {ai_response}\n"

    def run(self):
        print(f"\n🧠 Welcome to the AI Examiner on '{self.topic}'!\nType 'exit' to quit.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("👋 Exiting the exam simulator. Good luck studying!")
                break

            ai_response = self.ask(user_input)
            self.update_context(user_input, ai_response)

            print(f"Examiner: {ai_response}")

            

    
