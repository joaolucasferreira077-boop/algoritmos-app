# Laboratório de Algoritmos Clássicos

Aplicação web para executar seis algoritmos clássicos com valores escolhidos pelo usuário e acompanhar, passo a passo, como cada um chega ao resultado.

## Tecnologias

- **Frontend:** HTML, CSS e JavaScript puro, servidos pelo próprio Flask (template Jinja2)
- **Backend:** Python + Flask (API REST)
- **Servidor de produção:** Gunicorn
- **Banco de dados:** nenhum (os cálculos são feitos a cada requisição)
- **Hospedagem:** AWS Elastic Beanstalk ou Render
- **Versionamento:** Git e GitHub

## Requisitos

- Python 3.10 ou superior
- pip

## Instalação

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```bash
python app.py
```

- Aplicação: http://localhost:5000

Em produção, o app é iniciado pelo Gunicorn:

```bash
gunicorn app:app
```

## Publicação na nuvem

A aplicação gera uma URL pública única para a interface e para a API.

**AWS Elastic Beanstalk**
1. Compacte `app.py`, `requirements.txt`, `Procfile` e a pasta `templates/` em um `.zip`, com esses itens na raiz do arquivo.
2. No console da AWS, abra **Elastic Beanstalk → Create application**.
3. Escolha **Web server environment**, a plataforma **Python** e o preset **Single instance**.
4. Em **Application code**, envie o `.zip` e finalize em **Submit**.
5. Quando a saúde do ambiente ficar verde, a URL aparece no topo da página, por exemplo `http://entregavelfive-env.eba-6bxegvmj.us-east-2.elasticbeanstalk.com/`.

O `Procfile` define o comando de inicialização:

```
web: gunicorn app:app
```

**Render (alternativa gratuita, sem cartão)**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Instance Type: Free

## Primeiro acesso

Não há login nem cadastro. Abra a URL da aplicação, escolha um algoritmo no menu, digite os valores e clique em **Executar**.

## Algoritmos disponíveis

| Algoritmo | Entrada | Resultado |
|---|---|---|
| Fibonacci | quantidade de termos | sequência de Fibonacci |
| Fatorial | valor de `n` | `n!` |
| MDC (Euclides) | dois números | maior divisor comum |
| Crivo de Eratóstenes | limite superior | lista de primos até o limite |
| Busca binária | lista e valor procurado | posição do valor ou `-1` |
| Bubble sort | lista de números | lista ordenada |

## Regras de negócio

- Todo algoritmo devolve o **resultado** e a lista de **passos** executados, na ordem.
- Os valores são validados no servidor, e entradas fora dos limites retornam erro `400` com uma mensagem explicativa.
- Limites de entrada:
  - Fibonacci: `n` de 1 a 60
  - Fatorial: `n` de 0 a 50
  - MDC: `a` e `b` de 1 a 1.000.000.000
  - Crivo: `n` de 2 a 500
  - Busca binária e Bubble sort: lista de 1 a 30 inteiros separados por vírgula
  - Busca binária: `alvo` de -1.000.000.000 a 1.000.000.000
- A busca binária ordena a lista antes de procurar e retorna a posição na lista já ordenada.
- Resultados inteiros são devolvidos como texto, para não perder precisão no navegador (o fatorial de 50 passa de 60 dígitos).
- Algoritmo inexistente retorna `404`.

## Endpoints principais

| Método | Rota | Descrição | Parâmetros |
|---|---|---|---|
| GET | `/` | Interface web | — |
| GET | `/api/fibonacci` | Sequência de Fibonacci | `n` |
| GET | `/api/fatorial` | Fatorial | `n` |
| GET | `/api/mdc` | MDC pelo algoritmo de Euclides | `a`, `b` |
| GET | `/api/crivo` | Primos pelo Crivo de Eratóstenes | `n` |
| GET | `/api/busca` | Busca binária | `lista`, `alvo` |
| GET | `/api/bubble` | Ordenação Bubble sort | `lista` |

Exemplo de chamada:

```bash
curl "http://localhost:5000/api/mdc?a=252&b=105"
```

Resposta:

```json
{
  "resultado": "21",
  "passos": [
    "252 = 105 × 2 + 42",
    "105 = 42 × 2 + 21",
    "42 = 21 × 2 + 0",
    "Resto 0: o MDC é 21"
  ]
}
```

Resposta de erro:

```json
{ "erro": "'n' deve estar entre 0 e 50." }
```

## Estrutura

```
app.py                   # Flask, algoritmos, validação e rotas
templates/index.html     # interface (HTML, CSS e JavaScript)
requirements.txt         # dependências (Flask e Gunicorn)
Procfile                 # comando de inicialização no Elastic Beanstalk
.gitignore
README.md
```
