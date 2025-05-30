from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .template import create_template, create_question_template, create_answer_template
from .vectorstore import load_vectorstore
from .question_generator_base import QuestionGeneratorBase


class FlashCards(QuestionGeneratorBase):
    def __init__(
        self,
        topic: str,
        model_name="llama3.2:latest",
        k: int = 3,
        number_of_questions: int = 2,
    ):
        super().__init__(topic, model_name, k, number_of_questions)
        self.question_and_answer = []

    def answer(self, generated_question: str, debug=False) -> str:
        prompt = create_answer_template().format(
            topic=self.topic, generated_question=generated_question
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
