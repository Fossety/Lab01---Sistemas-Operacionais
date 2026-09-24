"""
Parte 1 (variante) - Condicao de Corrida forcada.

Em versoes recentes do CPython (3.10+), o interpretador so troca de thread
em pontos especificos (saltos de volta no laco, chamadas de funcao). Como
entre "temp = saldo_conta" e "saldo_conta = temp" nao existe nenhum desses
pontos, o codigo original pode dar 200.000 sempre, escondendo o problema.

Aqui inserimos time.sleep(0) dentro da secao critica. Ele nao "dorme":
apenas libera o GIL e pede ao SO para escalonar outra thread (yield),
simulando uma troca de contexto no pior momento possivel.
"""
import threading
import time

saldo_conta = 0
NUM_OPERACOES = 100000


def depositar():
    global saldo_conta
    for _ in range(NUM_OPERACOES):
        temp = saldo_conta      # 1. leitura
        temp = temp + 1         # 2. modificacao
        time.sleep(0)           # >>> troca de contexto forcada no meio da secao critica
        saldo_conta = temp      # 3. escrita (pode sobrescrever o deposito da outra thread)


def main():
    global saldo_conta
    print(f"[*] Saldo Inicial : {saldo_conta}")

    t1 = threading.Thread(target=depositar, name="Thread-Caixa-1")
    t2 = threading.Thread(target=depositar, name="Thread-App-2")

    inicio = time.time()
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    fim = time.time()

    saldo_esperado = NUM_OPERACOES * 2
    print(f"[*] Saldo Esperado : {saldo_esperado}")
    print(f"[!] Saldo Obtido : {saldo_conta}")
    print(f"[*] Tempo de Execucao : {fim - inicio:.4f} s")

    if saldo_conta != saldo_esperado:
        perdidos = saldo_esperado - saldo_conta
        print(f"\n[ALERTA] Condicao de Corrida detectada! Houve perda de dados ({perdidos} depositos perdidos).")
    else:
        print("\n[OK] Resultado integro.")


if __name__ == "__main__":
    main()
