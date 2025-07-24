## Information Retrieval System

## Project Structure
/
├── document.py              # Document class definition
├── main.py                  # Command-line interface application
├── test_wrapper.py          # Test interface wrapper
├── ir_core/                 # Core IR functionality package
│   ├── __init__.py         # Package initialization
│   ├── collection.py       # Document downloading and parsing
│   ├── retrieval.py        # Boolean search implementation
│   └── stopwords.py        # Stopword removal functions
└── public_tests/
    ├── englishST.txt       # English stopwords list
    ├── test_pr02_t2.py     # Document collection tests
    ├── test_pr02_t3.py     # Boolean search tests
    └── test_pr02_t4.py     # Stopword removal tests
