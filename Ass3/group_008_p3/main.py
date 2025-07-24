# Main entry point for the Information Retrieval System
# Provides a command-line interface for document collection management and search

import os
import re
import json
from ir_core.collection import load_documents_from_url
from ir_core.retrieval import linear_boolean_search, vector_space_search, precision_recall
from ir_core.stopwords import remove_stopwords_by_list, remove_stopwords_by_frequency
from ir_core.stemming import apply_stemming, apply_stemming_filtered

class IRSystemCLI:
    def __init__(self):
        self.collection = []  # List of Document objects
        self.current_stopword_file = None
        self.ground_truth = {}  # For evaluation
    
    def clear_screen(self):
        """Clear the terminal screen for better user experience"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Display the system header with current status"""
        print("=" * 60)
        print("INFORMATION RETRIEVAL SYSTEM")
        print("=" * 60)
        print(f"Collection Status: {len(self.collection)} documents loaded")
        if self.current_stopword_file:
            print(f"Stopword File: {os.path.basename(self.current_stopword_file)}")
        print("-" * 60)
    
    def print_menu(self):
        """Display the main menu options"""
        print("\nMAIN MENU:")
        print("  1) Download & Parse Collection")
        print("  2) Search Documents (Boolean)")
        print("  3) Search Documents (Vector Space Model)")
        print("  4) Remove Stopwords (List-based)")
        print("  5) Remove Stopwords (Frequency-based)")
        print("  6) Apply Stemming")
        print("  7) Load Ground Truth for Evaluation")
        print("  8) View Collection Status")
        print("  9) Exit")
        print("-" * 60)
    
    def get_user_choice(self):
        """Get and validate user menu choice"""
        try:
            choice = input("Enter your choice (1-9): ").strip()
            return choice
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return '9'
    
    def get_filtered_terms_count(self, doc):
        """Helper method to get filtered terms count safely"""
        if callable(doc.filtered_terms):
            return len(doc.filtered_terms())
        else:
            return len(doc.filtered_terms)
    
    def handle_download_parse(self):
        """Handle document collection downloading and parsing"""
        print("\nDOWNLOAD & PARSE COLLECTION")
        print("-" * 40)
        
        try:
            # Get URL
            url = input("Enter URL: ").strip()
            if not url:
                print("Error: URL cannot be empty")
                return
            
            # Get author and origin
            author = input("Enter author name: ").strip()
            origin = input("Enter collection name: ").strip()
            
            # Get line range
            start_line = int(input("Enter start line (0-based): ").strip())
            end_input = input("Enter end line (press Enter for end of file): ").strip()
            end_line = int(end_input) if end_input else None
            
            # Get regex pattern
            print("\nEnter regex pattern for document extraction:")
            print("   (Group 1: title, Group 2: content)")
            pattern_str = input("Regex pattern: ").strip()
            
            if not pattern_str:
                print("Error: Pattern cannot be empty")
                return
            
            # Compile regex pattern
            search_pattern = re.compile(pattern_str, re.DOTALL)
            
            # Download and parse
            print("\nDownloading and parsing...")
            documents = load_documents_from_url(url, author, origin, start_line, end_line, search_pattern)
            
            if documents:
                self.collection = documents
                print(f"Successfully loaded {len(documents)} documents!")
                
                # Show first few documents
                print("\nFirst 3 documents:")
                for i, doc in enumerate(documents[:3]):
                    print(f"   {i}: {doc.title[:50]}{'...' if len(doc.title) > 50 else ''}")
            else:
                print("Error: No documents found or error occurred")
                
        except ValueError as e:
            print(f"Error: Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_search(self):
        """Handle Boolean document search"""
        if not self.collection:
            print("Error: No documents loaded. Please load a collection first.")
            return
        
        print("\nSEARCH DOCUMENTS (Boolean Model)")
        print("-" * 40)
        
        try:
            # Get search query
            query = input("Enter search query (space-separated terms): ").strip()
            if not query:
                print("Error: Search query cannot be empty")
                return
            
            # Get search options
            print("\nSearch options:")
            print("  1. Original terms")
            print("  2. Filtered terms (after stopword removal)")
            print("  3. Stemmed terms")
            print("  4. Filtered + Stemmed terms")
            choice = input("Choose search type (1-4): ").strip()
            
            stopword_filtered = choice in ['2', '4']
            stemmed = choice in ['3', '4']
            
            # Perform search
            print(f"\nSearching for '{query}'...")
            results = linear_boolean_search(query, self.collection, stopword_filtered, stemmed)
            
            # Filter and display results (only show matches)
            matches = [(score, doc) for score, doc in results if score == 1]
            
            if matches:
                print(f"Found {len(matches)} matching document(s):")
                print("-" * 40)
                for score, doc in matches:
                    print(f"ID: {doc.document_id:3d} | {doc.title}")
                    print(f"   Author: {doc.author} | Origin: {doc.origin}")
                    preview = doc.raw_text[:100] + "..." if len(doc.raw_text) > 100 else doc.raw_text
                    print(f"   Preview: {preview}")
                    print()
                
                # Calculate precision and recall if ground truth is available
                self.calculate_evaluation(query, matches)
            else:
                print(f"No documents found containing all terms in '{query}'")
                
        except Exception as e:
            print(f"Error during search: {e}")
    
    def handle_vsm_search(self):
        """Handle Vector Space Model search"""
        if not self.collection:
            print("Error: No documents loaded. Please load a collection first.")
            return
        
        print("\nSEARCH DOCUMENTS (Vector Space Model)")
        print("-" * 40)
        
        try:
            # Get search query
            query = input("Enter search query (space-separated terms): ").strip()
            if not query:
                print("Error: Search query cannot be empty")
                return
            
            # Get search options
            print("\nSearch options:")
            print("  1. Original terms")
            print("  2. Filtered terms (after stopword removal)")
            print("  3. Stemmed terms")
            print("  4. Filtered + Stemmed terms")
            choice = input("Choose search type (1-4): ").strip()
            
            stopword_filtered = choice in ['2', '4']
            stemmed = choice in ['3', '4']
            
            # Perform search
            print(f"\nSearching for '{query}'...")
            results = vector_space_search(query, self.collection, stopword_filtered, stemmed)
            
            # Sort by relevance score (descending)
            results.sort(key=lambda x: x[0], reverse=True)
            
            # Display top results with non-zero scores
            relevant_results = [(score, doc) for score, doc in results if score > 0]
            
            if relevant_results:
                print(f"Found {len(relevant_results)} relevant document(s):")
                print("-" * 40)
                for score, doc in relevant_results[:10]:  # Show top 10
                    print(f"Score: {score:.4f} | ID: {doc.document_id:3d} | {doc.title}")
                    print(f"   Author: {doc.author} | Origin: {doc.origin}")
                    preview = doc.raw_text[:100] + "..." if len(doc.raw_text) > 100 else doc.raw_text
                    print(f"   Preview: {preview}")
                    print()
                
                # Calculate precision and recall if ground truth is available
                self.calculate_evaluation(query, relevant_results)
            else:
                print(f"No relevant documents found for '{query}'")
                
        except Exception as e:
            print(f"Error during search: {e}")
    
    def calculate_evaluation(self, query, results):
        """Calculate and display precision and recall"""
        if not self.ground_truth:
            return
        
        try:
            # Extract query terms for ground truth lookup
            query_terms = query.lower().strip().split()
            
            # Get retrieved document IDs
            retrieved_ids = {doc.document_id for score, doc in results}
            
            # Calculate precision and recall for each query term
            for term in query_terms:
                if term in self.ground_truth:
                    # Convert ground truth document names to IDs if possible
                    relevant_names = set(self.ground_truth[term])
                    relevant_ids = set()
                    
                    # Try to match document titles to ground truth names
                    for doc in self.collection:
                        doc_name = doc.title.lower().replace(' ', '_').replace('-', '_')
                        # Remove special characters and normalize
                        doc_name = re.sub(r'[^\w\s]', '', doc_name).replace(' ', '_')
                        
                        if any(doc_name in gt_name.lower() or gt_name.lower() in doc_name 
                               for gt_name in relevant_names):
                            relevant_ids.add(doc.document_id)
                    
                    if relevant_ids:
                        precision, recall = precision_recall(retrieved_ids, relevant_ids)
                        print(f"Evaluation for term '{term}':")
                        print(f"   Precision: {precision:.3f}")
                        print(f"   Recall: {recall:.3f}")
                        print()
        except Exception as e:
            print(f"Error calculating evaluation: {e}")
    
    def handle_stopwords_list(self):
        """Handle list-based stopword removal"""
        if not self.collection:
            print("Error: No documents loaded. Please load a collection first.")
            return
        
        print("\nREMOVE STOPWORDS (List-based)")
        print("-" * 40)
        
        try:
            # Get stopword file path
            file_path = input("Enter stopword file path: ").strip()
            if not file_path:
                print("Error: File path cannot be empty")
                return
            
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return
            
            # Load stopwords
            print("Loading stopwords...")
            stopwords = set()
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        stopwords.add(word)
            
            print(f"Loaded {len(stopwords)} stopwords")
            
            # Apply to all documents
            print("Applying stopword removal to all documents...")
            for doc in self.collection:
                remove_stopwords_by_list(doc, stopwords)
            
            self.current_stopword_file = file_path
            print("Stopword removal completed for all documents!")
            
            # Show statistics
            total_original = sum(len(doc.terms) for doc in self.collection)
            total_filtered = sum(self.get_filtered_terms_count(doc) for doc in self.collection)
            removed = total_original - total_filtered
            print(f"Statistics: {removed} terms removed ({total_filtered} remaining)")
            
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_stopwords_frequency(self):
        """Handle frequency-based stopword removal"""
        if not self.collection:
            print("Error: No documents loaded. Please load a collection first.")
            return
        
        print("\nREMOVE STOPWORDS (Frequency-based)")
        print("-" * 40)
        
        try:
            # Get frequency thresholds
            print("Enter frequency thresholds (0.0 to 1.0):")
            common_freq = float(input("Common frequency threshold (e.g., 0.1): ").strip())
            rare_freq = float(input("Rare frequency threshold (e.g., 0.001): ").strip())
            
            if not (0.0 <= common_freq <= 1.0) or not (0.0 <= rare_freq <= 1.0):
                print("Error: Frequencies must be between 0.0 and 1.0")
                return
            
            if rare_freq >= common_freq:
                print("Error: Rare frequency should be less than common frequency")
                return
            
            # Apply to all documents
            print("Applying frequency-based stopword removal...")
            for doc in self.collection:
                remove_stopwords_by_frequency(doc, self.collection, rare_freq, common_freq)
            
            print("Frequency-based stopword removal completed!")
            
            # Show statistics
            total_original = sum(len(doc.terms) for doc in self.collection)
            total_filtered = sum(self.get_filtered_terms_count(doc) for doc in self.collection)
            removed = total_original - total_filtered
            print(f"Statistics: {removed} terms removed ({total_filtered} remaining)")
            
        except ValueError:
            print("Error: Invalid frequency values. Please enter numbers between 0.0 and 1.0")
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_stemming(self):
        """Handle stemming application to documents"""
        if not self.collection:
            print("Error: No documents loaded. Please load a collection first.")
            return
        
        print("\nAPPLY STEMMING")
        print("-" * 40)
        
        try:
            print("Choose stemming option:")
            print("  1. Apply stemming to original terms")
            print("  2. Apply stemming to filtered terms (requires stopword removal first)")
            choice = input("Choose option (1 or 2): ").strip()
            
            if choice == '1':
                print("Applying stemming to original terms...")
                for doc in self.collection:
                    apply_stemming(doc)
                print("Stemming applied to all documents!")
                
                # Show statistics
                total_original = sum(len(doc.terms) for doc in self.collection)
                total_stemmed = sum(len(doc.stemmed_terms()) for doc in self.collection)
                print(f"Statistics: {total_original} original terms -> {total_stemmed} stemmed terms")
                
            elif choice == '2':
                # Check if filtered terms are available
                if not any(self.get_filtered_terms_count(doc) > 0 for doc in self.collection):
                    print("Error: No filtered terms available. Please apply stopword removal first.")
                    return
                
                print("Applying stemming to filtered terms...")
                for doc in self.collection:
                    apply_stemming_filtered(doc)
                print("Stemming applied to filtered terms for all documents!")
                
                # Show statistics
                total_filtered = sum(self.get_filtered_terms_count(doc) for doc in self.collection)
                total_stemmed = sum(len(doc.filtered_stemmed_terms()) for doc in self.collection)
                print(f"Statistics: {total_filtered} filtered terms -> {total_stemmed} stemmed terms")
            else:
                print("Error: Invalid choice. Please enter 1 or 2.")
                
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_ground_truth(self):
        """Handle ground truth loading for evaluation"""
        print("\nLOAD GROUND TRUTH")
        print("-" * 40)
        
        try:
            file_path = input("Enter ground truth JSON file path: ").strip()
            if not file_path:
                print("Error: File path cannot be empty")
                return
            
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return
            
            print("Loading ground truth...")
            with open(file_path, 'r', encoding='utf-8') as f:
                self.ground_truth = json.load(f)
            
            print(f"Ground truth loaded successfully!")
            print(f"Available query terms: {len(self.ground_truth)}")
            print(f"Sample terms: {list(self.ground_truth.keys())[:10]}")
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def show_collection_status(self):
        """Display detailed collection status"""
        print("\nCOLLECTION STATUS")
        print("-" * 40)
        
        if not self.collection:
            print("No documents loaded")
            return
        
        print(f"Total Documents: {len(self.collection)}")
        
        if self.collection:
            # Show authors and origins
            authors = set(doc.author for doc in self.collection)
            origins = set(doc.origin for doc in self.collection)
            
            print(f"Authors: {', '.join(authors)}")
            print(f"Origins: {', '.join(origins)}")
            
            # Show term statistics
            total_terms = sum(len(doc.terms) for doc in self.collection)
            avg_terms = total_terms / len(self.collection)
            print(f"Total Terms: {total_terms}")
            print(f"Average Terms per Document: {avg_terms:.1f}")
            
            # Show filtered terms if available
            if any(self.get_filtered_terms_count(doc) > 0 for doc in self.collection):
                total_filtered = sum(self.get_filtered_terms_count(doc) for doc in self.collection)
                avg_filtered = total_filtered / len(self.collection)
                print(f"Total Filtered Terms: {total_filtered}")
                print(f"Average Filtered Terms per Document: {avg_filtered:.1f}")
            
            # Show sample documents
            print(f"\nSample Documents:")
            for i, doc in enumerate(self.collection[:5]):
                print(f"   {doc.document_id:3d}: {doc.title[:50]}{'...' if len(doc.title) > 50 else ''}")
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_user_choice()
            
            if choice == '1':
                self.handle_download_parse()
            elif choice == '2':
                self.handle_search()
            elif choice == '3':
                self.handle_vsm_search()
            elif choice == '4':
                self.handle_stopwords_list()
            elif choice == '5':
                self.handle_stopwords_frequency()
            elif choice == '6':
                self.handle_stemming()
            elif choice == '7':
                self.handle_ground_truth()
            elif choice == '8':
                self.show_collection_status()
            elif choice == '9':
                print("\nThank you for using the IR System!")
                break
            else:
                print("Error: Invalid choice. Please enter 1-9.")
            
            if choice != '9':
                input("\nPress Enter to continue...")


def main():
    """Entry point for the application"""
    try:
        ir_system = IRSystemCLI()
        ir_system.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()