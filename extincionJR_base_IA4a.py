import random
import pandas as pd


DEBUG = False


def generar_mazo():
    """Genera todas las cartas según la distribución de fichas proporcionadas por el autor del juego 
    y las añade al mazo.
    This generates the cards (there are only 10 cards but every one of them are different). 
    They are 10 different dinosaurs who eat a different amount of food (leaves, meat, fish and bones)."""
    Protoceratops = {'nombre': 'Protoceratops', 'hoja': 2, 'carne': 0, 'pescado': 0, 'hueso': 0, 'fichas': []}
    Parasaurolophus = {'nombre': 'Parasaurolophus', 'hoja': 3, 'carne': 0, 'pescado': 0, 'hueso': 0, 'fichas': []}
    Triceratops = {'nombre': 'Triceratops', 'hoja': 3, 'carne': 0, 'pescado': 0, 'hueso': 0, 'fichas': []}
    Diplodocus = {'nombre': 'Diplodocus', 'hoja': 4, 'carne': 0, 'pescado': 0, 'hueso': 0, 'fichas': []}
    Carnotaurus = {'nombre': 'Carnotaurus', 'hoja': 0, 'carne': 3, 'pescado': 0, 'hueso': 0, 'fichas': []}
    TRex = {'nombre': 'TRex', 'hoja': 0, 'carne': 3, 'pescado': 0, 'hueso': 1, 'fichas': []}
    Velociraptor = {'nombre': 'Velociraptor', 'hoja': 0, 'carne': 1, 'pescado': 0, 'hueso': 1, 'fichas': []}
    Spinosaurus = {'nombre': 'Spinosaurus', 'hoja': 0, 'carne': 1, 'pescado': 3, 'hueso': 0, 'fichas': []}
    Pteranodon = {'nombre': 'Pteranodon', 'hoja': 0, 'carne': 0, 'pescado': 2, 'hueso': 0, 'fichas': []}
    Baryonix = {'nombre': 'Baryonix', 'hoja': 0, 'carne': 0, 'pescado': 2, 'hueso': 1, 'fichas': []}
    mazo = [Protoceratops, Parasaurolophus, Triceratops, Diplodocus, Carnotaurus, TRex, Velociraptor, Spinosaurus, Pteranodon, Baryonix]
    random.shuffle(mazo)
    return mazo

def generar_bolsa(ncomodinos):
    """Genera todas las fichas de alimento según la distribución proporcionada por el autor 
    y las añade a la bolsa.
    generates the bag with the food tokens and "comodinos" tokens. 
    One joker token can be eaten by any of the dinosaurs so the more joker tokens we have, 
    the easier we win the game. Remember this is a cooperative game and we have to feed the dinosaurs 
    before the extinction comes. """
    bolsa = ['hoja', 'hoja', 'hoja', 'hoja', 'hoja', 'hoja', 'hoja', 
             'carne', 'carne', 'carne', 'carne', 'carne',
             'pescado', 'pescado', 'pescado', 'pescado', 
             'hueso', 'hueso', 'hueso']
    comodinos = []
    if ncomodinos > 0: #Solo si establecemos más de 0 comodinos, añadimos todos esos comodinos a la bolsa.
        for i in range(ncomodinos):
            comodinos.append('comodino')
        bolsa.extend(comodinos)
    random.shuffle(bolsa)
    return bolsa

def preparar_partida():
    """Establece el estado inicial de la partida, incluyendo el mazo de dinosaurios, el de descartes (vacío), 
    la bolsa de fichas, el tablero de extinción (vacío) y la mesa (con 3 cartas iniciales).

    This establish the status of the game "estado" (the deck "mazo", the discards "descartes", 
    the center of the table "mesa" with the dinosaurs to feed, the extinction board "extincion" 
    -a countdown where we put the tokens if they don't match any of the dinosaurs in the table-, 
    the bag "bolsa" with the tokens and the turn "turno" starting from 0).    """
    estado = {
        'mazo': [], #mazo de robo actual
        'descartes': [], #mazo de cartas descartadas: indica lo cerca que se está de lograr ganar la partida
        'extincion': [], #tablero de extinción, que se irá llenando de fichas de alimento descartadas hasta llegar a 6.
        'mesa': [], #3 huecos dispuestos en la mesa para ver hasta 3 dinosaurios en ella 
        'bolsa': [], #bolsa con las fichas de alimento, se sacarán 2 y se elegirá una en cada turno, sin reposición
        'turno': 0
    }
    estado['mazo'] = generar_mazo()
    estado['bolsa'] = generar_bolsa(ncomodinos)
    for i in range(3): #sacamos 3 cartas del mazo para ponerlas en la mesa
        carta = estado['mazo'].pop()
        estado['mesa'].append(carta)
    return estado

def victoria(estado):
    """Se gana la partida si se han descartado y, por tanto, alimentado, a todos los dinosaurios"""
    if len(estado['descartes']) == 10:
        return True
    else:
        return False

def derrota(estado):
    """Se pierde la partida si se ha llenado de fichas el tablero de extinción"""
    if len(estado['extincion']) == 6:
        return True
    else:
        return False

def rescatar_dino(estado):
    """Rescatamos un dinosaurio si conseguimos cubrir todas sus necesidades de fichas de alimento.
    This applies when a dinosaur card in the center of the table is fully fed. It is rescued!"""
    for carta in estado['mesa']:
        if carta['hoja'] + carta['carne'] + carta['pescado'] + carta['hueso'] == 0:
            estado['mesa'].remove(carta)
            estado['descartes'].append(carta)
            dinos_rescatados = len(estado['descartes'])
            if DEBUG: print(f'Habéis rescatado al {carta["nombre"]}. Ya están rescatados {dinos_rescatados} dinosaurios:')
            for dino in estado['descartes']:
                if DEBUG: print(dino['nombre'])
            estado['bolsa'].extend(carta['fichas']) 
            if len(estado['mazo']) > 0: #Cuando se queda un espacio libre añadimos un dinosaurio del mazo (si no está vacío) 
                dino_repuesto = estado['mazo'].pop() 
                estado['mesa'].append(dino_repuesto)
                if DEBUG: print(f'Se ha añadido el {dino_repuesto["nombre"]}.\n')
    return estado

def alimentar_dino_hambriento(estado):
    """Dentro de la mesa, vamos mirando carta por carta hasta encontrar un hueco de alimento que 
    aún falte por rellenar.
    This is the basic code which applies for "comodinos", so it can be fed and substitute any food."""
    for carta in estado['mesa']:
        if carta['hoja'] > 0:
            carta['hoja'] -= 1
            break
        elif carta['carne'] > 0:
            carta['carne'] -= 1
            break
        elif carta['pescado'] > 0:
            carta['pescado'] -= 1
            break
        elif carta['hueso'] > 0:
            carta['hueso'] -= 1
            break
    return estado

def colocar_ficha(ficha1, ficha2, estado):
    """Recibimos 2 fichas y el estado de la partida. Si tenemos un comodín o alguno de los espacios restantes 
    de las cartas de dinosaurios coinciden con las fichas, colocamos ahí la carta y se reduce la necesidad del dino.
    We can only put a token on a dinosaur to feed it if it needs one of the tokens we do have in our hands."""
    for carta in estado['mesa']: #revisamos las cartas que hay en la mesa de una en una (hasta que tengamos una IA más compleja)
        if ficha1 == 'comodino':
            alimentar_dino_hambriento(estado)
            carta['fichas'].append(ficha1)
            estado['bolsa'].append(ficha2)
            random.shuffle(estado['bolsa'])
            if DEBUG: print(f'1 La ficha de {ficha1} se ha colocado en el {carta["nombre"]}, y la de {ficha2} se ha devuelto a la bolsa.\n')
            break
        elif ficha2 == 'comodino':
            alimentar_dino_hambriento(estado)
            carta['fichas'].append(ficha2)
            estado['bolsa'].append(ficha1)
            random.shuffle(estado['bolsa'])
            if DEBUG: print(f'2 La ficha de {ficha1} se ha devuelto a la bolsa y la de {ficha2} se ha colocado en el {carta["nombre"]}.\n')
            break
        elif carta[ficha1] > 0:
            carta[ficha1] = carta[ficha1] - 1
            carta['fichas'].append(ficha1)
            estado['bolsa'].append(ficha2)
            random.shuffle(estado['bolsa'])
            if DEBUG: print(f'1 La ficha de {ficha1} se ha colocado en el {carta["nombre"]}, y la de {ficha2} se ha devuelto a la bolsa.\n')
            break
        elif carta[ficha2] > 0:
            carta[ficha2] = carta[ficha2] - 1
            carta['fichas'].append(ficha2)
            estado['bolsa'].append(ficha1)
            random.shuffle(estado['bolsa'])
            if DEBUG: print(f'2 La ficha de {ficha1} se ha devuelto a la bolsa y la de {ficha2} se ha colocado en el {carta["nombre"]}.\n')
            break

    else:
        estado['extincion'].append(ficha1) #Si ninguna ficha encaja, la colocamos en el tablero de extinción -countdown-.
        estado['bolsa'].append(ficha2)
        random.shuffle(estado['bolsa'])
        if derrota(estado) == False:
            if DEBUG: print(f'3 La ficha de {ficha2} se ha devuelto a la bolsa y la ficha de {ficha1} se ha colocado en el tablero. Quedan {6-len(estado["extincion"])} espacios para la extinción.\n')
            

def partida(estado, ncomodinos):
    """Recibe el estado de la partida y el número de comodinos. Realiza el proceso de la partida.
    Modifica el estado de la partida, actualiza victoria o derrota y avanza los turnos.
    This organize the game step by step (turns), with estado and number of jokers as inputs."""
    while victoria(estado) == False and derrota(estado) == False: #Jugamos un nuevo turno mientras no hayamos ganado ni perdido.
        if DEBUG: print('Sacamos dos fichas de la bolsa...\n')
        ficha1 = estado['bolsa'].pop()
        ficha2 = estado['bolsa'].pop()
        if random.randint(1,2) == 1: #seleccionamos una de las dos fichas al azar (hasta que tengamos una IA más compleja)
            ficha1, ficha2 = ficha2, ficha1
        if DEBUG: print(f'Han salido una ficha de {ficha1} y otra de {ficha2}.\n')
        colocar_ficha(ficha1, ficha2, estado)
        rescatar_dino(estado)
        
        estado['turno'] += 1
        if DEBUG: print(f'Han pasado {estado["turno"]} turnos.\n\n')
        
        if victoria(estado) == True:
            if DEBUG: print('¡Habéis rescatado a todos los dinosaurios! ¡Habéis ganado la partida!')
            if DEBUG: print(f'Número de turnos: {estado["turno"]}')
            if DEBUG: print(f'Dinosaurios rescatados: {len(estado["descartes"])}')
            break              
        
        if derrota(estado) == True:
            if DEBUG: print(f'La ficha de {ficha2} se ha colocado en el tablero. La extinción ha llegado. GAME OVER.')
            if DEBUG: print(f'Número de turnos: {estado["turno"]}')
            if DEBUG: print(f'Dinosaurios rescatados: {len(estado["descartes"])}')
            break


def iniciar_partida(estado, ncomodinos):
    """Recibe estado y ncomodinos y devuelve, tras preparar y realizar la partida, 
    los datos relevantes para el diseño y los incluye en la varaible resultado, que devuelve.
    This function prepares and run the game 'partida' and it returns the resultado with the final simulation data."""
    preparar_partida()
    partida(estado, ncomodinos)
    dinos_rescatados = len(estado['descartes'])
    resultado = {'n_comodinos': ncomodinos, 'dinos_rescatados': dinos_rescatados, 'victoria': victoria(estado), 'n_turnos': estado['turno']}
    return resultado



#In the next few lines we just change the number of comodinos (joker tokens), run the simulation 10.000 times and sabe to a csv.
resultados0 = []
for i in range(10000):
    ncomodinos = 0
    estado = preparar_partida()
    resultado = iniciar_partida(estado, ncomodinos)
    resultados0.append(resultado)
df0 = pd.DataFrame(resultados0)
df0.to_csv('datos0.csv', index=False)

resultados1 = []
for i in range(10000):
    ncomodinos = 1
    estado = preparar_partida()
    resultado = iniciar_partida(estado, ncomodinos)
    resultados1.append(resultado)
df1 = pd.DataFrame(resultados1)
df1.to_csv('datos1.csv', index=False)

resultados2 = []
for i in range(10000):
    ncomodinos = 2
    estado = preparar_partida()
    resultado = iniciar_partida(estado, ncomodinos)
    resultados2.append(resultado)
df2 = pd.DataFrame(resultados2)
df2.to_csv('datos2.csv', index=False)

resultados3 = []
for i in range(10000):
    ncomodinos = 3
    estado = preparar_partida()
    resultado = iniciar_partida(estado, ncomodinos)
    resultados3.append(resultado)
df3 = pd.DataFrame(resultados3)
df3.to_csv('datos3.csv', index=False)

resultados4 = []
for i in range(10000):
    ncomodinos = 4
    estado = preparar_partida()
    resultado = iniciar_partida(estado, ncomodinos)
    resultados4.append(resultado)
df4 = pd.DataFrame(resultados4)
df4.to_csv('datos4.csv', index=False)

df = pd.concat([df0, df1, df2, df3, df4], axis=0)
df.to_csv('datos_extincion.csv', index=False)

