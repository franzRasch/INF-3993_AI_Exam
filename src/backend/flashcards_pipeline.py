import os
from local_loader import load_documents


def save_document(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)


def is_parsed(file_name: str, path: str) -> bool:
    file_path = os.path.join(path, file_name + ".txt")
    if os.path.exists(file_path):
        return True
    return False


def get_filename(path: str) -> str:
    path_without_ext = path.split(".")[0]
    file_name = path_without_ext.split("/")[-1]
    return file_name


def parse_all():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    file_path = os.path.join(base_dir, "data", "INF-3701")
    parsed_path = os.path.join(base_dir, "data", "INF-3701/txt")
    if not os.path.exists(parsed_path):
        os.makedirs(parsed_path)
    docs = load_documents(file_path)
    for doc in docs:
        file_name = get_filename(doc.metadata["source"])
        if not is_parsed(file_name, parsed_path):
            doc_path = os.path.join(parsed_path, file_name + ".txt")
            save_document(doc_path, doc.page_content)
    return parsed_path


parse_all()
