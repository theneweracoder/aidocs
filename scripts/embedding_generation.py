from sentence_transformers import SentenceTransformer

def generate_embeddings(doc_1, doc_2):
    """
    Generates embeddings for two documents using a Sentence Transformer model.
    The model is loaded from the internet.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    
    # Generate embeddings for both documents
    doc_1_embedding = model.encode(doc_1)
    doc_2_embedding = model.encode(doc_2)
    
    return doc_1_embedding, doc_2_embedding