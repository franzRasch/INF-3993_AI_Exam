
from .flashcards_pipeline import parse_all
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .template import create_question_template, create_answer_template
from .knowledge_base import KnowledgeBase
from collections import deque
import os
import time
import random


class FlashcardsGenerator:
    def __init__(self, topic: str, knowledge_base: KnowledgeBase, model_name="llama3.2:latest"):
        self._read_context()
        self.knowledge_base: KnowledgeBase = knowledge_base
        self.topic: str = topic
        self.model_name: str = model_name
        self.llm: OllamaLLM = OllamaLLM(model=model_name)
        self.prompt_template_question = ChatPromptTemplate.from_template(create_question_template())
        self.prompt_template_answer = ChatPromptTemplate.from_template(create_answer_template())

        self.already_asked_questions = deque(maxlen=10)
        self._prepare_base_prompt()

    def _read_context(self) -> None:
        path = parse_all()
        files = os.listdir(path)
        docs = list()
        for file in files:
            with open(path + "/" + file) as f:
                context = f.read()
                docs.append(context)
        self.context: list[str] = docs

    def _get_context_snippet(self, max_docs=5) -> str:
        return "\n\n".join(random.sample(self.context, min(len(self.context), max_docs)))

    def _prepare_base_prompt(self):
        snippet = self._get_context_snippet()
        self._base_prompt = self.prompt_template_question.partial(
            topic=self.topic,
            retrieved_context=snippet
        )

    def generate_question(self) -> str:
        prompt = self._base_prompt.format_prompt(
            already_asked_questions=list(self.already_asked_questions)
        ).to_string()

        output = self.llm.invoke(prompt).strip()
        self.already_asked_questions.append(output)
        return output

    def generate_answer(self, question: str) -> str:
        context = self.knowledge_base.search_collection(question)
        prompt = self.prompt_template_answer.format_prompt(
            topic=self.topic,
            generated_question=question,
            context=context
        ).to_string()

        output = self.llm.invoke(prompt).strip()
        return output

    def generate_flashcards(self, num_questions: int) -> list:
        qa_list = list()
        for _ in range(num_questions):
            start_time = time.perf_counter()
            question = self.generate_question()
            end_time = time.perf_counter()
            print(f"time to generate question: {end_time - start_time:.2f}s")

            start_time = time.perf_counter()
            answer = self.generate_answer(question)
            end_time = time.perf_counter()
            print(f"time to generate answer: {end_time - start_time:.2f}s")

            qa_pair = (question, answer)
            qa_list.append(qa_pair)

        return qa_list


if __name__ == "__main__":
    kb = KnowledgeBase("inf-3701")
    kb.build_collection("books")
    print("KB made")
    fg = FlashcardsGenerator("advanced distributed databases", kb)
    flashcards = fg.generate_flashcards(1)
    for i, flashcard in enumerate(flashcards):
        print(f"Flashcard {i}:")
        print(f"Question: {flashcard[0]}\n")
        print(f"Answer: {flashcard[1]}\n")
