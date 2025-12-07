"""Script to re-index the medical knowledge base with new documents."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.rag_service import get_rag_service
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def reindex_knowledge_base():
    """Re-index the medical knowledge base."""
    logger.info("Starting re-indexing of medical knowledge base...")
    
    try:
        # Get RAG service instance
        rag_service = get_rag_service()
        
        # Reset and re-index
        logger.info("Resetting collection and re-indexing all documents...")
        rag_service.reset_collection()
        
        # Get stats
        stats = rag_service.get_collection_stats()
        logger.info(f"✅ Re-indexing complete!")
        logger.info(f"   Total documents: {stats.get('total_documents', 0)}")
        logger.info(f"   Collection: {stats.get('collection_name', 'unknown')}")
        logger.info(f"   Embedding model: {stats.get('embedding_model', 'unknown')}")
        
    except Exception as e:
        logger.error(f"❌ Error during re-indexing: {e}")
        raise

if __name__ == "__main__":
    reindex_knowledge_base()
