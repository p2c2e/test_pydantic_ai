import asyncio
from dotenv import load_dotenv
import logging
import os
from typing import Optional
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from playwright.async_api import async_playwright, Page, BrowserContext, ElementHandle

# Load environment variables from .env file
load_dotenv()

# Configure logger
logger = logging.getLogger("WebSurferAgent")
if os.getenv("LOG_ENABLED", "").lower() in ("true", "1", "yes"):
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.CRITICAL)

# Environment variable to determine if screenshots should be saved
SAVE_SCREENSHOTS = os.getenv("SAVE_SCREENSHOTS", "false").lower() in ("true", "1", "yes")
print(SAVE_SCREENSHOTS)
exit(1)

class BrowserState(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    playwright: Optional[any] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None

class WebSurferAgent(Agent[BrowserState, str]):
    # DEFAULT_URL = "https://duckduckgo.com"
    DEFAULT_URL = "https://www.google.com"
    
    # SEARCH_URL_TEMPLATE = "https://www.duckduckgo.com/search?q={query}"
    SEARCH_URL_TEMPLATE = "https://duckduckgo.com/?t=h_&q={query}&ia=web"

    def __init__(self, model_name: str = 'openai:gpt-4o-mini', system_prompt: str = ""):
        # Initialize BrowserState
        browser_state = BrowserState()
        
        # Call the parent constructor
        super().__init__(
            model=model_name,
            deps_type=BrowserState,
            result_type=str,
            system_prompt=system_prompt or (
                "A helpful assistant with access to a web browser. Ask them to perform web searches, open pages, and interact "
                "with content (e.g., clicking links, scrolling the viewport, etc., filling in form fields, etc.) "
                "It can also summarize the entire page, or answer questions based on the content of the page. "
                "It can also be asked to sleep and wait for pages to load, in cases where the pages seem to be taking a while to load."
            ),
        )


async def get_or_create_page(ctx: RunContext[BrowserState]) -> Page:
    if ctx.deps.context is None:
        print("Creating new browser context...")
        ctx.deps.playwright = await async_playwright().start()
        browser = await ctx.deps.playwright.chromium.launch(headless=False)
        
        # Create context with permissions automatically denied
        ctx.deps.context = await browser.new_context(
            permissions=[],  # Explicitly deny all permissions
            geolocation=None,  # Explicitly deny geolocation
            ignore_https_errors=True,
            java_script_enabled=True,
            bypass_csp=True,
            viewport={'width': 1280, 'height': 1024}
        )
        
        # Set up automatic permission denial for all types of requests
        ctx.deps.context.on("permissionrequest", lambda request: request.deny())
        
        # Set geolocation to null to prevent any geolocation access
        await ctx.deps.context.set_geolocation(None)
    else:
        print("Using existing browser context")

    if ctx.deps.page is None:
        print("Creating new page...")
        ctx.deps.page = await ctx.deps.context.new_page()
        await ctx.deps.page.goto(web_surfer.DEFAULT_URL)
        print(f"Navigated new page to: {ctx.deps.page.url}")
    else:
        print(f"Using existing page with URL: {ctx.deps.page.url}")
        
    return ctx.deps.page

web_surfer = WebSurferAgent()

@web_surfer.tool
async def init(ctx: RunContext[BrowserState], headless: bool = True):
    """Initialize the browser instance.
    
    Args:
        ctx: The run context containing browser state
        headless: Whether to run the browser in headless mode (without UI)
        
    Returns:
        str: Success message if initialization was successful
        
    This function:
    - Starts the Playwright instance
    - Launches a Chromium browser
    - Creates a new browser context
    - Initializes a new page
    """
    print(f"init called with headless={headless}")
    print(f"Parameters: headless={headless}")
    ctx.deps.playwright = await async_playwright().start()
    browser = await ctx.deps.playwright.chromium.launch(headless=headless)
    
    # Create context with explicit permission denial
    ctx.deps.context = await browser.new_context(
        permissions=[],  # Deny all permissions
        geolocation=None,  # Explicitly deny geolocation
        ignore_https_errors=True,
        java_script_enabled=True,
        bypass_csp=True,
        viewport={'width': 1280, 'height': 1024}
    )
    
    # Set up automatic permission denial
    ctx.deps.context.on("permissionrequest", lambda request: request.deny())
    await ctx.deps.context.set_geolocation(None)
    ctx.deps.page = await get_or_create_page(ctx)
    return "Initialization successful"

@web_surfer.tool
async def visit_url(ctx: RunContext[BrowserState], url: str):
    """Navigate to a specified URL.
    
    Args:
        ctx: The run context containing browser state
        url: The URL to navigate to
        
    Returns:
        str: Success message with the visited URL or error message
        
    This function:
    - Creates or gets existing page
    - Navigates to the specified URL
    - Waits for page to fully load
    - Takes screenshot if enabled
    - Handles navigation errors
    """
    print(f"visit_url called with url={url}")
    print(f"Parameters: url={url}")
    if not url:
        ctx.deps.page = await get_or_create_page(ctx)
        if ctx.deps.page.url != web_surfer.DEFAULT_URL:
            await ctx.deps.page.goto(web_surfer.DEFAULT_URL)
        return f"Successfully ensured default page is loaded: {web_surfer.DEFAULT_URL}"

    try:
        ctx.deps.page = await get_or_create_page(ctx)
        print("Created page ...")
        await ctx.deps.page.goto(url)
        print("Goto url done ....")
        await ctx.deps.page.wait_for_load_state()
        print("Completed waiting .....")
        logger.info(f"Visited URL: {url}")
        if SAVE_SCREENSHOTS:
            await save_screenshot(ctx, "click")
        print("Returning success.....")
        return f"Successfully visited url {url}"
    except Exception as e:
        logger.error(f"Failed to visit URL {url}: {str(e)}")
        return f"Failed to visit URL {url}: {str(e)}"

@web_surfer.tool
async def history_back(ctx: RunContext[BrowserState]):
    """Navigate back in browser history.
    
    Args:
        ctx: The run context containing browser state
        
    Returns:
        str: Success message or error message
        
    This function:
    - Navigates back to previous page in history
    - Waits for page to fully load
    - Takes screenshot if enabled
    """
    print("history_back called")
    print("Parameters: none")
    ctx.deps.page = await get_or_create_page(ctx)
    await ctx.deps.page.go_back()
    await ctx.deps.page.wait_for_load_state()
    logger.info("Navigated back in history")
    if SAVE_SCREENSHOTS:
        await save_screenshot(ctx, "history_back")
    return "Successfully navigated back in history"

@web_surfer.tool
async def web_search(ctx: RunContext[BrowserState], query: str):
    """Perform a web search using default search url.
    
    Args:
        ctx: The run context containing browser state
        query: The search query string
        
    Returns:
        str: Success message with search query or error message
        
    This function:
    - Creates new page if none exists
    - Navigates to web search results for the query
    - Uses visit_url internally for navigation
    """
    print(f"web_search called with query={query}")
    print(f"Parameters: query={query}")
    ctx.deps.page = await get_or_create_page(ctx)
    # if ctx.deps.page is None:
    #     ctx.deps.page = await ctx.deps.context.new_page()
    #     await ctx.deps.page.goto(web_surfer.DEFAULT_URL)
    search_url = WebSurferAgent.SEARCH_URL_TEMPLATE.format(query=query)
    await visit_url(ctx, search_url)
    return f"Successfully performed web search for query '{query}'"

@web_surfer.tool
async def page_up(ctx: RunContext[BrowserState]):
    """Scroll the page up by one viewport height.
    
    Args:
        ctx: The run context containing browser state
        
    Returns:
        str: Success message or error message
        
    This function:
    - Checks if already at top of page
    - Scrolls up by one viewport height if possible
    - Takes screenshot if enabled
    """
    print("page_up called")
    print("Parameters: none")
    ctx.deps.page = await get_or_create_page(ctx)
    
    # Get current scroll position
    scroll_y = await ctx.deps.page.evaluate("window.scrollY")
    
    if scroll_y <= 0:
        return "Already at the top of the page"
        
    await ctx.deps.page.evaluate("window.scrollBy(0, -window.innerHeight);")
    logger.info("Scrolled up")
    if SAVE_SCREENSHOTS:
        await save_screenshot(ctx, "page_up")
    return "Successfully scrolled up"

@web_surfer.tool
async def page_down(ctx: RunContext[BrowserState]):
    """Scroll the page down by one viewport height.
    
    Args:
        ctx: The run context containing browser state
        
    Returns:
        str: Success message or error message
        
    This function:
    - Checks if already at bottom of page
    - Scrolls down by one viewport height if possible
    - Takes screenshot if enabled
    """
    print("page_down called")
    print("Parameters: none")
    ctx.deps.page = await get_or_create_page(ctx)
    
    # Get page height and scroll position
    page_height = await ctx.deps.page.evaluate("document.body.scrollHeight")
    viewport_height = await ctx.deps.page.evaluate("window.innerHeight")
    scroll_y = await ctx.deps.page.evaluate("window.scrollY")
    
    # Check if we're already at the bottom
    if scroll_y + viewport_height >= page_height:
        return "Already at the bottom of the page"
        
    await ctx.deps.page.evaluate("window.scrollBy(0, window.innerHeight);")
    logger.info("Scrolled down")
    if SAVE_SCREENSHOTS:
        await save_screenshot(ctx, "page_down")
    return "Successfully scrolled down"

@web_surfer.tool
async def input_text(ctx: RunContext[BrowserState], selector: str, text: str):
    """Input text into a web page element.
    
    Args:
        ctx: The run context containing browser state
        selector: CSS selector for the target element
        text: Text to input into the element
        
    Returns:
        str: Success message with input text or error message
        
    This function:
    - Verifies element exists using selector
    - Fills the element with specified text
    - Handles timeout and element not found errors
    - Takes screenshot if enabled
    """
    print(f"input_text called {selector} {text}")
    print(f"Parameters: selector={selector}, text={text}")
    try:
        ctx.deps.page = await get_or_create_page(ctx)
        print("After the get_or_create_page call ......")
        # First check if the selector exists
        element = await ctx.deps.page.query_selector(selector)
        if not element:
            message = f"No element found with selector '{selector}'. Please verify the selector or try a different one."
            logger.error(message)
            return message
        else:
            print(f"Element found with selector '{selector}' - {element}")
            
        await ctx.deps.page.fill(selector, text, timeout=5000)
        logger.info(f"Input text '{text}' into element with selector '{selector}'")
        if SAVE_SCREENSHOTS:
            await save_screenshot(ctx, "input_text")
        available_elements = await inspect_page_elements(ctx.deps.page)
        return f"Successfully input text: {text} and available fields are :\n {available_elements}"
    except Exception as e:
        message = f"Failed to input text: {str(e)}. If it is timing out, you could try alternative fields like text, input, textarea etc."
        logger.error(message)
        print(message)
        return message

@web_surfer.tool
async def click(ctx: RunContext[BrowserState], selector: str):
    """Click an element on the web page.
    
    Args:
        ctx: The run context containing browser state
        selector: CSS selector for the element to click
        
    Returns:
        str: Success message or error message with available elements if click fails
        
    This function:
    - Checks if element exists using selector
    - Attempts to click element with timeout
    - Returns list of available elements if click fails
    - Takes screenshot if enabled
    """
    print(f"click called with selector={selector}")
    print(f"Parameters: selector={selector}")
    try:
        ctx.deps.page = await get_or_create_page(ctx)
        
        # First check if the selector exists
        element = await ctx.deps.page.query_selector(selector)
        if not element:
            elements = await inspect_page_elements(ctx.deps.page)
            return f"No element found with selector '{selector}'. Available elements:\n{elements}"
            
        # Try to click with timeout
        await ctx.deps.page.click(selector, timeout=5000)
        logger.info(f"Clicked element with selector '{selector}'")
        if SAVE_SCREENSHOTS:
            await save_screenshot(ctx, "click")
        return f"Successfully clicked element with selector '{selector}'"
        
    except Exception as e:
        elements = await inspect_page_elements(ctx.deps.page)
        logger.error(f"Failed to click element: {str(e)}")
        return f"Failed to click element: {str(e)}. Available elements:\n{elements}"

# @web_surfer.tool
async def save_screenshot(ctx: RunContext[BrowserState], action: str):
    """Save a screenshot of the current page.
    
    Args:
        ctx: The run context containing browser state
        action: Identifier for the screenshot (used in filename)
        
    Returns:
        str: Path to saved screenshot or error message
        
    This function:
    - Creates screenshots directory if needed
    - Captures full page screenshot
    - Saves to file with action-based name
    - Returns path to saved screenshot
    """
    print(f"save_screenshot called with action={action}")
    print(f"Parameters: action={action}")
    ctx.deps.page = await get_or_create_page(ctx)
    # Define the directory to save screenshots
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # Construct the screenshot file path
    screenshot_path = os.path.join(screenshots_dir, f"screenshot_{action}.png")

    # Capture the screenshot
    await ctx.deps.page.screenshot(path=screenshot_path, full_page=True)

    # Log the screenshot path
    logger.info(f"Saved screenshot: {screenshot_path}")

    return f"Successfully saved screenshot: {screenshot_path}"

async def inspect_page_elements(page: Page) -> str:
    """Inspect the page and return information about input fields and buttons"""
    elements_info = []
    
    # Get all input elements
    inputs = await page.query_selector_all("input, textarea, select, button")
    for element in inputs:
        try:
            tag = await element.evaluate("el => el.tagName.toLowerCase()")
            element_type = await element.get_attribute("type") or "text"
            name = await element.get_attribute("name") or ""
            id_attr = await element.get_attribute("id") or ""
            placeholder = await element.get_attribute("placeholder") or ""
            
            elements_info.append(
                f"{tag} [type={element_type}] "
                f"name={name} id={id_attr} "
                f"placeholder={placeholder}"
            )
        except Exception as e:
            logger.error(f"Error inspecting element: {str(e)}")
            continue
            
    if not elements_info:
        return "No input fields or buttons found on the page"
        
    return "Page elements found:\n" + "\n".join(elements_info)

@web_surfer.tool
async def inspect_page(ctx: RunContext[BrowserState]) -> str:
    """Inspect and list all interactive elements on the page.
    
    Args:
        ctx: The run context containing browser state
        
    Returns:
        str: Formatted list of elements or error message
        
    This function:
    - Finds all input, textarea, select and button elements
    - Returns their tag names, types, IDs, names and placeholders
    - Handles inspection errors
    """
    """Inspect the current page and return information about form elements"""
    try:
        ctx.deps.page = await get_or_create_page(ctx)
        return await inspect_page_elements(ctx.deps.page)
    except Exception as e:
        logger.error(f"Failed to inspect page: {str(e)}")
        return f"Failed to inspect page: {str(e)}"

@web_surfer.tool
async def close(ctx: RunContext[BrowserState]):
    """Close the browser and cleanup resources.
    
    Args:
        ctx: The run context containing browser state
        
    Returns:
        str: Success message or error message
        
    This function:
    - Closes the browser context
    - Stops the Playwright instance
    - Cleans up all browser resources
    """
    print("close called")
    print("Parameters: none")
    if ctx.deps.context:
        await ctx.deps.context.close()
    if ctx.deps.playwright:
        await ctx.deps.playwright.stop()
    return "Successfully closed browser context and stopped Playwright"

# Example usage
async def main():
    # agent = WebSurferAgent()
    deps = BrowserState()
    result = await web_surfer.run("Visit the default page search for 'PydanticAI', scroll down, and click the first link", deps=deps)
    # await agent.init()
    # await agent.visit_url("https://www.example.com")
    # await agent.web_search("PydanticAI")
    # await agent.page_down()
    # await agent.page_up()
    # await agent.input_text("input[name='q']", "PydanticAI")
    # await agent.click("input[type='submit']")
    # await agent.history_back()
    # await agent.close()
    # print(result)

    # for msg in result.all_messages():
    #     print(msg)
    #     print("-"*50)
    # print("%"*50)
    # print(deps)
    print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
