s = '123456789'
n = int(input('Введите число: '))
if n >= 9:
    for i in range(10,n+1):
        s+=str(i)
print(f'ряд:{s}')
print(f'Ваше число: {s[n]}')



