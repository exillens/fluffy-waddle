
k = []
for n in range(1,10000):
    
    b = bin(n)[2:]
    if n % 4 == 0:
        b = b + bin(n)[-2:]
    else:
        a = n % 4
        b = b + bin(a)[2:]
    r = int(b, 2)
    if r > 250:
        k.append(r)
print(min(k))    
   
    