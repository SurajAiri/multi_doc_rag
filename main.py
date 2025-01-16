from src.llm.model import ModelRunner
from src.helper.doc_db import DocDb
from src.helper.doc_loader import DocLoader
import os
def main():

    print("current working dir: ",os.getcwd(),"\n")
    DB_PATH = "output/db/chroma"
    
    # Load the documents
    # docs = DocLoader.load_pdf("data/Think_Straight.pdf")

    # Create a document database
    doc_db = DocDb(DB_PATH)

    # Add the documents to the database
    # doc_db.add_document(docs)


    # Create the model runner
    model = ModelRunner( doc_db=doc_db)

    # Ask a question
    question = "What is the book about?"
    response = model.ask(question)

    print(response['answer'])

if __name__ == "__main__":
    main()