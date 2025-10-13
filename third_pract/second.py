def check_scobes(s: str):
    counter = 0
    for i in range(len(s)):
        if s[i] == '(':
            counter+=1
        if s[i] == ')':
            counter-=1
        if counter < 0: return False
    if counter == 0: return True
    return False

s = str(input("Enter a value: "))
print(f'Answer: {"Все верно" if check_scobes(s) else "Вы ошиблись."}')