import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    CSVLoader
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain

# 加载环境变量
load_dotenv(encoding='utf-8')


class EnterpriseKnowledgeBase:
    """企业级知识库系统"""

    def __init__(self, config):
        self.config = config
        self.vectorstore = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

    def load_documents(self, paths):
        """加载多种格式的文档"""
        documents = []

        for path in paths:
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
            elif path.endswith('.docx'):
                loader = Docx2txtLoader(path)
            elif path.endswith('.md'):
                loader = UnstructuredMarkdownLoader(path)
            elif path.endswith('.csv'):
                loader = CSVLoader(path)
            else:
                continue

            docs = loader.load()
            # 添加元数据
            for doc in docs:
                doc.metadata['source'] = path
                doc.metadata['timestamp'] = datetime.now()

            documents.extend(docs)
            logging.info(f"加载文档：{path}, 共{len(docs)}页")

        return documents

    def process_documents(self, documents):
        """处理文档：分割、清洗、嵌入"""
        # 智能文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.get('chunk_size', 1000),
            chunk_overlap=self.config.get('chunk_overlap', 200),
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)
        logging.info(f"分割成{len(chunks)}个文本块")

        # 创建嵌入
        if self.config.get('embedding_model') == 'huggingface':
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            embeddings = OpenAIEmbeddings(
                model="text-embedding-v1",
                api_key=os.getenv("QIANWEN_API_KEY"),
                base_url=os.getenv("QIANWEN_BASE_URL")
            )

        # 存储到向量数据库
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./enterprise_kb"
        )

        return self.vectorstore

    def create_retriever(self):
        """创建检索器"""
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 20,
                "lambda_mult": 0.5
            }
        )
        return retriever

    def build_qa_system(self):
        """构建问答系统"""
        retriever = self.create_retriever()

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(
                model_name=os.getenv("QIANWEN_MODEL_NAME"),
                temperature=0.2,
                api_key=os.getenv("QIANWEN_API_KEY"),
                base_url=os.getenv("QIANWEN_BASE_URL")
            ),
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )

        return self.qa_chain

    def ask(self, question, user_id=None):
        """问答接口"""
        if not self.qa_chain:
            self.build_qa_system()

        # 添加用户标识
        if user_id:
            question = f"[用户ID: {user_id}] {question}"

        result = self.qa_chain({"question": question})

        # 格式化输出
        response = {
            "answer": result["answer"],
            "sources": self._format_sources(result.get("source_documents", [])),
            "chat_history": result.get("chat_history", [])
        }

        return response

    def _format_sources(self, docs):
        """格式化来源文档"""
        sources = []
        seen = set()

        for doc in docs:
            source = {
                "file": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "preview": doc.page_content[:200] + "..."
            }

            # 去重
            key = (source["file"], source["page"])
            if key not in seen:
                sources.append(source)
                seen.add(key)

        return sources[:3]


def scan_documents_folder(folder_path="./documents"):
    """扫描文档目录，返回所有支持的文件路径"""
    supported_extensions = ('.pdf', '.docx', '.md', '.csv', '.txt')
    documents = []
    
    # 如果目录不存在，创建它
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 已创建文档目录：{os.path.abspath(folder_path)}")
        print("   请将文档文件放入此目录后重新运行")
        return []
    
    # 遍历目录
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            full_path = os.path.join(folder_path, filename)
            documents.append(full_path)
    
    return documents


# 使用示例
if __name__ == "__main__":
    config = {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "embedding_model": "openai",
        "vectorstore": "chroma"
    }

    kb = EnterpriseKnowledgeBase(config)
    
    # 方式1：自动扫描 documents 目录
    doc_folder = "./documents"
    doc_paths = scan_documents_folder(doc_folder)
    
    # 方式2：手动指定文件路径（与方式1二选一）
    # doc_paths = [
    #     "./documents/公司手册.pdf",
    #     "./documents/产品文档.md",
    #     "./documents/技术规范.docx"
    # ]
    
    if not doc_paths:
        print(f"⚠️  在 {os.path.abspath(doc_folder)} 目录下未找到文档")
        print("   支持的格式：.pdf, .docx, .md, .csv, .txt")
        exit(1)
    
    print(f"📚 找到 {len(doc_paths)} 个文档文件：")
    for path in doc_paths:
        print(f"   - {path}")
    print()

    # 加载文档
    docs = kb.load_documents(doc_paths)
    
    if not docs:
        print("❌ 未能加载任何文档内容")
        exit(1)

    # 处理文档
    kb.process_documents(docs)
    
    # 交互式问答
    print("\n" + "="*50)
    print("💬 开始问答（输入 'quit' 退出）")
    print("="*50 + "\n")
    
    while True:
        question = input("❓ 请输入问题：").strip()
        if question.lower() == 'quit':
            break
        if not question:
            continue
            
        response = kb.ask(question)
        print(f"\n🤖 答案：{response['answer']}\n")
        
        if response['sources']:
            print("📄 参考来源：")
            for i, source in enumerate(response['sources'], 1):
                print(f"   {i}. {source['file']} (第{source['page']}页)")
                print(f"      预览：{source['preview'][:100]}...")
            print()
