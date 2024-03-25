import os
import openai
from os.path import join, dirname
from dotenv import load_dotenv
import validators
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import AzureOpenAIEmbeddings

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from utils import urls
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def read_pdf(path):
    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()

def load_docs(path_files, url=False):
    documents = []
    if not url:
        print("`Reading doc ...`")
        for path in path_files:
            print(path)
            file_extension = os.path.splitext(path)[1]
            if file_extension == ".pdf":
                print(path)
                # pages = PyPDFLoader(path).load()
                pages = read_pdf(path)
            elif validators.url(path):
                print("Reading url...")
                pages = WebBaseLoader(path).load()
                # documents.extend(loader.load())
                # print(pages)
            else:
                print("File extension not supported")
            pages_context = "\n\n".join([doc.page_content.replace("\n", " ") for doc in pages])
            # pages_context = pages
            texts = text_splitter.split_text(pages_context)
            if str(pages[0].metadata['source']).split("\\")[0] == "docs":
                pages[0].metadata['source'] = ""
            documents.extend(["sources document: "+ str(pages[0].metadata['source']) +" "+ text for text in texts])
            # documents.extend(texts)
    return documents
chunk_size = 1000 #characters in each chunk
overlap = 100
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=overlap)
list_urls = urls
texts = load_docs(list_urls)
num_chunks = len(texts)
print(f"Number of text chunks: {num_chunks}")
print(text_splitter)
model_name = "OpenAI Embedding"

if model_name == "OpenAI Embedding":
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBED_OPENAI_MODEL")
                            )
    # print("len embedding:", len(embeddings[0]))
    vectorstore = FAISS.from_texts(texts, embedding=embeddings)
    vectorstore.save_local("faiss_index")
elif model_name == "sbert":
    embeddings = HuggingFaceEmbeddings(model_name="keepitreal/vietnamese-sbert")
    vectorstore = FAISS.from_texts(texts, embedding=embeddings)
    vectorstore.save_local("faiss_index_sbert")
print(vectorstore.index.ntotal)
print("save sucessfully")
