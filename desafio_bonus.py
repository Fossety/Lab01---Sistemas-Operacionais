"""
Desafio Extra (Bonus) - 3 threads: 2 depositos + 1 saque.

- Thread-Deposito-1: deposita R$ 1,00, NUM_OPERACOES vezes
- Thread-Deposito-2: deposita R$ 1,00, NUM_OPERACOES vezes
- Thread-Saque-3   : saca    R$ 1,00, NUM_OPERACOES vezes

Saldo final esperado = 2*N - N = N.

O script roda o cenario duas vezes:
  1. sem Lock (com troca de contexto forcada) -> saldo incorreto
  2. com Lock                                  -> saldo correto
"""
import random
import threading
import time

NUM_OPERACOES = 100000
VALOR = 1  # R$ 1,00
PROB_TROCA_CONTEXTO = 0.01


class ContaBancaria:
    def __init__(self, usar_lock):
        self.saldo = 0
        self.usar_lock = usar_lock
        self.lock = threading.Lock()

    def _alterar_saldo(self, delta):
        # Secao critica: leitura -> modificacao -> escrita
        temp = self.saldo
        temp = temp + delta
        # Forca troca de contexto em ~1% das operacoes, em pontos aleatorios.
        # Um yield em TODA operacao faz as threads alternarem em sincronia
        # perfeita e as perdas de deposito/saque se cancelam por coincidencia.
        if random.random() < PROB_TROCA_CONTEXTO:
            time.sleep(0)
        self.saldo = temp

    def movimentar(self, delta):
        if self.usar_lock:
            with self.lock:  # exclusao mutua: uma thread por vez
                self._alterar_saldo(delta)
        else:
            self._alterar_saldo(delta)


def depositar(conta):
    for _ in range(NUM_OPERACOES):
        conta.movimentar(+VALOR)


def sacar(conta):
    for _ in range(NUM_OPERACOES):
        conta.movimentar(-VALOR)


def executar(usar_lock):
    conta = ContaBancaria(usar_lock)
    threads = [
        threading.Thread(target=depositar, args=(conta,), name="Thread-Deposito-1"),
        threading.Thread(target=depositar, args=(conta,), name="Thread-Deposito-2"),
        threading.Thread(target=sacar, args=(conta,), name="Thread-Saque-3"),
    ]

    inicio = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.time()

    saldo_esperado = 2 * NUM_OPERACOES * VALOR - NUM_OPERACOES * VALOR
    modo = "COM Lock" if usar_lock else "SEM Lock"
    print(f"=== {modo} ===")
    print(f"[*] Depositos : 2 threads x {NUM_OPERACOES} x R$ {VALOR:.2f}")
    print(f"[*] Saques    : 1 thread  x {NUM_OPERACOES} x R$ {VALOR:.2f}")
    print(f"[*] Saldo Esperado : R$ {saldo_esperado:,.2f}")
    print(f"[!] Saldo Obtido   : R$ {conta.saldo:,.2f}")
    print(f"[*] Tempo de Execucao : {fim - inicio:.4f} s")
    if conta.saldo != saldo_esperado:
        print(f"[ALERTA] Saldo inconsistente (diferenca de R$ {conta.saldo - saldo_esperado:,.2f})\n")
    else:
        print("[OK] Resultado integro.\n")


def main():
    executar(usar_lock=False)
    executar(usar_lock=True)


if __name__ == "__main__":
    main()
