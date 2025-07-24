# Contains functions for word stemming using Porter Stemming Algorithm.
# Implements the Porter stemming algorithm as described in stemming_algorithm.txt

import re

def is_consonant(word, i):
    """Check if character at position i is a consonant."""
    if i < 0 or i >= len(word):
        return False
    
    char = word[i].lower()
    if char in 'aeiou':
        return False
    
    # Y is a consonant unless preceded by a consonant
    if char == 'y':
        if i == 0:
            return True
        return not is_consonant(word, i - 1)
    
    return True

def measure(word):
    """Calculate the measure of a word."""
    n = len(word)
    if n == 0:
        return 0
    
    m = 0
    i = 0
    
    # Skip initial consonants
    while i < n and is_consonant(word, i):
        i += 1
    
    # Count VC sequences
    while i < n:
        # Skip vowels
        while i < n and not is_consonant(word, i):
            i += 1
        
        if i >= n:
            break
            
        # Skip consonants
        while i < n and is_consonant(word, i):
            i += 1
        
        m += 1
    
    return m

def contains_vowel(word):
    """Check if word contains a vowel."""
    for i in range(len(word)):
        if not is_consonant(word, i):
            return True
    return False

def ends_double_consonant(word):
    """Check if word ends with double consonant."""
    if len(word) < 2:
        return False
    return (word[-1] == word[-2] and 
            is_consonant(word, len(word) - 1))

def cvc_ending(word):
    """Check if word ends with consonant-vowel-consonant pattern where last consonant is not w, x, or y."""
    if len(word) < 3:
        return False
    
    n = len(word)
    return (is_consonant(word, n - 3) and
            not is_consonant(word, n - 2) and
            is_consonant(word, n - 1) and
            word[-1] not in 'wxy')

def stem_term(word):
    """
    Apply Porter stemming algorithm to a single word.
    
    Parameters:
        word (str): The word to stem
    
    Returns:
        str: The stemmed word
    """
    if len(word) <= 2:
        return word.lower()
    
    word = word.lower()
    
    # Step 1a
    if word.endswith('sses'):
        word = word[:-2]  # sses -> ss
    elif word.endswith('ies'):
        word = word[:-2]  # ies -> i
    elif word.endswith('ss'):
        pass  # ss -> ss
    elif word.endswith('s') and len(word) > 1:
        word = word[:-1]  # s -> (empty)
    
    # Step 1b
    if word.endswith('eed'):
        stem = word[:-3]
        if measure(stem) > 0:
            word = word[:-1]  # eed -> ee
    elif word.endswith('ed'):
        stem = word[:-2]
        if contains_vowel(stem):
            word = stem
            # Apply post-processing
            if word.endswith('at'):
                word += 'e'
            elif word.endswith('bl'):
                word += 'e'
            elif word.endswith('iz'):
                word += 'e'
            elif ends_double_consonant(word) and word[-1] not in 'lsz':
                word = word[:-1]
            elif measure(word) == 1 and cvc_ending(word):
                word += 'e'
    elif word.endswith('ing'):
        stem = word[:-3]
        if contains_vowel(stem):
            word = stem
            # Apply post-processing
            if word.endswith('at'):
                word += 'e'
            elif word.endswith('bl'):
                word += 'e'
            elif word.endswith('iz'):
                word += 'e'
            elif ends_double_consonant(word) and word[-1] not in 'lsz':
                word = word[:-1]
            elif measure(word) == 1 and cvc_ending(word):
                word += 'e'
    
    # Step 1c
    if word.endswith('y') and contains_vowel(word[:-1]):
        word = word[:-1] + 'i'
    
    # Step 2
    step2_rules = [
        ('ational', 'ate'), ('tional', 'tion'), ('enci', 'ence'), ('anci', 'ance'),
        ('izer', 'ize'), ('abli', 'able'), ('alli', 'al'), ('entli', 'ent'),
        ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'), ('ation', 'ate'),
        ('ator', 'ate'), ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'),
        ('ousness', 'ous'), ('aliti', 'al'), ('iviti', 'ive'), ('biliti', 'ble')
    ]
    
    for suffix, replacement in step2_rules:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 0:
                word = stem + replacement
            break
    
    # Step 3
    step3_rules = [
        ('icate', 'ic'), ('ative', ''), ('alize', 'al'), ('iciti', 'ic'),
        ('ical', 'ic'), ('ful', ''), ('ness', '')
    ]
    
    for suffix, replacement in step3_rules:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 0:
                word = stem + replacement
            break
    
    # Step 4
    step4_rules = [
        'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement',
        'ment', 'ent', 'ion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize'
    ]
    
    for suffix in step4_rules:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 1:
                # Special case for 'ion'
                if suffix == 'ion' and len(stem) > 0 and stem[-1] in 'st':
                    word = stem
                elif suffix != 'ion':
                    word = stem
            break
    
    # Step 5a
    if word.endswith('e'):
        stem = word[:-1]
        stem_measure = measure(stem)
        if stem_measure > 1 or (stem_measure == 1 and not cvc_ending(stem)):
            word = stem
    
    # Step 5b
    if measure(word) > 1 and ends_double_consonant(word) and word.endswith('l'):
        word = word[:-1]
    
    return word

def apply_stemming(doc):
    """
    Apply stemming to document terms and store in _stemmed_terms.
    
    Parameters:
        doc (Document): The document to process
    """
    stemmed = [stem_term(term) for term in doc.terms]
    doc._stemmed_terms = stemmed

def apply_stemming_filtered(doc):
    """
    Apply stemming to filtered terms and store in _filtered_stemmed_terms.
    
    Parameters:
        doc (Document): The document to process
    """
    if callable(doc.filtered_terms):
        terms_to_stem = doc.filtered_terms()
    else:
        terms_to_stem = doc.filtered_terms
    
    stemmed = [stem_term(term) for term in terms_to_stem]
    doc._filtered_stemmed_terms = stemmed