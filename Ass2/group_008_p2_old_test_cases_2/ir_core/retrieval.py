# Contains functions for document retrieval using Boolean search model.
# Implements linear scan search through document collections.

def linear_boolean_search(term, collection, stopword_filtered=False):
    """
    Search a given collection of documents for all documents that contain a given term, using a simple Boolean model.
    
    Parameters:
        term (str): The search term
        collection (list): A collection of documents to search in
        stopword_filtered (bool): If True, search in filtered_terms; if False, search in terms
    
    Returns:
        list: List of tuples (relevance_score, document) where score is 1 for matches, 0 for non-matches
    """
    
    # Convert search term to lowercase for case-insensitive search
    search_term = term.lower().strip()
    
    # Store results as list of tuples (score, document)
    results = []
    
    # Linear scan through all documents in the collection
    for doc in collection:
        # Choose which terms list to search based on stopword_filtered parameter
        if stopword_filtered:
            # Search in filtered terms (after stopword removal)
            terms_to_search = doc.filtered_terms
        else:
            # Search in original terms
            terms_to_search = doc.terms
        
        # Convert terms to lowercase for comparison
        lowercase_terms = [term.lower() for term in terms_to_search]
        
        # Check if the search term appears in the chosen terms list
        if search_term in lowercase_terms:
            # Document contains the term - add with score 1
            results.append((1, doc))
        else:
            # Document doesn't contain the term - add with score 0
            results.append((0, doc))
    
    return results