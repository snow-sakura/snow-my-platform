# 基于公司文档的QA系统
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA

# 加载环境变量
load_dotenv()

# 1. 加载文档
print("📚 加载文档...")
loader = DirectoryLoader(
    "docs/",
    glob="**/*.txt",
    show_progress=True,
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()

# 2. 分割文档
print("✂️ 分割文档...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
texts = text_splitter.split_documents(documents)

# 3. 创建向量数据库
print("🏠 创建向量数据库...")
embeddings = OpenAIEmbeddings(
    model="text-embedding-v1",
    api_key=os.getenv("QIANWEN_API_KEY"),
    base_url=os.getenv("QIANWEN_BASE_URL")
)
vectorstore = Chroma.from_documents(
    documents=texts, embedding=embeddings,
    persist_directory="./company_docs_db"
)

# 4. 创建QA链
print("🔗 创建QA链...")
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model_name=os.getenv("QIANWEN_MODEL_NAME"),
        temperature=0.7,
        api_key=os.getenv("QIANWEN_API_KEY"),
        base_url=os.getenv("QIANWEN_BASE_URL")
    ),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 3}
    ),
    return_source_documents=True
)
# 5. 交互式提问
print('\n ☎️ 开始问答(输入"quit"退出)\n')
while True:
    query = input("❓️ 你: ")
    if query.lower() == "quit":
        break
    
    result = qa_chain({"query": query})
    print(f"\n 🤖 机器人:{result['result']}\n")

    # 显示来源
    if result.get('source_documents'):
        print("📄 参考文档：")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f" {i}. {doc.metadata.get('source', 'Unknown')}")
        print()
