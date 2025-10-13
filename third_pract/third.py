
def move_to(string: str, sym: str, start: bool = True) -> str:
    if start:
        counter = 0
        for i in range(len(string)):
            if string[i] == sym:
                counter+=1
        string = string.replace(sym, '')
        string = sym*counter+string
        return string
    counter = 0
    for i in range(len(string)):
        if string[i] == sym:
            counter+=1
    string = string.replace(sym, '')
    string = string+sym*counter
    return string


s = str(input("Enter a value: "))
sym = str(input("Enter a symbol: "))
forward = bool(input("Enter a variant: 0 to move to start, 1 to move to end: "))
print(f'Answer: {move_to(s, sym, True)}')
