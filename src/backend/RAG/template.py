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

    Now write your question and output it **only** as valid JSON** with a single key `"question"`.  
    Example:
    {{"question":"What is a vector clock?"}}
    """
    return template


def create_answer_template():
    template = """
    You are an expert in {topic}.
    Answer the following question in **no more than 100 characters**.
    Provide **only** the answer—no labels, explanations, or extra text.

    Question: {generated_question}

    Output your response **only** as valid JSON with a single key `"answer"`. Do not use any other keys or formatting.
    Example:
    {{"answer":"A vector clock is a way to order events in distributed systems."}}
    """
    return template
