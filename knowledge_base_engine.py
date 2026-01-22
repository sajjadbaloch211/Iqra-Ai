import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class KnowledgeBaseEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', db_path='iqra_brain.index', metadata_path='iqra_metadata.pkl'):
        self.model = SentenceTransformer(model_name)
        self.db_path = db_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []
        
        # Load existing index if available
        if os.path.exists(self.db_path) and os.path.exists(self.metadata_path):
            self.load_index()

    def ingest_directory(self, directory_path='knowledge_base'):
        """Reads all .txt files from the directory and adds them to the index."""
        documents = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as f:
                    documents.append(f.read())
        
        if not documents:
            print("No new documents found in knowledge_base.")
            return

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50
        )
        
        all_chunks = []
        for doc in documents:
            chunks = text_splitter.split_text(doc)
            all_chunks.extend(chunks)

        print(f"Creating embeddings for {len(all_chunks)} chunks...")
        embeddings = self.model.encode(all_chunks)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Save metadata (the actual text chunks)
        self.metadata = all_chunks
        
        self.save_index()
        print("Knowledge base updated successfully!")

    def save_index(self):
        faiss.write_index(self.index, self.db_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load_index(self):
        self.index = faiss.read_index(self.db_path)
        with open(self.metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=5):
        """Searches the index for the most relevant chunks."""
        if self.index is None:
            return ""
        
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), top_k)
        
        results = [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        return "\n\n".join(results)

if __name__ == "__main__":
    # If run directly, ingest the knowledge_base folder
    engine = KnowledgeBaseEngine()
    engine.ingest_directory()
