import os
from typing import Any

from dotenv import load_dotenv
from langchain.chat_models import  ChatOpenAI

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain.memory import ZepMemory

from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from os.path import join, dirname
from dotenv import load_dotenv
from prompt import TEMPLATE_SYSTEM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from uuid import uuid4
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# str(uuid4())
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
class Chatbot:
    def __init__(self, 
                 session_id,
                 model_name ="OpenAI Embedding"):
        self.memory = ConversationBufferWindowMemory(
                                                memory_key='chat_history', 
                                                return_messages=True, 
                                                input_key="question")
        # self.zep_memory = 
        self.session_id = session_id  # This is a unique identifier for the user/session
        self.session_id ="996171c3-747a-439c-91b5-1ce4ed4ecbca"
        # Initialize the Zep Memory Class
        self.bi_enc_dict = {
                        'OpenAI Embedding': 'openai-gpt',
                        'sbert':"keepitreal/vietnamese-sbert"
                    }
        self.CHAIN_TYPE = 'stuff' 
        self.embeddings = self.gen_embeddings(model_name)
        self.vectorstore = FAISS.load_local("faiss_index", self.embeddings)
        self.chain = self.load_retrieval_chain(self.vectorstore, CHAIN_TYPE=self.CHAIN_TYPE)

    def __call__(self, *args: Any) -> Any:
        # load_dotenv()
        return self.gen_qa_response(*args, self.chain)['result']
    
    def load_prompt(self, chain_type='refine'):
        if chain_type == 'refine':
            system_template=TEMPLATE_SYSTEM
        elif chain_type == "map_reduce":
            system_template=TEMPLATE_SYSTEM
        elif chain_type == 'stuff':
            system_template = TEMPLATE_SYSTEM
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
            
        return prompt

    def gen_embeddings(self, model_name):
        '''Generate embeddings for given model'''

        embedd = OpenAIEmbeddings(
                                    model=os.getenv("EMBED_OPENAI_MODEL")
                                 )

        return embedd


    def load_retrieval_chain(self, vectorstore, CHAIN_TYPE='refine'):

        '''Load Chain'''

        # Initialize the RetrievalQA chain with streaming output
        QA_CHAIN_PROMPT = PromptTemplate.from_template(TEMPLATE_SYSTEM)

        chat_llm=ChatOpenAI(
                        temperature=0.7, 
                        model_name=os.getenv("OPENAI_MODEL")
                    )

        chain = RetrievalQA.from_chain_type(
            chat_llm,
            retriever=vectorstore.as_retriever(search_kwargs={'k':5}),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT,
                                # "memory": self.memory
                                },
        )

        return chain

    def run_qa_chain(self, query,_chain):
        '''Run the QnA chain'''
        answer = _chain({"query": query})
        return answer


    def gen_qa_response(self, user_question, _chain):
        '''Generate responses from query'''
        result = {}
        if user_question:
            result = self.run_qa_chain(user_question,_chain)
            # print(result)
        return result
    
# # #Usage:    
# import time
# start = time.time()
# response = Chatbot(str(uuid4()))
# ans = response("Con trai tôi có dấu hiệu ít nói, chậm phát triển thì có phải bị tự kỷ không?")
# print(time.time() - start)
# print(ans)
  
