import random

def numeros(qtd):
    num = ''
    for x in range(qtd):
        num += str(random.randint(0, 9))
        print(num)
    
    return num


def saldo():
    num = random.randint(1500, 100000)
    return num


def cartao():
    num = ''
    for x in range(16):
        num += str(random.randint(0, 9))
        if (x + 1) % 4 == 0 and x != 15:
            num += '.'
    return num