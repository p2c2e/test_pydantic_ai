import os
import re
import asyncio
import logging
from urllib.parse import urljoin, urldefrag
import html2text
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def download_markdown(base_url: str, url_pattern: str):
    """
    Download markdown content from URLs matching a given pattern in the base URL content.
    
    Args:
        base_url: The starting URL to scrape
        url_pattern: Regular expression pattern to match URLs for processing
    """
    logger.info(f"Starting download from base URL: {base_url}")
    logger.info(f"Using URL pattern: {url_pattern}")
    
    # Create output directory if it doesn't exist
    output_dir = 'markdown_docs'
    os.makedirs(output_dir, exist_ok=True)
    logger.debug(f"Created/verified output directory: {output_dir}")
    
    async with async_playwright() as p:
        # Launch browser
        logger.debug("Launching browser...")
        browser = await p.chromium.launch()
        
        context = await browser.new_context()
        async with context:
            page = await context.new_page()
            
            # Navigate to base URL and wait for content to load
            logger.debug(f"Navigating to {base_url}")
            await page.goto(base_url, wait_until="networkidle")
            content = await page.content()
            logger.debug("Retrieved base page content")
            
            # Parse the content
            soup = BeautifulSoup(content, 'html.parser')
        
            # Find all links in the content
            links = soup.find_all('a', href=True)
            logger.debug(f"Found {len(links)} total links on the page")
            
            # Keep track of processed URLs
            processed_urls = set()
            api_links = []
            
            # Extract links matching the provided pattern
            url_regex = re.compile(url_pattern)
            for link in links:
                href = link['href']
                # Convert relative URLs to absolute first
                absolute_url = urljoin(base_url, href)
                # Remove URL fragments
                url_without_fragment, _ = urldefrag(absolute_url)
                logger.debug(f"Converting {href} to {url_without_fragment}")
                
                # Skip if we've already processed this URL
                if url_without_fragment in processed_urls:
                    logger.debug(f"Skipping already processed URL: {url_without_fragment}")
                    continue
                
                # Then check if it matches our pattern
                if url_regex.match(url_without_fragment):
                    api_links.append(url_without_fragment)
                    processed_urls.add(url_without_fragment)
            logger.info(f"Found {len(api_links)} unique API documentation links to process")
            
            # Download content for each API link
            for i, url in enumerate(api_links, 1):
                logger.info(f"Processing link {i}/{len(api_links)}: {url}")
                try:
                    # Navigate to URL and wait for content to load
                    logger.debug(f"Navigating to {url}")
                    await page.goto(url, wait_until="networkidle")
                    content = await page.content()
                    logger.debug(f"Retrieved content from {url}")
                    
                    # Create filename from URL
                    filename = url.rstrip('/').split('/')[-1]
                    if '/' in filename:
                        filename = filename.replace('/', '_')
                    filename = f"{filename}.md"
                    filepath = os.path.join('markdown_docs', filename)
                    
                    # Convert HTML to Markdown
                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    h.ignore_images = False
                    h.ignore_tables = False
                    markdown_content = h.handle(content)
                    
                    # Save content as markdown file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    logger.info(f"Successfully downloaded and saved: {filename}")
                    logger.debug(f"Content length: {len(content)} characters")
                    
                except Exception as e:
                    logger.error(f"Error downloading {url}: {str(e)}", exc_info=True)
                
                # Add a small delay between requests
                await asyncio.sleep(1)
            
            logger.info("Download process completed")

if __name__ == "__main__":
    base_url = "https://ai.pydantic.dev/api/agent/"
    # Pattern to match API documentation URLs (both relative and absolute)
    url_pattern = r'https://ai.pydantic.dev/api/.*'
    asyncio.run(download_markdown(base_url, url_pattern))
