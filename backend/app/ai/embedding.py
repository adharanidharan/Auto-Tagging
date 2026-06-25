import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Initialize the model once when the module loads
logger.info("Initializing SentenceTransformer model (all-MiniLM-L6-v2)...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load sentence-transformers model: {e}")
    model = None

def generate_embedding(text: str, model_name: str = "MiniLM Embedding Model") -> list[float]:
    """
    Generates a 384-dimensional vector embedding for the given text.
    If 'Future AI Models' is selected, it will log the model switch and fall back 
    to the high-performance local MiniLM model to maintain functionality without external paid APIs.
    """
    if model is None:
        # Emergency fallback to a dummy vector of 384 dimensions if model didn't load
        logger.warning("Model not loaded, returning mock zero vector")
        return [0.0] * 384

    if model_name != "MiniLM Embedding Model":
        logger.info(f"Model selection '{model_name}' received. Running local MiniLM fallback.")
        
    embedding = model.encode(text)
    return embedding.tolist()
