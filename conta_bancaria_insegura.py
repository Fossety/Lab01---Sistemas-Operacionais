"""
Parte 1 - Provocando a Condicao de Corrida (Race Condition).

Duas threads depositam R$ 1,00 na mesma conta, 100.000 vezes cada,
SEM nenhuma sincronizacao. A operacao "ler -> somar -> escrever" nao e
atomica: se o escalonador trocar de thread entre a leitura e a escrita,
um deposito sobrescreve o outro e dados sao perdidos.
"""
import threading
import time

saldo_conta = 0
NUM_OPERACOES = 100000


def depositar():
    global saldo_conta
    for _ in range(NUM_OPERACOES):
        # Operacao NAO-ATOMICA (Leitura, Modificacao e Escrita)
        temp = saldo_conta      # 1. leitura da memoria compartilhada
        temp = temp + 1         # 2. modificacao em variavel local
        saldo_conta = temp      # 3. escrita de volta na memoria compartilhada


def main():
    global saldo_conta
    print(f"[*] Saldo Inicial : {saldo_conta}")

    t1 = threading.Thread(target=depositar, name="Thread-Caixa-1")
    t2 = threading.Thread(target=depositar, name="Thread-App-2")

    # Medicao de tempo adicionada para responder a Questao 2 (custo do Lock)
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
