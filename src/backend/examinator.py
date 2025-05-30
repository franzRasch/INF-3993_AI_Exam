import json
from template import create_answer_review_template
from question_generator_base import QuestionGeneratorBase
import whisper
from fastapi import UploadFile
import os
import tempfile


class Examinator(QuestionGeneratorBase):
    """A class for conducting oral examinations using a language model.

    Args:
        QuestionGeneratorBase : Base class for generating questions based on a topic and context.
    """

    def __init__(
        self,
        topic: str,
        model_name="llama3.2:latest",
        whisper_model="base",
        k: int = 3,
        number_of_questions: int = 5,
    ):
        super().__init__(topic, model_name, k, number_of_questions)
        self.whisper_model = whisper.load_model(whisper_model)

    def generate_questions(self) -> list[str]:
        """Generates a list of questions based on the topic and context.

        Returns:
            list[str]: A list of generated question strings.
        """
        questions = []
        for _ in range(self.number_of_questions):
            raw_output = self.generate_question()
            try:
                parsed = json.loads(raw_output)
                questions.append(parsed["question"])
            except json.JSONDecodeError:
                print(f"Failed to parse question: {raw_output}")

        return questions

    def transcribe_answer(self, student_answer: UploadFile) -> str:
        """Transcribes a student's audio answer to text using Whisper.

        Args:
            student_answer (UploadFile): The student's audio answer.

        Returns:
            str: The transcribed text of the student's answer.
        """

        file_content = student_answer.file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            result = self.whisper_model.transcribe(tmp_path, language="en")
            result_text = result["text"]
            print("Transcribed text:", result_text)
            return result_text
        finally:
            os.remove(tmp_path)

    def review_oral_answer(self, question: str, student_answer: UploadFile) -> str:
        """Reviews a student's oral answer to a question.

        Args:
            question (str): The question being answered.
            student_answer (str): The student's answer.

        Returns:
            str: The feedback on the student's answer, formatted as JSON.
        """

        # Transcribe the student's answer from audio to text
        transcribed_answer = self.transcribe_answer(student_answer)

        prompt = create_answer_review_template().format(
            topic=self.topic,
            student_answer=transcribed_answer,
            generated_question=question,
            retrieved_context=self.context,
        )
        full_output = ""
        print(question)

        for chunk in self.llm.stream(prompt):
            full_output += chunk

        return full_output

    def review_text_answer(self, question: str, student_answer: str) -> str:
        """Reviews a student's text answer to a question.

        Args:
            question (str): The question being answered.
            student_answer (str): The student's answer.

        Returns:
            str: The feedback on the student's answer.
        """

        prompt = create_answer_review_template().format(
            topic=self.topic,
            student_answer=student_answer,
            generated_question=question,
            retrieved_context=self.context,
        )
        full_output = ""

        for chunk in self.llm.stream(prompt):
            full_output += chunk

        return full_output
