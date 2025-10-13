import re
from playwright.sync_api import Page, expect

preco = None

def test_has_title(page: Page):
    page.goto("https://www.amazon.com.br/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Amazon"))


def obter_preco(texto_preco):
    global preco 
    preco = int(texto_preco.replace("R$", "").replace(".", "").replace(",", ""))
    print(f"Preço do produto: R$ {preco/100:.2f}")
    return preco  


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
    print('\n' + texto_preco)
    obter_preco(texto_preco)
   
