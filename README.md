# site-to-md

A tool to crawl websites from sitemaps and convert pages to Markdown files.

## Description

site-to-md is a Python tool that uses the crawl4ai library to:

1. Parse a website's sitemap.xml file
2. Extract all URLs from the sitemap
3. Visit each URL and convert the content to Markdown
4. Save each page as a separate Markdown file in domain-specific folders under the "outputs" directory

## Use Cases

### Retrieval-Augmented Generation (RAG)

One of the primary use cases for site-to-md is to prepare content for Retrieval-Augmented Generation (RAG) systems. RAG is a technique that enhances Large Language Models (LLMs) by:

1. **Retrieving** relevant information from a knowledge base of documents
2. **Augmenting** the model's prompt with this retrieved information
3. **Generating** responses that incorporate both the model's parametric knowledge and the retrieved context

By converting website content to Markdown files:

- Content becomes easily parsable for vector embedding creation
- Documentation is transformed into a format ideal for chunk-based retrieval
- Knowledge bases can be kept up-to-date with the latest website information
- Domain-specific knowledge can be integrated into AI assistants and chatbots

## Installation

### Prerequisites

- Python 3.7+
- crawl4ai library

### Setup

```bash
# Clone the repository
git clone https://github.com/clydesantiago/site-to-md.git
cd site-to-md

# Install dependencies
pip install crawl4ai
```

## Usage

1. Open `main.py` and replace the sitemap URL with the one you want to crawl:

```python
sitemap = "https://your-website.com/sitemap.xml"  # Replace with your sitemap URL
```

2. Run the script:

```bash
python main.py
```

3. Markdown files will be generated in the `outputs` directory, organized by domain name.
   For example:
   - `outputs/example.com/page1.md`
   - `outputs/example.com/page2.md`
   - `outputs/blog.example.com/post1.md`

## Features

- Asynchronous web crawling for improved performance
- Memory-adaptive dispatching to prevent system overload
- Automatic file naming based on URL structure
- Domain-based file organization
- Detailed progress monitoring

## Configuration Options

The script includes several configuration options:

- `BrowserConfig`: Configure headless mode and verbosity
- `CrawlerRunConfig`: Set caching strategy and streaming mode
- `MemoryAdaptiveDispatcher`: Control memory usage and concurrent sessions

## License

MIT License
