from document_loader import load_documents
from embedding_generation import generate_embeddings
from comparison import compare_documents, detailed_comparison
from dotenv import load_dotenv
import os
import warnings

# Suppress the Transformers warning about cache migration
warnings.filterwarnings("ignore", message="The cache for model files in Transformers v4.22.0 has been updated")
warnings.filterwarnings("ignore", message="huggingface/tokenizers: The current process just got forked")

# Set environment variable to disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Load the documents from the data folder
doc_1, doc_2 = load_documents('data/2020.pdf', 'data/2023.pdf')

# Generate embeddings using Sentence Transformers
doc_1_embedding, doc_2_embedding = generate_embeddings(doc_1, doc_2)

# Perform an initial similarity comparison
similarity_score = compare_documents(doc_1_embedding, doc_2_embedding)
print(f"Similarity Score: {similarity_score:.4f}")

# Use OpenAI API for detailed comparison
detailed_result = detailed_comparison(doc_1, doc_2, openai_api_key)
print(f"Detailed Comparison Result: \n{detailed_result}")