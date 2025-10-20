# Simluation convert gital data to digital sinal

def convert(mensagem):
    list_sinal = []
    for l in mensagem:
        if l == "0":
            list_sinal.append("+3v")
        elif l == "1":
            list_sinal.append("-3v")      
        else:
            pass
    return list_sinal 

print(convert("10011"))     