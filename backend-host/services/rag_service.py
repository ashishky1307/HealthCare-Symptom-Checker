"""RAG (Retrieval-Augmented Generation) service for medical knowledge."""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import hashlib

try:
    from pypdf import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    logger = logging.getLogger(__name__)
    logger.warning("pypdf not installed. PDF support disabled.")

logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG service for retrieving relevant medical knowledge.
    Uses ChromaDB for vector storage and SentenceTransformer for embeddings.
    """
    
    def __init__(
        self,
        knowledge_base_path: str,
        persist_directory: str = "./data/chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "medical_knowledge"
    ):
        """
        Initialize RAG service.
        
        Args:
            knowledge_base_path: Path to medical knowledge documents
            persist_directory: Directory to persist ChromaDB
            embedding_model: SentenceTransformer model name
            collection_name: ChromaDB collection name
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model
        self.collection_name = collection_name
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at: {persist_directory}")
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
            )
            logger.info(f"✅ Loaded existing collection: {collection_name}")
        except Exception:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"description": "Medical knowledge base for symptom analysis"}
            )
            logger.info(f"✅ Created new collection: {collection_name}")
            # Index documents on first run
            self._index_documents()
    
    def _index_documents(self):
        """Index all documents from knowledge base into ChromaDB."""
        if not self.knowledge_base_path.exists():
            logger.error(f"Knowledge base path not found: {self.knowledge_base_path}")
            return
        
        logger.info("Indexing medical knowledge documents...")
        
        # Get all text and PDF files
        text_files = list(self.knowledge_base_path.glob("*.txt"))
        pdf_files = list(self.knowledge_base_path.glob("*.pdf")) if PDF_SUPPORT else []
        
        all_files = text_files + pdf_files
        
        if not all_files:
            logger.warning("No text or PDF files found in knowledge base")
            return
        
        total_chunks = 0
        for file_path in all_files:
            try:
                # Read content based on file type
                if file_path.suffix.lower() == '.pdf':
                    content = self._extract_pdf_text(file_path)
                    if not content:
                        logger.warning(f"No text extracted from PDF: {file_path.name}")
                        continue
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                
                # Split content into chunks
                chunks = self._split_into_chunks(content, file_path.stem)
                
                if chunks:
                    # Prepare data for ChromaDB
                    documents = [chunk['text'] for chunk in chunks]
                    metadatas = [chunk['metadata'] for chunk in chunks]
                    ids = [chunk['id'] for chunk in chunks]
                    
                    # Generate embeddings
                    embeddings = self.embedding_model.encode(
                        documents,
                        show_progress_bar=True,
                        convert_to_numpy=True
                    ).tolist()
                    
                    # Add to collection
                    self.collection.add(
                        documents=documents,
                        embeddings=embeddings,
                        metadatas=metadatas,
                        ids=ids
                    )
                    
                    total_chunks += len(chunks)
                    logger.info(f"✓ Indexed {len(chunks)} chunks from {file_path.name}")
            
            except Exception as e:
                logger.error(f"Error indexing {file_path.name}: {e}")
        
        logger.info(f"✅ Total indexed chunks: {total_chunks}")
    
    def _split_into_chunks(
        self,
        content: str,
        source: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Split document content into overlapping chunks.
        
        Args:
            content: Document text content
            source: Source document name
            chunk_size: Target size of each chunk in characters
            overlap: Number of overlapping characters between chunks
        
        Returns:
            List of chunk dictionaries with text, metadata, and id
        """
        # Split by sections (using == markers)
        sections = content.split('\n====================\n')
        
        chunks = []
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Extract section title (first line)
            lines = section.split('\n', 1)
            title = lines[0].strip() if lines else "Unknown"
            section_content = lines[1].strip() if len(lines) > 1 else section
            
            # If section is small enough, keep as single chunk
            if len(section_content) <= chunk_size:
                chunk_id = self._generate_chunk_id(source, title, 0)
                chunks.append({
                    'text': section_content,
                    'metadata': {
                        'source': source,
                        'section': title,
                        'chunk_index': 0
                    },
                    'id': chunk_id
                })
            else:
                # Split large sections into smaller chunks
                words = section_content.split()
                current_chunk = []
                current_size = 0
                chunk_index = 0
                
                for word in words:
                    word_size = len(word) + 1  # +1 for space
                    
                    if current_size + word_size > chunk_size and current_chunk:
                        # Save current chunk
                        chunk_text = ' '.join(current_chunk)
                        chunk_id = self._generate_chunk_id(source, title, chunk_index)
                        chunks.append({
                            'text': chunk_text,
                            'metadata': {
                                'source': source,
                                'section': title,
                                'chunk_index': chunk_index
                            },
                            'id': chunk_id
                        })
                        
                        # Start new chunk with overlap
                        overlap_words = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                        current_chunk = overlap_words + [word]
                        current_size = sum(len(w) + 1 for w in current_chunk)
                        chunk_index += 1
                    else:
                        current_chunk.append(word)
                        current_size += word_size
                
                # Add remaining chunk
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    chunk_id = self._generate_chunk_id(source, title, chunk_index)
                    chunks.append({
                        'text': chunk_text,
                        'metadata': {
                            'source': source,
                            'section': title,
                            'chunk_index': chunk_index
                        },
                        'id': chunk_id
                    })
        
        return chunks
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text content
        """
        if not PDF_SUPPORT:
            logger.error("PDF support not available. Install pypdf package.")
            return ""
        
        try:
            reader = PdfReader(str(pdf_path))
            text_content = []
            
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"\n--- Page {page_num} ---\n{text}")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num} from {pdf_path.name}: {e}")
            
            full_text = "\n".join(text_content)
            logger.info(f"✓ Extracted {len(full_text)} characters from {pdf_path.name} ({len(reader.pages)} pages)")
            return full_text
        
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path.name}: {e}")
            return ""
    
    def _generate_chunk_id(self, source: str, section: str, index: int) -> str:
        """Generate unique ID for a chunk."""
        content = f"{source}_{section}_{index}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def retrieve_relevant_context(
        self,
        query: str,
        n_results: int = 5,
        min_relevance_score: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from knowledge base.
        
        Args:
            query: Search query (symptoms or medical terms)
            n_results: Number of results to retrieve
            min_relevance_score: Minimum relevance score (0-1)
        
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(
                query,
                convert_to_numpy=True
            ).tolist()
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            relevant_chunks = []
            
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # Convert distance to similarity score (cosine similarity)
                    # ChromaDB uses L2 distance by default
                    # For normalized embeddings: similarity = 1 - (distance^2 / 2)
                    similarity = 1 - (distance ** 2 / 2)
                    
                    if similarity >= min_relevance_score:
                        relevant_chunks.append({
                            'text': doc,
                            'source': metadata.get('source', 'unknown'),
                            'section': metadata.get('section', 'unknown'),
                            'relevance_score': similarity,
                            'rank': i + 1
                        })
            
            logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks for query: {query[:50]}...")
            return relevant_chunks
        
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def format_context_for_llm(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        max_chunks: int = 3
    ) -> str:
        """
        Format retrieved chunks into context string for LLM.
        
        Args:
            retrieved_chunks: List of retrieved document chunks
            max_chunks: Maximum number of chunks to include
        
        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return ""
        
        # Take top chunks
        top_chunks = retrieved_chunks[:max_chunks]
        
        context_parts = ["RELEVANT MEDICAL KNOWLEDGE:\n"]
        
        for i, chunk in enumerate(top_chunks, 1):
            context_parts.append(
                f"\n[Source: {chunk['source']} - {chunk['section']}]\n"
                f"{chunk['text']}\n"
            )
        
        return "\n".join(context_parts)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base collection."""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection_name,
                'embedding_model': self.embedding_model_name
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def reset_collection(self):
        """Reset the collection (useful for re-indexing)."""
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Medical knowledge base for symptom analysis"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
            
            self._index_documents()
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")


# Singleton instance
_rag_service_instance: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service singleton instance."""
    global _rag_service_instance
    
    if _rag_service_instance is None:
        # Get paths
        current_dir = Path(__file__).parent.parent
        knowledge_base_path = current_dir / "data" / "medical_knowledge"
        persist_directory = current_dir / "data" / "chroma_db"
        
        _rag_service_instance = RAGService(
            knowledge_base_path=str(knowledge_base_path),
            persist_directory=str(persist_directory)
        )
    
    return _rag_service_instance
