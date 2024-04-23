import random
import sys

# python scan.py -H http://c4n.fun -C combo1.txt -O iptv.txt -B 15
print('rodando gerador combo http://c4n.fun:80 ...')
try:
    with open('combo1.txt', 'a', encoding='utf8') as f:
        for i in range(10):
            var1 = str(i) * 8
            var2 = str(i) * 6
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush()
        for i in range(10):
            var1 = str(i) * 9
            var2 = str(i) * 9
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush() 
        for i in range(10):
            var1 = str(i) * 8
            var2 = str(i) * 8
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush()
        for i in range(10):
            var1 = str(i) * 7
            var2 = str(i) * 7
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush()
        for i in range(10):
            var1 = str(i) * 6
            var2 = str(i) * 6
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush()                                             
        while True:
            var1 = '0' + ''.join([str(random.randint(0, 9)) for _ in range(7)])
            # Gerando 6 números aleatórios entre 0 e 9 e os armazenando em uma string
            var2 = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            combo = var1 + ':' + var2 + '\n'
            f.write(combo)
            f.flush()
except KeyboardInterrupt:
    print("\nTecla Ctrl+C pressionada. Encerrando o programa...")
    sys.exit(0)  # Sai do programa com status de sucesso