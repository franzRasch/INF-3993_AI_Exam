import re
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def remove_intro_until_task(text: str) -> str:
    """
    Removes everything before 'Task 1:' in the document.
    """
    marker = "Task 1:"
    index = text.find(marker)
    return text[index:] if index != -1 else text


def remove_task_and_question_prefix(text: str) -> str:
    """
    Removes prefixes like 'Task 1: b)' or 'Task 2: a)' from the beginning of the text.
    """
    return re.sub(r"^\s*Task\s*\d+:\s*[a-h]\)\s*", "", text, flags=re.IGNORECASE)


def split_documents_by_exam_question(documents: List[Document]) -> List[Document]:
    """
    Splits documents into individual exam questions based on 'Task N:' and 'a)', 'b)', etc.
    Each returned Document contains a single question as one chunk.
    """
    question_chunks = []

    for doc in documents:
        cleaned_text = remove_intro_until_task(doc.page_content)

        # Split by each task (e.g., Task 1:, Task 2:) using a regex
        task_blocks = re.split(r"(Task\s*\d+:)", cleaned_text)

        # Combine the task label and content back together
        tasks = []
        for i in range(1, len(task_blocks), 2):
            task_label = task_blocks[i].strip()
            task_content = task_blocks[i + 1].strip()
            tasks.append((task_label, task_content))

        for task_label, task_content in tasks:
            # Split task content into individual questions based on a), b), etc.
            parts = re.split(r"\n?\s*([a-h]\))", task_content)

            if len(parts) <= 1:
                full_chunk = f"{task_label} {task_content}".strip()
                question_chunks.append(
                    Document(page_content=full_chunk, metadata=doc.metadata)
                )
                continue

            # Recombine: prefix + question label + question content
            prefix = f"{task_label}"
            for i in range(1, len(parts) - 1, 2):
                label = parts[i].strip()
                content = parts[i + 1].strip()
                chunk_text = f"{prefix} {label} {content}".strip()
                chunk_text = remove_task_and_question_prefix(chunk_text)

                question_chunks.append(
                    Document(page_content=chunk_text, metadata=doc.metadata)
                )

    return question_chunks


def split_documents(
    documents: List[Document], chunk_size=1000, overlap=200
) -> List[Document]:
    """
    Fallback splitter for general-purpose documents using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def smart_split_documents(
    documents: List[Document], is_exam: bool = False
) -> List[Document]:
    """
    Smart splitting: If it's an exam, split by task and question; otherwise, use recursive chunking.
    """
    if is_exam:
        return split_documents_by_exam_question(documents)
    else:
        return split_documents(documents)
