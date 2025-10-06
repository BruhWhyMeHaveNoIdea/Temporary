"""
# 1
alp_en = ''.join(sorted([i for i in 'QWERTYUIOPASDFGHKJKLZXCVBNM']))
alp_rus = ''.join(sorted([i for i in 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ']))


def ccode(string: str):
    lang = ''
    if any([i for i in [j in string for j in alp_en]]):
        lang = alp_en+'A'
    elif any([i for i in [j in string for j in alp_rus]]):
        lang = alp_rus+'А'
    else:
        raise ValueError("Not known language")
    words = [i.upper() for i in string]
    ans = ''
    while words:
        word = words.pop(0)
        if word == ' ': 
            ans+=' '
            continue
        cur_index = lang.index(word)
        ans+=lang[cur_index+1]
    return ans


def decode(string: str):
    string=string.upper()
    lang = ''
    if any([i for i in [j in string for j in alp_en]]) and any([i for i in [j in string for j in alp_rus]]): return "Не совмещаем"
    if any([i for i in [j in string for j in alp_en]]):
        lang = 'A'+alp_en
    elif any([i for i in [j in string for j in alp_rus]]):
        lang = 'А'+alp_rus
    else:
        raise ValueError("Not known language: {string}")
    words = [i.upper() for i in string]
    ans = ''
    while words:
        word = words.pop(0)
        if word == ' ': 
            ans+=' '
            continue
        cur_index = lang.index(word)
        ans+=lang[cur_index-1]
    return ans

string = input("Insert a value: ")

choosen_type = int(input("Insert a type: 1 for code, 0 for decode: "))
if choosen_type not in [0, 1]:
    print("Wrong type")
elif choosen_type == 0:
    print(decode(string=string))
else:
    print(ccode(string=string))

"""




"""
# 2

def check_winners(scores: list, student_score: int):
    scores = sorted(scores)
    if any([int(i) == int(student_score) for i in scores[-3:]]):
        return "Вы в тройке победителей!"
    else:
        return "Вы не попали в тройку победителей. "

scores = [20, 48, 52, 38, 36, 13, 7, 41, 34, 24, 5, 51, 9, 14, 28]
student_score = int(input("Введите ваши баллы: "))
print(check_winners(scores=scores, student_score=student_score)) 
"""




"""
# 3

def print_pack_report(num):
    if num < 2: raise ValueError("Wrong input")
    f1 = num%3 == 0
    f2 = num%5 == 0
    if f1 and f2:
        return f"{num} - расфасуем по 3 или по 5"
    elif f1:
        return f"{num} - расфасуем по 3"
    elif f2:
        return f"{num} - расфасуем по 5"
    else:
        return f"{num} - не заказываем"
    
num = int(input("Введите кол-во пироженных: "))
print(print_pack_report(num))
"""




"""
# 4

def generate_password(settings: dict):
    from random import choice
    up = alphabet = ''.join(sorted([i for i in 'QWERTYUIOPASDFGHJKLZXCVBNM']))
    down = alphabet = ''.join(sorted([i for i in 'QWERTYUIOPASDFGHJKLZXCVBNM'.lower()]))
    ssymbol = '!@#$%^&*()_'
    nums='0123456789'
    alphabet = ''
    ans = ''
    if settings["lcase"] == False and settings["ucase"] == False: return "А что использовать то?"
    if settings["lcase"] == True: alphabet+=down
    if settings["ucase"] == True: alphabet+=up
    if settings["nums"] == True: alphabet+=nums
    if settings["ssymbol"] == True: alphabet+=ssymbol
    for i in range(settings["length"]):
        ans+=choice(alphabet)
    return ans


lcase = input("Использовать нижний регистр? Да/Нет: ").lower()
ucase = input("Использовать верхний регистр? Да/Нет: ").lower()
ssymbol = input("Использовать спец. символ? Да/Нет: ").lower()
nums = input("Использовать цифры? Да/Нет: ").lower()
length = int(input("Введите длину пароля: "))

if not(all([i in ["да", "нет"] for i in [lcase, ucase, ssymbol, nums]])):
    print("Введены некорректные данные")
    exit()

if type(length) != type(0):
    print("Введены некорректные данные")
    exit()

settings = {
    "lcase": True if lcase=="да" else False,
    "ucase": True if ucase=="да" else False,
    "ssymbol": True if lcase=="да" else False,
    "nums": True if lcase=="да" else False,
    "length": length
}

print(generate_password(settings=settings))

"""




"""
# 5

def from_roman(string: str):
    romans = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    answer = 0
    before = 0
    string = reversed(string)
    for i in string:
        arabic = romans[i]
        if arabic < before: answer-=arabic
        else: answer+=arabic
        before = arabic
    return answer

def to_roman(string: int):
    romans = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX',5: 'V', 4: 'IV', 1 : 'I'}
    answer = ''
    for i, j in romans.items():
        while string >= int(i):
            answer+=j
            string-=int(i)
    return answer

num = input("Введите число: ")

if any([i in 'QWERTYUIOPASDFGHJKLZXCVBNM'+'QWERTYUIOPASDFGHJKLZXCVBNM'.lower() for i in str(num)]):
    print(from_roman(num))
else:
    print(to_roman(num))

"""




'''
def game(word: str):
    word = word.lower()
    letters = set()
    attempts = 6
    while attempts > 0:
        current = ''.join([i if i in letters else '_' for i in word])
        if '_' not in current:
            print(f"Вы победили. Слово: {word}")
            return
        
        print(f'У вас осталось {attempts} попыток.')
        guess = input('Угадывайте букву: ').lower()
        
        if guess in letters:
            print(f"Вы уже указывали эту букву. Буквы: {' '.join(letters)}")
            continue
        
        if guess in word:
            letters.add(guess)
            print("Верно! Эта буква есть в слове.")
        else:
            attempts -= 1
            print(f"Вы не угадали. У вас осталось {attempts} попыток.")
    
    print('Вы проиграли')
    print(f'Загаданное слово было: {word}')

word = input("Введите слово, которое вы хотите, чтобы отгадали: ")
game(word=word)
'''

