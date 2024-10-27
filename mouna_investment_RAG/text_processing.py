from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        document_text = f.read()

    # Split the document for better indexing
    text_splitter = RecursiveCharacterTextSplitter()
    documents_split = text_splitter.split_text(document_text)
    
    return documents_split