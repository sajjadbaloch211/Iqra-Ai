from knowledge_base_engine import KnowledgeBaseEngine
import os
import time

def sync():
    print("🧠 IQRA VIRTUAL BRAIN - SYNCHRONIZER")
    print("------------------------------------")
    
    if not os.path.exists('knowledge_base'):
        os.makedirs('knowledge_base')
        print("Folder 'knowledge_base' created. Please put your .txt files there.")
        return

    start_time = time.time()
    engine = KnowledgeBaseEngine()
    
    print("Scanning knowledge_base folder for new data...")
    engine.ingest_directory('knowledge_base')
    
    end_time = time.time()
    print(f"------------------------------------")
    print(f"✅ Sync Complete! Time taken: {end_time - start_time:.2f} seconds.")
    print(f"Chatbot is now updated with the latest university information.")

if __name__ == "__main__":
    sync()
