def create_template():
    template = """
    """


def create_question_template():
    template = """
    You are a professor in the field of {topic}.
    Your task is to write **one** exam-style question under 100 characters.
    Do **not** include an answer, explanations, or any extra text.
    Use these examples for style:

    [BEGIN EXAMPLE QUESTIONS]
    {retrieved_context}
    [END EXAMPLE QUESTIONS]

    Do not write any question that has already been asked, listed below.
    [BEGIN ALREADY ASKED QUESTIONS]
    {already_asked_questions}
    [END ALREADY ASKED QUESTIONS]

    Now write your question and output it **only** as valid JSON** with a single key `"question"`.
    Do not use any other keys or formatting, and only include the question itself.
    Example:
    {{"question":"What is a vector clock?"}}
    """
    return template


def create_answer_template():
    template = """
    You are an expert in {topic}.
    Answer the following question in **no more than 100 characters**.
    Provide **only** the answer—no labels, explanations, or extra text.
    Use the following context to answer the question:

    [BEGIN CONTEXT]
    {context}
    [END CONTEXT]

    Question: {generated_question}

    Output your response **only** as valid JSON with a single key `"answer"`. Do not use any other keys or formatting.
    Example:
    {{"answer":"A vector clock is a way to order events in distributed systems."}}
    """
    return template


def create_answer_review_template():
    template = """
    You are an examiner in the field of {topic}.
    Your task is to review the answer to the following question, as if it was given by a student in an oral exam.
    The review should be based on the {retrieved_context}.

    Question: {generated_question}
    Answer: {student_answer}

    Review the answer and provide feedback in **no more than 100 characters**.
    Review should contain passed/not passed and a short reason.
    Provide **only** the feedback—no labels, explanations, or extra text.
    Output your response **only** as valid JSON with a single key `"feedback"`. Do not use any other keys or formatting.
    Example:
    {{"feedback":"Passed: The answer is correct and concise."}}
    """
    return template
