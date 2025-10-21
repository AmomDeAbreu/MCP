import os
import re
import json
from datetime import date

from playwright.sync_api import Page, expect

preco = None
# Caso este código esteja sendo rodado em uma IDE no desktop, atualize o path file para o caminho do arquivo JSON
path_file = 'preco.json'

def test_has_title(page: Page):
    page.goto("https://www.amazon.com.br/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Amazon"))


def salvar_preco_json(preco):
    """Salva o preço no arquivo JSON. Se o arquivo existir, acrescenta o novo valor
    ao final de uma lista; caso contrário cria o arquivo.

    A função também verifica caminhos alternativos (por exemplo, em Codespaces)
    tentando localizar o arquivo em múltiplos locais antes de criar um novo.
    """

    # Normaliza o valor (armazena em reais, não em centavos)
    valor = preco / 100
    data_atual = date.today().strftime('%d-%m-%Y')  # DD-MM-YYYY

    # Possíveis locais onde o arquivo pode existir (cwd e workspace raiz)
    candidates = [os.path.abspath(path_file), os.path.abspath(os.path.join('/workspaces', os.getenv('GITHUB_WORKSPACE', ''), path_file))]

    # Em Codespaces a variável GITHUB_WORKSPACE pode não estar definida; tentamos também /workspaces
    candidates.append(os.path.abspath(os.path.join('/workspaces', path_file)))

    existing_path = None
    for p in candidates:
        if p and os.path.exists(p):
            existing_path = p
            break

    if existing_path:
        # Lê arquivo existente e atualiza
        with open(existing_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        if not isinstance(data, list):
            data = [data]
        data.append({'preco': valor, 'data': data_atual})
        with open(existing_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        # Cria novo arquivo no cwd
        data = [{'preco': valor, 'data': data_atual}]
        with open(path_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def obter_preco(texto_preco):
    global preco 
    preco = int(texto_preco.replace("R$", "").replace(".", "").replace(",", ""))

    print(f"Preço do produto: R$ {preco/100:.2f}")
    # Salva também no arquivo JSON para persistência
    try:
        salvar_preco_json(preco)
    except Exception as e:
        print(f"Aviso: falha ao salvar preço em JSON: {e}")
    return preco  


def test_search_and_get(page: Page):
    page.goto("https://www.amazon.com.br/")

    # Espera o link "Get started" estar visível
    page.locator("#twotabsearchtextbox").wait_for(state="visible", timeout=60000)
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
   
