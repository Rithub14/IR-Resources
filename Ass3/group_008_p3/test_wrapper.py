# Information Retrieval - Practical Task 2
# Wrapper for Unit Tests
# Version 1.0 (2025-05-24)

# You must implement this file so that the test suite can run your code.
# This file acts as a bridge between your individual implementation and the expected interface.

# You are free to organize your own code however you want - but make sure
# that the following three functions are importable and behave as specified below.

from document import Document
from ir_core.collection import load_documents_from_url
from ir_core.retrieval import linear_boolean_search, vector_space_search, precision_recall
from ir_core.stopwords import remove_stopwords_by_list, remove_stopwords_by_frequency
from ir_core.stemming import stem_term, apply_stemming, apply_stemming_filtered

