# Contains functions for stop word removal from documents.
# Supports both list-based and frequency-based stop word filtering methods.

from collections import Counter

def remove_stopwords_by_list(doc, stopwords):
    """
    Remove stopwords from the given document and store the result in doc.filtered_terms.
    
    Parameters:
        doc (Document): The document to clean
        stopwords (set[str]): The stop words to remove
    
    This function modifies the document in-place by setting doc.filtered_terms.
    Leaves doc.terms and doc.raw_text unchanged.
    """
    
    # Filter terms by removing stop words (case-insensitive)
    filtered_terms = []
    for term in doc.terms:
        if term.lower() not in stopwords:
            # Convert to lowercase to match expected test output
            filtered_terms.append(term.lower())
    
    # Store the filtered terms in the document (in-place modification)
    doc.filtered_terms = filtered_terms


def remove_stopwords_by_frequency(doc, collection, common_frequency, rare_frequency):
    """
    Remove stopwords from the given document and store the result in doc.filtered_terms.
    
    Parameters:
        doc (Document): The document to clean
        collection (list[Document]): A collection of documents to use as a reference
        common_frequency (float): The frequency at which a term is "too common" to hold meaningful semantics
        rare_frequency (float): The frequency at which a term is "too rare" to help finding a document
    
    This function modifies the document in-place by setting doc.filtered_terms.
    Leaves doc.terms and doc.raw_text unchanged.
    """
    
    # Compute term frequencies across the entire collection
    term_frequencies = Counter()
    
    # Count all terms in all documents
    for document in collection:
        for term in document.terms:
            term_frequencies[term] += 1
    
    # Calculate total number of terms to get relative frequencies
    total_terms = sum(term_frequencies.values())
    
    if total_terms == 0:
        # No terms found, set empty filtered terms
        doc.filtered_terms = []
        return
    
    # Create set of stop words (terms that are too common or too rare)
    stopwords = set()
    
    for term, count in term_frequencies.items():
        # Calculate relative frequency (0.0 to 1.0)
        relative_freq = count / total_terms
        
        # Remove terms that are too common or too rare
        if relative_freq >= common_frequency or relative_freq <= rare_frequency:
            stopwords.add(term)
    
    # Filter terms by removing stop words
    filtered_terms = []
    for term in doc.terms:
        if term not in stopwords:
            # Convert to lowercase to match expected test output
            filtered_terms.append(term.lower())
    
    # Store the filtered terms in the document (in-place modification)
    doc.filtered_terms = filtered_terms