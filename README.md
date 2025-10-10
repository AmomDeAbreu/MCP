# README for MCP Playstation Project

## Overview

The MCP Playstation Project is a Playwright-based test automation system that validates and extracts product information from Amazon Brazil's website [1](#0-0) . The system specifically targets PlayStation 5 console listings through automated browser testing [2](#0-1) .

## Purpose

This project serves two primary functions:
1. **Functional Testing**: Validates Amazon Brazil's search functionality and page navigation [3](#0-2) 
2. **Data Extraction**: Scrapes PlayStation 5 product pricing information [4](#0-3) 

## Project Structure

```
MCP/
├── main.py              # Core test automation logic
├── __pycache__/         # Python bytecode cache
└── README.md            # Project documentation
```

All test logic resides in a single file (`main.py`) containing two test functions [5](#0-4) .

## Test Functions

### `test_has_title(page: Page)`
A smoke test that validates Amazon Brazil's homepage accessibility by checking for "Amazon" in the page title [6](#0-5) .

### `test_search_and_get(page: Page)`
The main automation workflow that:
- Navigates to Amazon Brazil [7](#0-6) 
- Searches for "playstation 5" [8](#0-7) 
- Locates the "Console PlayStation 5 - Digital Edition" product [9](#0-8) 
- Extracts and prints the product price [4](#0-3) 

## Dependencies

- **playwright**: Browser automation framework [10](#0-9) 
- **pytest**: Test execution framework (implicit via test function naming) [11](#0-10) 
- **re**: Regular expression support for title validation [12](#0-11) 

## Key Selectors

The system uses specific CSS selectors to interact with Amazon's interface:
- `#twotabsearchtextbox`: Search input field [13](#0-12) 
- `#nav-search-submit-text`: Search submit button [14](#0-13) 
- `div[data-cy="asin-faceout-container"]`: Product container [9](#0-8) 
- `span.a-offscreen`: Price text element [15](#0-14) 

## Execution

Tests are executed using pytest's test discovery mechanism, which automatically finds and runs functions prefixed with `test_` [16](#0-15) . The `page` fixture is provided by the `pytest-playwright` plugin<cite />.

## Notes

The codebase contains commented-out code (lines 26-41) that appears to be experimental or deprecated test logic for alternative element selection strategies [17](#0-16) . The current implementation uses a simpler approach focused on the Digital Edition PlayStation 5 console<cite />.

Wiki pages you might want to explore:
- [Overview (AmomDeAbreu/MCP)](/wiki/AmomDeAbreu/MCP#1)

### Citations

**File:** main.py (L1-1)
```python
import re
```

**File:** main.py (L2-2)
```python
from playwright.sync_api import Page, expect
```

**File:** main.py (L4-25)
```python
def test_has_title(page: Page):
    page.goto("https://www.amazon.com.br/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Amazon"))

def test_search_and_get(page: Page):
    page.goto("https://www.amazon.com.br/")

    # Espera o link "Get started" estar visível
    page.locator("#twotabsearchtextbox").fill("playstation 5");
    element1 = page.locator("#nav-search-submit-text");
    element1.click()
    expect(page).to_have_title(re.compile("playstation"))
    # Encontra o produto pelo texto do título
    produto = page.locator('div[data-cy="asin-faceout-container"]:has-text("Console PlayStation 5 - Digital Edition")').first

    # Dentro desse produto, pega o preço
    preco = produto.locator("span.a-offscreen").first
    preco.wait_for(state="visible", timeout=5000)
    texto_preco = preco.inner_text()
    print(texto_preco)
```

**File:** main.py (L26-41)
```python
    # element = page.locator('a[href*="B09FGCKBPK"]:has-text("Console PlayStation 5 - Digital Edition")')
    # div.wait_for(state="visible", timeout=5000)
    # print("HTML do link Playstation 5:", element.inner_html())

    # element = page.get_by_role("link", name="Get started")
    # element.wait_for(state="visible", timeout=5000)
    # print("HTML do link Get started:", element.inner_html())

    # # Click the get started link.
    # element.click()

    # # Expects page to have a heading with the name of Installation.
    # expect(page.get_by_role("heading", name="Installation")).to_be_visible()
    # title = page.get_by_role("heading", name="Installation")
    # title.wait_for(state="visible", timeout=5000)
    # print("HTML do título Installation:", title.inner_html())
```
