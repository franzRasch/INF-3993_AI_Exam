from flashcards_pipeline import parse_all
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from template import create_question_template, create_answer_template
from knowledge_base import KnowledgeBase
import os
from knowledge_base import KnowledgeBase


class FlashcardsGenerator:
    def __init__(self, topic: str, knowledge_base: KnowledgeBase, model_name="llama3.2:latest"):
        self._read_context()
        self.knowledge_base: KnowledgeBase = knowledge_base
        self.topic: str = topic
        self.model_name: str = model_name
        self.llm: OllamaLLM = OllamaLLM(model=model_name)
        self.prompt_template_question = ChatPromptTemplate.from_template(create_question_template())
        self.prompt_template_answer = ChatPromptTemplate.from_template(create_answer_template())

        self.already_asked_questions = []

    def _read_context(self) -> None:
        path = parse_all()
        files = os.listdir(path)
        docs = list()
        for file in files:
            with open(path + "/" + file) as f:
                context = f.read()
                docs.append(context)
        self.context: list[str] = docs
    
    def generate_question(self) -> str:
        flashcards_context = "\n\n".join(self.context)
        prompt = self.prompt_template_question.format_prompt(
            already_asked_questions=self.already_asked_questions,
            topic=self.topic,
            retrieved_context=flashcards_context
        ).to_string()
        full_output = ""
        for chunk in self.llm.stream(prompt):
            full_output += chunk

        self.already_asked_questions.append(full_output.strip())
        return full_output.strip()
    
    def generate_answer(self, question: str) -> str:
        context = self.knowledge_base.search_collection(question)
        prompt = self.prompt_template_answer.format_prompt(
            topic = self.topic,
            generated_question = question,
            context = context
        ).to_string()
        for chunk in self.llm.stream(prompt):
            full_output += chunk
        return full_output.strip()

    def generate_flashcards(self, num_questions: int) -> list:
        qa_list = list()
        for _ in range(num_questions):
            question = self.generate_question()
            answer = self.generate_answer(question)
            qa_pair = (question, answer)
            qa_list.append(qa_pair)
        return qa_list
    
kb = KnowledgeBase("inf-3701")
kb.build_collection("books")
print("KB made")
fg = FlashcardsGenerator("advanced distributed databases", kb)
flashcards = fg.generate_flashcards(1)
for i, flashcard in enumerate(flashcards):
    print(f"Flashcard {i}:")
    print(f"Question: {flashcard[0]}\n")
    print(f"Answer: {flashcard[1]}\n")