import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import sys

# Tenta localizar o arquivo preco.json nos mesmos locais que main.py
path_file = 'preco.json'
candidates = [os.path.abspath(path_file), os.path.abspath(os.path.join('/workspaces', os.getenv('GITHUB_WORKSPACE', ''), path_file)), os.path.abspath(os.path.join('/workspaces', path_file))]

data = []
existing_path = None
for p in candidates:
	if p and os.path.exists(p):
		existing_path = p
		break

# Executa o teste que atualiza o preço antes de plotar (opcional)
def run_update_test():
	cmd = [sys.executable, '-m', 'pytest', '-q', '-s', 'main.py::test_search_and_get']
	print('Executando teste para atualizar preço (pode abrir navegador)...')
	try:
		proc = subprocess.run(cmd, capture_output=True, text=True)
		print(proc.stdout)
		if proc.stderr:
			print('stderr:', proc.stderr)
		if proc.returncode != 0:
			print(f'ATENÇÃO: teste retornou código {proc.returncode}. Continuando com dados existentes.')
	except FileNotFoundError:
		print('pytest não encontrado. Instale pytest se quiser executar o teste automaticamente.')

# Tenta rodar o teste para atualizar o arquivo antes de carregar os dados
run_update_test()

if existing_path:
	with open(existing_path, 'r', encoding='utf-8') as f:
		try:
			data = json.load(f)
		except json.JSONDecodeError:
			data = []

if not data:
	print('Nenhum registro de preço encontrado em', existing_path if existing_path else path_file)
else:
	# Extrai listas de datas e preços
	datas = [datetime.strptime(item['data'], '%d-%m-%Y') for item in data if 'data' in item and 'preco' in item]
	precos = [item['preco'] for item in data if 'data' in item and 'preco' in item]

	# Mostra o preço mais recente
	print(f"Preço mais recente: R$ {precos[-1]:.2f} (data: {datas[-1].strftime('%d-%m-%Y')})")

	# Plota histórico
	plt.figure(figsize=(10, 5))
	plt.plot(datas, precos, marker='o')

	# Formata eixo x para mostrar dia/mês (dd/mm)
	plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m'))

	# Inclui o ano do último registro no título
	ano_ultimo = datas[-1].year
	plt.title(f'Histórico de preços - PlayStation 5 ({ano_ultimo})')
	plt.xlabel('Data (dd/mm)')
	plt.ylabel('Preço (R$)')
	plt.grid(True)
	plt.tight_layout()

	# Anota cada ponto com o preço exato
	for x, y in zip(datas, precos):
		plt.annotate(f'R$ {y:.2f}', xy=(x, y), xytext=(0, 6), textcoords='offset points', ha='center', fontsize=8)

	# Salva o gráfico em arquivo sempre
	out_file = 'preco.png'
	try:
		plt.savefig(out_file)
		print(f'Gráfico salvo em {out_file}')
	except Exception as e:
		print(f'Falha ao salvar gráfico em {out_file}: {e}')

	# Tenta mostrar a janela; em ambientes headless isso pode falhar, então capturamos a exceção
	try:
		plt.show()
	except Exception as e:
		print('Não foi possível mostrar o gráfico na tela (ambiente headless?):', e)

