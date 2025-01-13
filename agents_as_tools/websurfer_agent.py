import asyncio
import logging
import os
from typing import Optional
import html2text

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Page, BrowserContext
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from agent_utils import get_model

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
        self.name = "WebSurferAgent"
        # Call the parent constructor
        active_model = get_model()

        super().__init__(
            model=active_model,
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
        # print("Using existing browser context")
        pass

    if ctx.deps.page is None:
        print("Creating new page...")
        ctx.deps.page = await ctx.deps.context.new_page()
        await ctx.deps.page.goto(WebSurferAgent.DEFAULT_URL)
        print(f"Navigated new page to: {ctx.deps.page.url}")
    else:
        # print(f"Using existing page with URL: {ctx.deps.page.url}")
        pass
        
    return ctx.deps.page

def create_websurfer_agent() -> WebSurferAgent:
    web_surfer = WebSurferAgent()

    print("Here............")
    @web_surfer.tool
    async def summarize(ctx: RunContext[BrowserState]) -> str:
        """Extract the markdown version of the currently active page.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: Markdown version of the page content
            
        This function:
        - Retrieves the HTML content of the current page
        - Converts it to markdown format
        """
        print("**** summarize called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            html_content = await ctx.deps.page.content()
            # Convert HTML to markdown using html2text
            markdown_content = html2text.html2text(html_content)
            return markdown_content
        except Exception as e:
            logger.error(f"Failed to summarize page: {str(e)}")
            return f"Failed to summarize page: {str(e)}"
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

    # print("Here.2...........")
    # async def inspect_page_elements(page: Page) -> str:
    #     """Inspect the current page and return information about form elements."""
    #     print("**** inspect_page_elements called ...........")
    #     locator = page.locator("a, input, textarea, select, button")
    #     elements = await locator.all()
    #     element_info = []
    #     element_counts = {}
    #     for element in elements:
    #         try:
    #             tag_name = await element.evaluate("el => el.tagName")
    #             element_type = await element.evaluate("el => el.type || ''")
    #             element_id = await element.evaluate("el => el.id || ''")
    #             element_name = await element.evaluate("el => el.name || ''")
    #             element_placeholder = await element.evaluate("el => el.placeholder || ''")
    #
    #             try:
    #                 # Compute the XPath
    #                 xpath = await page.evaluate(
    #                     """el => {
    #                         let xpath = '';
    #                         let currentElement = el;
    #                         while (currentElement) {
    #                             if (currentElement.parentNode) {
    #                                 const index = Array.from(currentElement.parentNode.children).indexOf(currentElement) + 1;
    #                                 xpath = '/' + currentElement.tagName + '[' + index + ']' + xpath;
    #                                 currentElement = currentElement.parentNode;
    #                             } else {
    #                                 break;
    #                             }
    #                         }
    #                         return xpath;
    #                     }""",
    #                     element
    #                 )
    #             except Exception as e:
    #                 print(f"Error computing XPath for element: {e}")
    #                 xpath = "Error computing XPath"
    #
    #             # Construct element information string
    #             element_details = [f"Tag: {tag_name}", f"Type: {element_type}"]
    #             if element_id:
    #                 element_details.append(f"ID: {element_id}")
    #             if element_name:
    #                 element_details.append(f"Name: {element_name}")
    #             if element_placeholder:
    #                 element_details.append(f"Placeholder: {element_placeholder}")
    #             element_details.append(f"Selector: {xpath}")
    #
    #             element_info.append(", ".join(element_details))
    #
    #             # Update element counts
    #             element_counts[tag_name] = element_counts.get(tag_name, 0) + 1
    #         except Exception as e:
    #             print(f"Error evaluating element: {e}")
    #     # Print debug information with counts of each type of element
    #     print("Element counts:", element_counts)
    #
    #     rv = "\n".join(element_info)
    #     # print(rv)
    #     return rv

    @web_surfer.tool
    async def get_current_url(ctx: RunContext[BrowserState]) -> str:
        """Get the current page URL or page open in the browser.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: The current page URL or an error message
            
        This function:
        - Retrieves the URL of the current page
        """
        print("**** get_current_url called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            current_url = ctx.deps.page.url
            logger.info(f"Current page URL: {current_url}")
            return f"Current url is {current_url}"
        except Exception as e:
            logger.error(f"Failed to get current page URL: {str(e)}")
            return f"Failed to get current page URL: {str(e)}"


    @web_surfer.tool
    async def visit_url(ctx: RunContext[BrowserState], url: str):
        """Navigate to a specified URL.
        
        Args:
            ctx: The run context containing browser state
            url: The URL to navigate to
            
        Returns:
            str: Success message with the visited URL or error message
            
        This function:
        - Checks if already on the requested URL
        - Creates or gets existing page if needed
        - Navigates to the specified URL if different
        - Waits for page to fully load
        - Takes screenshot if enabled
        - Handles navigation errors
        """
        print(f"**** visit_url called with url={url}")
        print(f"Parameters: url={url}")
        if not url:
            ctx.deps.page = await get_or_create_page(ctx)
            if ctx.deps.page.url != web_surfer.DEFAULT_URL:
                await ctx.deps.page.goto(web_surfer.DEFAULT_URL)
            return f"Successfully ensured default page is loaded: {web_surfer.DEFAULT_URL}"

        try:
            ctx.deps.page = await get_or_create_page(ctx)
            
            # Check if we're already on the requested URL
            if ctx.deps.page.url == url:
                return f"Already on page: {url}"
                
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


    print("Here....3........")

    @web_surfer.tool
    async def reload_page(ctx: RunContext[BrowserState]) -> str:
        """Reload the current page.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: Success message or error message
            
        This function:
        - Reloads the current page
        - Waits for page to fully load
        - Takes screenshot if enabled
        """
        print("**** reload_page called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            await ctx.deps.page.reload()
            await ctx.deps.page.wait_for_load_state()
            logger.info("Reloaded current page")
            if SAVE_SCREENSHOTS:
                await save_screenshot(ctx, "reload_page")
            return "Successfully reloaded current page"
        except Exception as e:
            logger.error(f"Failed to reload page: {str(e)}")
            return f"Failed to reload page: {str(e)}"

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
        print("**** history_back called")
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
        print(f"**** web_search called with query={query}")
        print(f"Parameters: query={query}")
        ctx.deps.page = await get_or_create_page(ctx)
        # if ctx.deps.page is None:
        #     ctx.deps.page = await ctx.deps.context.new_page()
        #     await ctx.deps.page.goto(web_surfer.DEFAULT_URL)
        search_url = WebSurferAgent.SEARCH_URL_TEMPLATE.format(query=query)
        await visit_url(ctx, search_url)
        return f"Successfully performed web search for query '{query}'"

    print("Here.....5 .......")

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
        print("**** page_up called")
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
        print("**** page_down called")
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
        print(f"**** input_text called {selector} {text}")
        print(f"Parameters: selector={selector}, text={text}")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            print("After the get_or_create_page call ......")
            # First check if the element exists using locator
            locator = ctx.deps.page.locator(selector)
            if await locator.count() == 0:
                message = f"No element found with selector '{selector}'. Please verify the selector or try a different one."
                logger.error(message)
                return message
            else:
                print(f"Element found with selector '{selector}'")

            await locator.fill(text, timeout=5000)
            logger.info(f"Input text '{text}' into element with selector '{selector}'")
            if SAVE_SCREENSHOTS:
                await save_screenshot(ctx, "input_text")
            # available_elements = await inspect_page_elements(ctx.deps.page)
            return f"Successfully input text: {text}"
        except Exception as e:
            message = f"Failed to input text: {str(e)}. If it is timing out, you could try alternative fields like text, input, textarea etc."
            logger.error(message)
            print(message)
            return message


    valid_selectors = """
        Here are some valid selectors:
        
        ### **1. CSS Selectors**
        *Standard* CSS selectors are supported.
        
        - **Examples:**
          ```python
          page.locator("div.classname")
          page.locator("#id")
          page.locator("input[type='text']")
          ```
        
        ### **2. Text Selectors**
        Matches elements by their visible text.
        
        - **Exact or partial Text:**
          ```python
          page.locator("text=Partial Text")
          ```
        
        - **Case Insensitivity:**
          ```python
          page.locator("text=/Text/i")
          ```
        
        ### **3. Role Selectors**
        Matches elements by their [ARIA roles](https://www.w3.org/TR/wai-aria/#roles).
        
        - **Examples:**
          ```python
          page.locator("role=button[name='Submit']")
          page.locator("role=checkbox[checked]")
          ```
        
        ### **4. XPath Selectors**
        Standard XPath expressions.
        
        - **Examples:**
          ```python
          page.locator("//div[@class='classname']")
          page.locator("//button[text()='Click me']")
          ```
        
        ---
        
        ### **5. ID Selectors**
        Matches elements by their `id` attribute.
        
        - **Examples:**
          ```python
          page.locator("#unique-id")
          ```
        
        ---
        
        ### **6. Data Test Selectors**
        Matches elements by a custom data attribute (e.g., `data-testid`, `data-test`).
        
        - **Examples:**
          ```python
          page.locator("[data-testid='test-id']")
          page.locator("[data-test='test']")
          ```
        
        ---
        
        ### **7. Attribute Selectors**
        Matches elements with specific attributes.
        
        - **Examples:**
          ```python
          page.locator("[type='submit']")
          page.locator("[name='username']")
          ```
        
        ---
        
        ### **8. Chained Locators**
        Combine selectors to target nested elements.
        
        - **Examples:**
          ```python
          page.locator("div.container >> text='Login'")
          page.locator("div#parent >> button.child-class")
          ```
        
        ---
        
        ### **9. Index-Based Selectors**
        Target specific instances of elements.
        
        - **Examples:**
          ```python
          page.locator("div.classname >> nth=0")  # First match
          page.locator("li >> nth=-1")           # Last match
          ```
        
        ---
        
        ### **10. Has Locator**
        Matches elements containing other elements.
        
        - **Examples:**
          ```python
          page.locator("div:has(button)")
          page.locator("ul:has(li.active)")
          ```
        
        ---
        
        ### **11. Has-Text Selector**
        Matches elements containing specific text.
        
        - **Examples:**
          ```python
          page.locator("button:has-text('Submit')")
          page.locator("a:has-text('Learn More')")
          ```
        
        ---
        
        ### **12. Combining Selectors**
        Use logical operators to combine selectors.
        
        - **Examples:**
          ```python
          page.locator("button:has-text('Save') >> visible=true")
          ```
        
        ---
        
        ### **13. Visible/Hidden State**
        Filters elements based on visibility.
        
        - **Examples:**
          ```python
          page.locator("button >> visible=true")
          page.locator("div.hidden >> hidden=true")
          ```
        
        ---
        
        ### **14. Custom Selectors**
        Playwright supports custom selectors for advanced use cases.
        
        - **Examples:**
          ```python
          page.locator('css=div[role="dialog"] >> text="Confirm"')
          ```
        
        ---
        
        ### **15. Regex Selectors**
        Match text or attributes using regular expressions.
        
        - **Examples:**
          ```python
          page.locator("text=/^Start/")  # Starts with "Start"
          page.locator("[placeholder=/enter your name/i]")  # Case-insensitive match
          ```
        
        ---
        
        Using these selectors, you can precisely interact with elements on a webpage during automation with Playwright in Python.
    """

    @web_surfer.tool
    async def click(ctx: RunContext[BrowserState], selector: str):
        """Click an element on the web page.
        
        Args:
            ctx: The run context containing browser state
            selector: Ony valid CSS or XPaths are allowed - Use ids, names or position of the element when possible. This is the element to click
            
        Returns:
            str: Success message or error message with available elements if click fails
            
        This function:
        - Checks if element exists using selector
        - Attempts to click element with timeout
        - Returns list of available elements if click fails
        - Takes screenshot if enabled
        """
        print(f"**** click called with selector={selector}")
        print(f"Parameters: selector={selector}")
        try:
            ctx.deps.page = await get_or_create_page(ctx)

            # Use Playwright's locator with the provided selector
            locator = ctx.deps.page.locator(selector)
            if await locator.count() == 0:
                print("Element not found...")
                # Attempt a more general search if specific selector fails
                locator = ctx.deps.page.locator("a")
                elements = await locator.evaluate_all("els => els.map(el => el.href)")
                return f"No element found with selector '{selector}'. Available links: {elements}"

            # Click the first matching element
            await locator.first.click()
            logger.info(f"Clicked element with selector '{selector}'")
            if SAVE_SCREENSHOTS:
                await save_screenshot(ctx, "click")
            return f"Successfully clicked element with selector '{selector}'"

        except Exception as e:
            locator = ctx.deps.page.locator("a")
            elements = await locator.evaluate_all("els => els.map(el => el.href)")
            logger.error(f"Failed to click element: {str(e)}")
            return f"Failed to click element: {str(e)}. Available links: {elements}"

    # @web_surfer.tool
    # async def inspect_page(ctx: RunContext[BrowserState]) -> str:
    #     """Inspect and list all interactive elements on the page.
    #
    #     Args:
    #         ctx: The run context containing browser state
    #
    #     Returns:
    #         str: Formatted list of elements or error message
    #
    #     This function:
    #     - Finds all input, textarea, select and button elements
    #     - Returns their tag names, types, IDs, names and placeholders
    #     - Handles inspection errors
    #     """
    #     """Inspect the current page and return information about form elements"""
    #     try:
    #         ctx.deps.page = await get_or_create_page(ctx)
    #         return await inspect_page_elements(ctx.deps.page)
    #     except Exception as e:
    #         logger.error(f"Failed to inspect page: {str(e)}")
    #         return f"Failed to inspect page: {str(e)}"

    # @web_surfer.tool
    # async def close(ctx: RunContext[BrowserState]):
    #     """Close the browser and cleanup resources.
    #
    #     Args:
    #         ctx: The run context containing browser state
    #
    #     Returns:
    #         str: Success message or error message
    #
    #     This function:
    #     - Closes the browser context
    #     - Stops the Playwright instance
    #     - Cleans up all browser resources
    #     """
    #     print("**** close called")
    #     print("Parameters: none")
    #     if ctx.deps.context:
    #         await ctx.deps.context.close()
    #     if ctx.deps.playwright:
    #         await ctx.deps.playwright.stop()
    #     return "Successfully closed browser context and stopped Playwright"


    @web_surfer.tool
    async def save_screenshot(ctx: RunContext[BrowserState], action: str):
        """Save a screenshot of the current page."""
        import uuid
        print("**** save_screenshot called")
        print(f"Parameters: action={action}")
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        # Generate unique filename with UUID suffix
        screenshot_path = f"screenshots/{action}_{uuid.uuid4().hex}.png"
        try:
            await ctx.deps.page.screenshot(path=screenshot_path)
        except:
            print("Something BAD happened here..")
        logger.info(f"Screenshot saved to {screenshot_path}")
        return f"Screenshot saved successfully to {screenshot_path}"

    @web_surfer.tool
    async def get_links(ctx: RunContext[BrowserState]) -> str:
        """Get all links from the current page.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: Formatted list of links with their text and href attributes
            
        This function:
        - Finds all <a> tags on the page
        - Extracts their text content and href attributes
        - Returns them in a formatted string
        """
        print("**** get_links called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            links = await ctx.deps.page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a')).map(a => {
                    return {
                        text: a.textContent.trim(),
                        href: a.getAttribute('href') || ''
                    };
                });
            }""")
            
            # Format the links for display
            formatted_links = []
            for link in links:
                if link['href']:  # Only include links with a valid href
                    formatted_links.append(f"{link['text']} -> {link['href']}")

            rv =  "\n".join(formatted_links) or "No links found on the page"
            return rv
        except Exception as e:
            logger.error(f"Failed to get links: {str(e)}")
            return f"Failed to get links: {str(e)}"

    @web_surfer.tool
    async def get_all_buttons(ctx: RunContext[BrowserState]) -> str:
        """Get all buttons from the current page.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: Formatted list of buttons with their text and type attributes
            
        This function:
        - Finds all button elements on the page
        - Extracts their text content and type attributes
        - Returns them in a formatted string
        """
        print("**** get_all_buttons called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            buttons = await ctx.deps.page.evaluate("""() => {
                return Array.from(document.querySelectorAll('button, input[type="button"], input[type="submit"]')).map(btn => {
                    return {
                        text: btn.textContent?.trim() || btn.value?.trim() || '',
                        type: btn.type || 'button',
                        tag: btn.tagName.toLowerCase()
                    };
                });
            }""")
            
            # Format the buttons for display
            formatted_buttons = []
            for btn in buttons:
                formatted_buttons.append(f"{btn['tag']} ({btn['type']}): {btn['text']}")
            
            return "\n".join(formatted_buttons) or "No buttons found on the page"
        except Exception as e:
            logger.error(f"Failed to get buttons: {str(e)}")
            return f"Failed to get buttons: {str(e)}"

    @web_surfer.tool
    async def get_all_inputs(ctx: RunContext[BrowserState]) -> str:
        """Get all input elements from the current page.
        
        Args:
            ctx: The run context containing browser state
            
        Returns:
            str: Formatted list of inputs with their type, name and placeholder attributes
            
        This function:
        - Finds all input, textarea and select elements on the page
        - Extracts their type, name and placeholder attributes
        - Returns them in a formatted string
        """
        print("**** get_all_inputs called")
        print("Parameters: none")
        try:
            ctx.deps.page = await get_or_create_page(ctx)
            inputs = await ctx.deps.page.evaluate("""() => {
                return Array.from(document.querySelectorAll('input, textarea, select')).map(input => {
                    return {
                        type: input.type || input.tagName.toLowerCase(),
                        name: input.name || '',
                        placeholder: input.placeholder || '',
                        value: input.value || '',
                        options: input.tagName === 'SELECT' ? 
                            Array.from(input.options).map(opt => opt.text) : []
                    };
                });
            }""")
            
            # Format the inputs for display
            formatted_inputs = []
            for inp in inputs:
                details = [f"Type: {inp['type']}"]
                if inp['name']:
                    details.append(f"Name: {inp['name']}")
                if inp['placeholder']:
                    details.append(f"Placeholder: {inp['placeholder']}")
                if inp['value']:
                    details.append(f"Value: {inp['value']}")
                if inp['options'].length > 0:
                    details.append(f"Options: {', '.join(inp['options'])}")
                
                formatted_inputs.append(" | ".join(details))
            
            return "\n".join(formatted_inputs) or "No inputs found on the page"
        except Exception as e:
            logger.error(f"Failed to get inputs: {str(e)}")
            return f"Failed to get inputs: {str(e)}"

    return web_surfer

# Example usage
async def main():
    web_surfer = create_websurfer_agent()
    deps = BrowserState()
    result = await web_surfer.run("Visit the Google homepage, search for 'PydanticAI', scroll down, and click the first link and finally save a screenshot", deps=deps)
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
