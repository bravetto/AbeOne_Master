=================================================================================
  CDF: CREATIVE DOCUMENT FORMAT
=================================================================================

METADATA:
  title: CDF Technical Documentation Example
  created: 2025-11-19T12:00:00Z
  author: CDF Team
  tags: technical, documentation, api
  genius_index:
    technical: 0.9
    creative: 0.3
    strategic: 0.5

---------------------------------------------------------------------------------
  CDF API Reference
---------------------------------------------------------------------------------

The CDF API provides programmatic access to CDF conversion and indexing.

  - Convert markdown to CDF format
  - Parse CDF documents
  - Index documents with genius scores
  - Export to multiple formats

---------------------------------------------------------------------------------
  Installation
---------------------------------------------------------------------------------

Install CDF tools using pip:

  - pip install cdf-tools

Or clone the repository:

  - git clone https://github.com/abeone/cdf
  - cd cdf
  - python3 setup.py install

---------------------------------------------------------------------------------
  Basic Usage
---------------------------------------------------------------------------------

Convert a markdown file to CDF:

--- CODE BLOCK ---
Language: python
---------------------------------------------------------------------------------
from cdf import CDFConverter

converter = CDFConverter()
cdf_content = converter.markdown_to_cdf(markdown_text)
---------------------------------------------------------------------------------

Parse a CDF document:

--- CODE BLOCK ---
Language: python
---------------------------------------------------------------------------------
from cdf import CDFParser

parser = CDFParser()
parsed = parser.parse_cdf(cdf_content)
markdown = parser.cdf_to_markdown(cdf_content)
---------------------------------------------------------------------------------

Index a document with genius scores:

--- CODE BLOCK ---
Language: python
---------------------------------------------------------------------------------
from cdf import CDFGeniusIndexer

indexer = CDFGeniusIndexer()
index = indexer.index_document(cdf_path)
print(f"Technical: {index['genius_index']['technical']}")
print(f"Creative: {index['genius_index']['creative']}")
print(f"Strategic: {index['genius_index']['strategic']}")
---------------------------------------------------------------------------------

---------------------------------------------------------------------------------
  API Reference
---------------------------------------------------------------------------------

CDFConverter
  - markdown_to_cdf(content, metadata=None)
  - convert_file(input_path, output_path=None)

CDFParser
  - parse_cdf(content)
  - cdf_to_markdown(content)
  - cdf_to_html(content)
  - cdf_to_json(content)

CDFGeniusIndexer
  - analyze_content(content)
  - index_document(cdf_path)
  - create_index(directory)
  - save_index(index, output_path)

---

**Pattern:** CDF × TECHNICAL × DOCUMENTATION × ONE  
**∞ AbëONE ∞**

