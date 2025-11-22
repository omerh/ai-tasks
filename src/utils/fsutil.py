import os


def create_conversation_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)
