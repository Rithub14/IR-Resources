# Contains functions for downloading and parsing document collections.
# Supports downloading from URLs and parsing multi-story text files into individual documents.

import urllib.request
import re
from document import Document

def load_documents_from_url(url, author, origin, start_line, end_line, search_pattern):
    """
    Download a text from the given URL, extract stories/chapters and return them as Document objects.
    
    Parameters:
        url (str): The URL to the Project Gutenberg text file
        author (str): The author name to assign to each document
        origin (str): The title of the containing collection, to assign to each document
        start_line (int): Line number from where to start searching
        end_line (int): Line number until which to search
        search_pattern (Pattern[str]): RE pattern where the 1st capture group contains the title 
                                      and the 2nd the text of the document
    
    Returns:
        list[Document]: List of parsed documents
    """
    
    # Download the file content
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading file: {e}")
        return []
    
    # Split content into lines
    lines = content.split('\n')
    
    # Extract the specified line range
    if end_line is None:
        end_line = len(lines)
    
    # Ensure valid line ranges
    start_line = max(0, start_line)
    end_line = min(len(lines), end_line)
    
    if start_line >= end_line:
        print("Invalid line range specified")
        return []
    
    # Get the text within the specified range
    text_content = '\n'.join(lines[start_line:end_line])
    
    # Normalize line endings for consistent regex matching
    normalized_content = text_content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Use regex pattern to find all matches
    matches = search_pattern.findall(normalized_content)
    
    documents = []
    document_id = 0
    
    for match in matches:
        # Extract title and content from regex groups
        if len(match) >= 2:
            story_title = match[0].strip()
            story_content = match[1].strip()
        else:
            # Skip invalid matches
            continue
        
        # Remove line breaks from content for raw_text
        clean_raw_text = story_content.replace('\n', ' ').strip()
        
        # Tokenize into terms (alphanumeric + apostrophes, lowercase)
        terms = re.findall(r"[A-Za-z0-9']+", clean_raw_text.lower())
        
        # Create Document object
        doc = Document(
            document_id=document_id,
            title=story_title,
            raw_text=clean_raw_text,
            terms=terms,
            author=author,
            origin=origin
        )
        
        documents.append(doc)
        document_id += 1
    
    return documents