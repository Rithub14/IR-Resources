# Contains functions for stop word removal from documents.
# Supports both list-based and frequency-based stop word filtering methods.

def remove_stopwords_by_list(doc, stopwords):
    """
    Remove stopwords from the given document and store the result in doc.filtered_terms.
    
    Parameters:
        doc (Document): The document to clean
        stopwords (set[str]): The stop words to remove
    
    This function modifies the document in-place by setting doc._filtered_terms.
    Leaves doc.terms and doc.raw_text unchanged.
    """
    
    # Filter terms by removing stop words (case-insensitive)
    filtered_terms = []
    for term in doc.terms:
        if term.lower() not in stopwords:
            # Convert to lowercase to match expected test output
            filtered_terms.append(term.lower())
    
    # Store the filtered terms in the document (in-place modification)
    doc._filtered_terms = filtered_terms


def remove_stopwords_by_frequency(doc, collection, rare_frequency, common_frequency):
    """
    Remove stopwords from the given document and store the result in doc.filtered_terms.
    
    Parameters:
        doc (Document): The document to clean
        collection (list[Document]): A collection of documents to use as a reference
        rare_frequency (float): The frequency at which a term is "too rare" to help finding a document
        common_frequency (float): The frequency at which a term is "too common" to hold meaningful semantics
    
    This function modifies the document in-place by setting doc._filtered_terms.
    Leaves doc.terms and doc.raw_text unchanged.
    """
    
    # Compute document frequencies across the entire collection
    term_doc_counts = {}
    
    # Count in how many documents each term appears
    for document in collection:
        # Get unique terms in this document
        unique_terms = set(document.terms)
        for term in unique_terms:
            term_doc_counts[term] = term_doc_counts.get(term, 0) + 1
    
    # Calculate total number of documents
    total_docs = len(collection)
    
    if total_docs == 0:
        # No documents found, set empty filtered terms
        doc._filtered_terms = []
        return
    
    # Create set of stop words (terms that are too common or too rare)
    stopwords = set()
    
    for term, doc_count in term_doc_counts.items():
        # Calculate document frequency (0.0 to 1.0)
        doc_freq = doc_count / total_docs
        
        # Remove terms that are too common or too rare
        if doc_freq >= common_frequency or doc_freq <= rare_frequency:
            stopwords.add(term)
    
    # Filter terms by removing stop words
    filtered_terms = []
    for term in doc.terms:
        if term not in stopwords:
            # Convert to lowercase to match expected test output
            filtered_terms.append(term.lower())
    
    # Store the filtered terms in the document (in-place modification)
    doc._filtered_terms = filtered_terms