from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from template import create_template, create_question_template, create_answer_template
from vectorstore import load_vectorstore


class ExamTrainer:
    def __init__(self, topic: str, model_name="llama3.2:latest", k: int = 3):
        self.topic = topic
        self.k = k
        self.context = ""
        self.question_and_answer = []

        self.llm = OllamaLLM(model=model_name)
        template = create_question_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)

        self.db = load_vectorstore()


    def _format_prompt(self, question: str, retrieved_context: str) -> str:
        return self.prompt_template.format_prompt(
            topic=self.topic,
            context=self.context,
            question=question,
            retrieved_context=retrieved_context,
        ).to_string()
        

    def ask(self, question: str, debug=False) -> str:
        results = self.db.similarity_search(query=question, k=self.k)
        chunks = [doc.page_content for doc in results]
        if not chunks:
            return "🤖 No relevant information found. Please try asking something else."
        
        if debug:
            print("\n🔍 Retrieved Chunks:\n")
            for index, chunk in enumerate(chunks):
                print(f"Chunk {index}: {chunk}\n")

        retrieved_context = "\n\n".join(chunks)
        prompt = self._format_prompt(question, retrieved_context)

        print("🤖 ", end="", flush=True)  # Prefix for clarity

        # STREAMING
        full_output = ""
        for chunk in self.llm.stream(prompt):  # Limit response tokens to 100
            print(chunk, end="", flush=True)
            full_output += chunk
        return full_output

    def generate_question(self, debug=False) -> str:
        results = self.db.similarity_search(query=self.topic, k=self.k)
        chunks = [doc.page_content for doc in results]

        if debug:
            print("\n🔍 Retrieved Chunks:\n")
            for index, chunk in enumerate(chunks):
                print(f"Chunk {index}: {chunk}\n")

        retrieved_context = "\n\n".join(chunks)

        prompt = self.prompt_template.format_prompt(
            topic=self.topic,
            retrieved_context=retrieved_context
        ).to_string()

        print("", end="", flush=True)
        full_output = ""
        for chunk in self.llm.stream(prompt):
            full_output += chunk

        return full_output.strip()
    
    def answer(self, generated_question: str, debug=False) -> str:
        if not generated_question:
            return "🤖 No question generated. Please try again."

        prompt = create_answer_template().format(
            topic=self.topic,
            generated_question=generated_question
        )

        full_output = ""
        for chunk in self.llm.stream(prompt):
            #print(chunk, end="", flush=True)
            full_output += chunk

        return full_output



    def update_context(self, user_input: str, ai_response: str):
        self.context += f"\nStudent: {user_input}\nExaminer: {ai_response}\n"

    def run(self):
        
        print(f"\n🧠 Welcome to the AI Examiner on '{self.topic}'!\nType 'exit' to quit.\n")

        question = self.generate_question()
        answer = self.answer(f"{question}")
        qa_pair = (question, answer)
        self.question_and_answer.append(qa_pair)
        pair = self.question_and_answer.pop()
        print(pair)
        return
        #print(f"\n🤖 {ai_response.strip()}")

        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit" or "quit" or "bye":
                print("👋 Exiting the exam simulator. Good luck studying!")
                break

            self.update_context(user_input, ai_response)
            ai_response = self.ask(self.topic)  # continue generating new questions from topic
            #print(f"\n🤖 {ai_response.strip()}")





