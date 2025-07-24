## Information Retrieval System

A comprehensive information retrieval system implementing document collection, processing, search, and evaluation functionalities.

## Project Structure
```
/
├── document.py              # Document class with stemming support
├── main.py                  # Enhanced CLI with new search options
├── test_wrapper.py          # Test interface wrapper
├── stemming_algorithm.txt   # Porter stemming algorithm specification
├── ir_core/                 # Core IR functionality package
│   ├── __init__.py         # Package initialization
│   ├── collection.py       # Document downloading and parsing
│   ├── retrieval.py        # Boolean & Vector Space Model search
│   ├── stopwords.py        # Stopword removal functions
│   └── stemming.py         # Porter stemming implementation
├── public_tests/           # PR02 test cases
│   ├── englishST.txt       # English stopwords list
│   ├── test_pr02_t2.py     # Document collection tests
│   ├── test_pr02_t3.py     # Boolean search tests
│   └── test_pr02_t4.py     # Stopword removal tests
└── pr03_tests_v1.0/        # PR03 test cases
    ├── test_pr03_t1.py     # Stemming tests
    ├── test_pr03_t2.py     # Vector Space Model tests
    └── test_pr03_t3.py     # Evaluation tests
```

## Usage

### Running the Application
```bash
python main.py
```

### Menu Options
1. **Download & Parse Collection** - Load documents from URLs
2. **Search Documents (Boolean)** - Boolean search with multi-term support
3. **Search Documents (Vector Space Model)** - tf-idf based ranking search
4. **Remove Stopwords (List-based)** - Filter using external stopword files
5. **Remove Stopwords (Frequency-based)** - Automatic filtering by term frequency
6. **Apply Stemming** - Porter stemming for term normalization
7. **Load Ground Truth for Evaluation** - Load JSON ground truth for precision/recall
8. **View Collection Status** - Display collection statistics
9. **Exit**

### Search Options
For each search method, you can choose:
- **Original terms**: Search in raw document terms
- **Filtered terms**: Search after stopword removal
- **Stemmed terms**: Search using Porter stemmed terms
- **Filtered + Stemmed terms**: Combined preprocessing

### Testing
```bash
# Run all tests
python -m pytest public_tests/ pr03_tests_v1.0/ -v

# Run specific tests
python -m pytest public_tests/ -v          # PR02 tests
python -m pytest pr03_tests_v1.0/ -v       # PR03 tests
```
