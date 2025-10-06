"""
# 1
def guess_the_num():
    from random import randint
    num = randint(1, 100)
    print(num)
    attempts = 0
    try:
        user_num = int(input("Угадывайте число (от 1 до 100): "))
    except:
        print("Введено не число")
    while user_num != num:
        if num > user_num:
            print("Загаданное число больше.")
            attempts+=1

        if num < user_num:
            print("Загаданное число меньше.")
            attempts+=1
        
        if attempts == 3:
            if num%2==0: 
                print("Загаданное число четное.")
            else: 
                print("Загаданное число нечетное.")
        user_num = int(input("Угадывайте число (от 1 до 100): "))

    else:
        print("Вы угадали!")
        return

"""
'''

# 2


def get_keys(d: dict, val: int | list):
    ans = []
    if type(val) == type(1):
        for key, value in d.items():
            if value == val:
                if key not in ans:
                    ans.append(key)
        print(ans)
        return ans
    elif type(val) == type([1]):
        for i in val:
            for key, value in d.items():
                if value == i and key not in ans:
                    ans.append(key)

        return ans


def analyse(string: str):
    string=string.upper()
    alph = sorted([i for i in 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'])
    glas = 'УЕАОИЯЮЭЫЁ'
    sogl = 'ЙЦКНГШЩЗХЪФВПРЛДЖЧСМТЬБ!"№;%:?*()_+-=[]";/><.'
    d = dict()


    for i in alph:
        d[i] = 0


    glas_word = sum([string.upper().count(i) for i in glas])
    sogl_word = sum([string.upper().count(i) for i in sogl])
    spaces_word = string.count(' ')


    for i in string:
        if i in d.keys():
            d[i]+=1
    max_w = sorted([i for i in d.values()])[-3:]
    rare_words = get_keys(d, max_w)[-3:]
    print(rare_words)
    length = len(string.split())


    print(f"Количество гласных символов: {glas_word}")
    print(f"Количество негласных символов: {sogl_word}")
    print(f"Количество пробелов: {spaces_word}")
    print(f"Топ 3 самых часто встречающихся символов: {rare_words[0]}, {rare_words[1]}, {rare_words[2]}")
    print(f"Количество слов: {length}")
    return



string = input('Введите строку: ')
analyse(string=string)

'''
'''
# 3

def game():
    # 1 - stone, 2 - scrissors, 3 - paper
    from random import randint
    user_score = 0
    comp_score = 0

    while user_score < 3 and comp_score < 3:
        user_choice = int(input("Что хотите выбрать? (1 - камень, 2 - ножницы, 3 - бумага) "))
        comp_choice = randint(1, 3)

        if user_choice == comp_choice:
            print("Ничья!")
            continue

        if user_choice == 1 and comp_choice == 3:
            comp_score+=1
            print("Вы проиграли. Компьютер выбрал бумагу")
            continue
        elif user_choice == 1 and comp_choice == 2:
            user_score+=1
            print("Вы победили. Компьютер выбрал ножницы")
            continue

        if user_choice == 2 and comp_choice == 1:
            comp_score+=1
            print("Вы проиграли. Компьютер выбрал камень")
            continue
        elif user_choice == 2 and comp_choice == 3:
            user_score+=1
            print("Вы победили. Компьютер выбрал бумагу")
            continue

        if user_choice == 3 and comp_choice == 2:
            comp_score+=1
            print("Вы проиграли. Компьютер выбрал ножницы")
            continue
        elif user_choice == 3 and comp_choice == 1:
            user_score+=1
            print("Вы победили. Компьютер выбрал камень")
            continue

    else:
        if user_score == 3:
            print("Поздравляем с победой.")
        elif comp_score == 3:
            print("Поздравляем с поражением")

        
game()

'''

# 4


class BankOperations:

    def __init__(self):
        self.user_accounts = dict()
        self.created_accounts = 0

    def transition(self, from_account: int, to_account: int, amount: float):
        if from_account not in self.user_account.keys():
            return "Указаного вами счета, с которого будете переводить - не существует"
        if to_account not in self.user_account.keys():
            return "Указаного вами счета, куда будете переводить - не существует"

        value = self.user_accounts.fromkeys(from_account)
        if value < amount:
            return "Недостаточно средств."
        self.user_accounts[from_account]-=amount
        self.user_accounts[to_account]+=amount
        return "Успешно!"
        
    def repletion(self, to_account: int, score: float):
        if to_account not in self.user_accounts.keys():
            return "Указаного вами счета, который будете пополнять - не существует"
        self.user_accounts[to_account] += score
        return 'Успешно!'

    def write_off(self, to_account: int, score: float):
        if to_account not in self.user_accounts.keys():
            return "Указаного вами счета, который будете пополнять - не существует"
        self.user_accounts[to_account] -= score
        return 'Успешно!'

    def check_out(self):
        s = ''
        if self.user_accounts == {}:
            return "Нет созданных счетов"
        
        for account, value in self.user_accounts.items():
            s += f'Счет №{account}, состояние счета: {value}\n'
        return s
    
    def create_account(self):
        self.user_accounts[self.created_accounts+1] = 0
        return f"Создан счет с №{self.created_accounts+1}"
    

def start_work():
    from time import sleep


    operation = BankOperations()
    s = """
Добро пожаловать в банковские системы.
1 - Создание счета;
2 - Проверка счета;
3 - Пополнение счета;
4 - Списание со счета;
5 - Перевод с счета на счет;

0 - Закончить работу.

Введите цифру: 
    """

    while True:
        sleep(3)
        user_choice = int(input(s))
        if user_choice not in range(1, 6):
            print("Не существует такой операции.")
            continue
        if user_choice == 1:
            print(operation.create_account())
            continue
        if user_choice == 2:
            print(operation.check_out())
            continue
        if user_choice == 3:
            to_account = int(input("Введите номер счета: "))
            amount = float(input("Введите сумму: "))
            print(operation.repletion(to_account=to_account, score=amount))
            continue
        if user_choice == 4:
            to_account = int(input("Введите номер счета: "))
            amount = float(input("Введите сумму: "))
            print(operation.write_off(to_account=to_account, score=amount))
            continue
        if user_choice == 5:
            from_account = int(input("Введите номер счета с которого будете переводить: "))
            to_account = int(input("Введите номер счета на который будете переводить: "))
            amount = float(input("Введите сумму: "))
            print(operation.transition(from_account=from_account, to_account=to_account, amount=amount))
            continue
        if user_choice == 0:
            print("Спасибо за работу!")
            break

start_work()