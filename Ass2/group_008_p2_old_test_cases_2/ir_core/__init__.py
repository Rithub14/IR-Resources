# IR Core Package 
# This package contains all the core functionality for the IR system:
# - document: Document class definition
# - collection: Document collection downloading and parsing
# - retrieval: Boolean search functionality  
# - stopwords: Stop word removal (list-based and frequency-based)

# Make core classes and functions available at package level
from document import Document
from .collection import load_documents_from_url
from .retrieval import linear_boolean_search
from .stopwords import remove_stopwords_by_list, remove_stopwords_by_frequency

__all__ = [
    'Document',
    'load_documents_from_url', 
    'linear_boolean_search',
    'remove_stopwords_by_list',
    'remove_stopwords_by_frequency'
]