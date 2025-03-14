import asyncio
import os
from urllib.parse import urlparse
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode,
    MemoryAdaptiveDispatcher,
    CrawlerMonitor,
    DisplayMode
)

async def crawl_batch(sitemap):
    urls = []
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=False  # Default: get all results at once
    )

    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=10,
        monitor=CrawlerMonitor(
            display_mode=DisplayMode.DETAILED
        )
    )

    # Read the sitemap and extract URLs
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=sitemap, config=run_config)
        
        # Parse the sitemap XML to extract URLs
        url_elements = result.markdown.split('<url>')[1:]
        for url_element in url_elements:
            loc_start = url_element.find('<loc>') + len('<loc>')
            loc_end = url_element.find('</loc>')
            url = url_element[loc_start:loc_end]
            urls.append(url)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Get all results at once
        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        )

        # Process all results after completion
        for result in results:
            if result.success:
                await process_result(result)
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")

async def process_result(result):
    # Extract hostname from URL
    parsed_url = urlparse(result.url)
    hostname = parsed_url.netloc
    
    # Create outputs/hostname directory if it doesn't exist
    output_dir = os.path.join("outputs", hostname)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a filename from the URL path
    path_parts = parsed_url.path.strip('/').split('/')
    
    # Use the last part of the path as the base filename
    if path_parts and path_parts[-1]:
        filename = path_parts[-1]
    else:
        # If the path is empty or ends with /, use 'index'
        filename = 'index'
    
    # Ensure filename is valid and add .md extension
    filename = filename.replace('/', '-') + '.md'
    filepath = os.path.join(output_dir, filename)
    
    # Save the markdown content to the file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result.markdown)
        print(f"Saved {result.url} to {filepath}")
    except Exception as e:
        print(f"Error saving {result.url}: {str(e)}")

if __name__ == "__main__":
    sitemap = "https://docs.crawl4ai.com/sitemap.xml" # Replace with your sitemap URL
    asyncio.run(crawl_batch(sitemap))