import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# ---------- Algoritmos: cada função devolve (resultado, passos) ----------

def fibonacci(n):
    a, b = 0, 1
    seq, steps = [], []
    for i in range(n):
        seq.append(a)
        steps.append(f"F({i}) = {a}")
        a, b = b, a + b
    return seq, steps


def fatorial(n):
    resultado, steps = 1, []
    for i in range(2, n + 1):
        anterior = resultado
        resultado *= i
        steps.append(f"{anterior} × {i} = {resultado}")
    if not steps:
        steps.append("0! e 1! valem 1")
    return resultado, steps


def mdc(a, b):
    steps = []
    x, y = a, b
    while y != 0:
        steps.append(f"{x} = {y} × {x // y} + {x % y}")
        x, y = y, x % y
    steps.append(f"Resto 0: o MDC é {x}")
    return x, steps


def crivo(n):
    eh_primo = [True] * (n + 1)
    eh_primo[0:2] = [False, False][: n + 1]
    steps = []
    i = 2
    while i * i <= n:
        if eh_primo[i]:
            riscados = list(range(i * i, n + 1, i))
            for m in riscados:
                eh_primo[m] = False
            if riscados:
                steps.append(f"Primo {i}: risca {', '.join(map(str, riscados))}")
        i += 1
    primos = [k for k, v in enumerate(eh_primo) if v]
    return primos, steps or ["Nenhum número a riscar"]


def busca_binaria(lista, alvo):
    lista = sorted(lista)
    steps = [f"Lista ordenada: {lista}"]
    ini, fim = 0, len(lista) - 1
    while ini <= fim:
        meio = (ini + fim) // 2
        steps.append(f"Intervalo [{ini}..{fim}], meio = posição {meio} (valor {lista[meio]})")
        if lista[meio] == alvo:
            steps.append(f"Encontrado na posição {meio}")
            return meio, steps
        if lista[meio] < alvo:
            ini = meio + 1
        else:
            fim = meio - 1
    steps.append("Intervalo vazio: valor não está na lista")
    return -1, steps


def bubble_sort(lista):
    v = list(lista)
    steps = [f"Início: {v}"]
    for passo in range(len(v) - 1):
        trocou = False
        for j in range(len(v) - 1 - passo):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                trocou = True
        steps.append(f"Passada {passo + 1}: {v}")
        if not trocou:
            break
    return v, steps


# ---------- Rotas ----------

def inteiro(nome, minimo, maximo):
    try:
        valor = int(request.args.get(nome, ""))
    except ValueError:
        raise ValueError(f"'{nome}' precisa ser um número inteiro.")
    if not minimo <= valor <= maximo:
        raise ValueError(f"'{nome}' deve estar entre {minimo} e {maximo}.")
    return valor


def lista_inteiros(nome):
    bruto = request.args.get(nome, "")
    try:
        valores = [int(p) for p in bruto.replace(";", ",").split(",") if p.strip()]
    except ValueError:
        raise ValueError("Use apenas números inteiros separados por vírgula.")
    if not 1 <= len(valores) <= 30:
        raise ValueError("Informe de 1 a 30 números.")
    return valores


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/<nome>")
def api(nome):
    try:
        if nome == "fibonacci":
            r, s = fibonacci(inteiro("n", 1, 60))
        elif nome == "fatorial":
            r, s = fatorial(inteiro("n", 0, 50))
        elif nome == "mdc":
            r, s = mdc(inteiro("a", 1, 10**9), inteiro("b", 1, 10**9))
        elif nome == "crivo":
            r, s = crivo(inteiro("n", 2, 500))
        elif nome == "busca":
            r, s = busca_binaria(lista_inteiros("lista"), inteiro("alvo", -10**9, 10**9))
        elif nome == "bubble":
            r, s = bubble_sort(lista_inteiros("lista"))
        else:
            return jsonify(erro="Algoritmo não encontrado."), 404
    except ValueError as e:
        return jsonify(erro=str(e)), 400
    return jsonify(resultado=str(r) if isinstance(r, int) else r, passos=s)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
