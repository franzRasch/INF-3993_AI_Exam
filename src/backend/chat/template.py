def chat_template():
    template = """
    You are a professor in the field of {topic}.
    Your task is to respond to the user's input based on the provided context.
    Please keep your response concise and relevant to the topic, as short as possible.

    [BEGIN PREVIOUS CONTEXT]
    {context}
    [END PREVIOUS CONTEXT]

    User Input that shall be answered: {user_input}
    """
    return template