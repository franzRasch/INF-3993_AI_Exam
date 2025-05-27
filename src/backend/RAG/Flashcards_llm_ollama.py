from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from template import create_template, create_question_template, create_answer_template
from vectorstore import load_vectorstore


class FlashCards:
    def __init__(self, topic: str, model_name="llama3.2:latest", k: int = 3, number_of_questions: int = 2):
        self.topic = topic
        self.number_of_questions = number_of_questions
        self.k = k
        self.context = ""
        self.question_and_answer = []
        self.already_asked_questions = []

        self.llm = OllamaLLM(model=model_name)
        template = create_question_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)
        self.db = load_vectorstore()

    def _format_prompt(self, retrieved_context: str) -> str:
        return self.prompt_template.format_prompt(
            topic=self.topic,
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
    
    def run_flashcards(self, number_of_questions):
        for i in range(number_of_questions):
            question = self.generate_question()
            answer = self.answer(f"{question}")
            qa_pair = (question, answer)
            self.question_and_answer.append(qa_pair)
        print(self.question_and_answer)

    def run(self):
        self.run_flashcards(self.number_of_questions)
        return






