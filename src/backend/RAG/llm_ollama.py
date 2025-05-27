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
        self.already_asked_questions = []

        self.llm = OllamaLLM(model=model_name)
        template = create_question_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)
        self.db = load_vectorstore()

    def _format_prompt(self, number_of_questions: str, retrieved_context: str) -> str:
        return self.prompt_template.format_prompt(
            topic=self.topic,
            number_of_questions = number_of_questions,
            context=self.context,
            retrieved_context=retrieved_context,
        ).to_string()
        
    def generate_question(self) -> str:
        results = self.db.similarity_search(query=self.topic, k=self.k)
        chunks = [doc.page_content for doc in results]

        retrieved_context = "\n\n".join(chunks)

        prompt = self.prompt_template.format_prompt(
            already_asked_questions=self.already_asked_questions,
            topic=self.topic,
            retrieved_context=retrieved_context
        ).to_string()
        full_output = ""
        for chunk in self.llm.stream(prompt):
            full_output += chunk

        self.already_asked_questions.append(full_output.strip())
        return full_output.strip()
    
    def answer(self, generated_question: str, debug=False) -> str:
        prompt = create_answer_template().format(
            topic=self.topic,
            generated_question=generated_question
        )
        full_output = ""
        for chunk in self.llm.stream(prompt):
            full_output += chunk
        return full_output
    
    def run_q_and_a(self, number_of_questions):
        for i in range(number_of_questions):
            question = self.generate_question()
            answer = self.answer(f"{question}")
            qa_pair = (question, answer)
            self.question_and_answer.append(qa_pair)
        print(self.question_and_answer)


    def run(self):
        number_of_questions = 2
        print(f"\n🧠 Welcome to the AI Examiner on '{self.topic}'!\nType 'exit' to quit.\n")
        self.run_q_and_a(number_of_questions)
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





