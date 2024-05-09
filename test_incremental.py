import time

usuarios = {}

names = ['al', 'le', 'lo']

def incremental(usuario, hora):
    if not usuario+hora in usuarios:
        usuarios[usuario+hora] = 0

    usuarios[usuario + hora] = usuarios[usuario + hora] + 1
    print(usuarios[usuario + hora])



for name in names:
    i = 0
    while i < 10:
        incremental(name, time.strftime("%M"))
        i = i + 1

print(usuarios)
