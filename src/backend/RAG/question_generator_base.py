from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from RAG.template import create_question_template
from RAG.vectorstore import load_vectorstore


class QuestionGeneratorBase:
    """Base class for generating questions based on a topic and context."""

    def __init__(
        self,
        topic: str,
        model_name="llama3.2:latest",
        k: int = 3,
        number_of_questions: int = 2,
    ):
        self.topic = topic
        self.number_of_questions = number_of_questions
        self.k = k
        self.context = ""
        self.already_asked_questions = []

        self.llm = OllamaLLM(model=model_name)
        template = create_question_template()
        self.prompt_template = ChatPromptTemplate.from_template(template)
        self.db = load_vectorstore()

    def _format_prompt(self, retrieved_context: str) -> str:
        """Formats the prompt with the given context.

        Args:
            retrieved_context (str): The context retrieved from the vector store.

        Returns:
            str: The formatted prompt string.
        """
        return self.prompt_template.format_prompt(
            topic=self.topic,
            context=self.context,
            retrieved_context=retrieved_context,
        ).to_string()

    def generate_question(self) -> str:
        """Generates a question based on the topic and retrieved context.

        Returns:
            str: The generated question string.
        """
        results = self.db.similarity_search(query=self.topic, k=self.k)
        chunks = [doc.page_content for doc in results]

        retrieved_context = "\n\n".join(chunks)

        prompt = self.prompt_template.format_prompt(
            already_asked_questions=self.already_asked_questions,
            topic=self.topic,
            retrieved_context=retrieved_context,
        ).to_string()
        full_output = ""
        for chunk in self.llm.stream(prompt):
            full_output += chunk

        self.already_asked_questions.append(full_output.strip())
        return full_output.strip()
