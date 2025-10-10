import re
from playwright.sync_api import Page, expect

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



