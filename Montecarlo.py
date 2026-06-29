import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

N = 1000  # nombre de partícules
precisio  = 0.01  # precisió de la simulació

T = np.logspace(-1, 3, num=70)  # temperatures entre 0.01 i 1000

estats = np.array([0, 1, 10])  # estats possibles d'una partícula
X = np.random.choice(estats, size=N)  # estats inicials de les partícules

def P_acc(a,b,temperatura): # Probablitat d'accepatacció
    delta = (a - b)
    if delta <= 0:
        return 1.0
    else:
        return np.exp(-delta / temperatura)

ocupacio0 = []
ocupacio1 = []
ocupacio2 = []
for t in T: #Per cada temperatura deixem evoluconoar el sistema fins arribar a l'equilibri
    x = X.copy() # Copiem els estats inicials avans de modificarlos
    error = precisio + 1 # donem un valor a l'error per començar el bucle
    while error > precisio:
        E_inicial = np.sum(x) #Energia avans de modificar els estats
        for i in range(2*N): # Fem 2*N intents de canvi d'estat
            particula = np.random.randint(N) # Triem una partícula a l'atzar
            canvi = np.random.choice([s for s in estats if s != x[particula]]) # Triem un nou estat per la partícula
            if np.random.rand() < P_acc(canvi,x[particula],t): # Acceptem o rebutgem el microstat
                x[particula] = canvi
        E_final = np.sum(x) # Energia després de modificar els estats
        error = abs(E_final - E_inicial) / E_inicial # calculem l'error relatiu per comprovar si hem arribat a l'equilibri
    ocupacio0.append(np.sum(x == 0)) #Guardem el nombre de partícules en cada estat per cada temperatura
    ocupacio1.append(np.sum(x == 1))
    ocupacio2.append(np.sum(x == 10)) 

def f(T,E): #Distribucions teòriques de cada nivell en funció de la temperatura.
    return np.exp(-E/T)/(1 + np.exp(-1/T) + np.exp(-10/T))

# Grafica de ocupació en funció de temperatura
plt.plot(T, N*f(T,0),'--',color = "#A7C7E7") 
plt.plot(T, N*f(T,1),'--',color = "#A8E6A3")
plt.plot(T, N*f(T,10),'--',color = "#F4A7A7")

plt.plot(T, ocupacio0,'.',color = "#2C6DA9", label='Fonamental')
plt.plot(T, ocupacio1, '.',color = "#227D28", label='1r excitat')
plt.plot(T, ocupacio2, '.',color = "#9B0505", label='2n excitat')

plt.vlines(10/np.log(N),0,N,color='black',linestyle='dashed',label=r'$T_c$')
plt.xscale('log')
plt.xlabel(r'$kT/\varepsilon$') 
plt.ylabel('Ocupació')
plt.xlim(0.1, 1000)
plt.tick_params(axis='both', which='both', top=True, right=True,direction='in')
plt.legend()
plt.show()


# Fluctuacions relatives de l'energia en funció del nombre de partícules
Nv = [10, 100, 1000, 5000, 10000] # llista amb el nombre de partícules a avaluar
T_fixa = 300  # temperatura fixa per arribar a l'equilibri

fluctuacions_relatives = []

for N in Nv:
    X_inici = np.random.choice(estats, size=N) # estats inicials de les partícules
    x = X_inici.copy()
        
    energies_equilibri = []
    passos_mesura = 500  # nombre de mostres independents d'energia
    
    for _ in range(passos_mesura):
        for i in range(N): 
            particula = np.random.randint(N) # Triem una partícula a l'atzar
            canvi = np.random.choice([s for s in estats if s != x[particula]]) # Triem un nou estat per la partícula
            if np.random.rand() < P_acc(canvi, x[particula], T_fixa): # Acceptem o rebutgem el microstat
                x[particula] = canvi
        energies_equilibri.append(np.sum(x)) # guardem l'energia total del microstat
        
    E_mitjana = np.mean(energies_equilibri) # energia mitjana
    Desviacio_E = np.std(energies_equilibri) # desviació estàndard
    fluctuacions_relatives.append(Desviacio_E / E_mitjana) # calculem la fluctuació relativa

# Representació gràfica
plt.figure()
plt.plot(Nv, fluctuacions_relatives, 'o', label='Fluctuació simulada')

constant_ajust = fluctuacions_relatives[0] * np.sqrt(Nv[0])
eixX = np.linspace(9, 11000, 20)
plt.plot(eixX, constant_ajust / np.sqrt(eixX), '--', color='red', label=r'Teoria $\propto 1/\sqrt{N}$')

plt.xscale('log')
plt.yscale('log')
plt.xlim(9, 11000)
plt.ylim(0.01, 1)
ax = plt.gca()
ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=5))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(1, 10), numticks=10))
ax.yaxis.set_major_formatter(ticker.LogFormatterSciNotation(base=10.0))
ax.yaxis.set_minor_formatter(ticker.LogFormatterSciNotation(base=10.0, labelOnlyBase=False))
plt.tick_params(axis='both', which='both', top=True, right=True, direction='in')
plt.tick_params(axis='y', which='minor', length=4)
plt.xlabel('Nombre de partícules ($N$)')
plt.ylabel(r"Fluctuació relativa de l'energia ($\sigma_E / \langle E \rangle$)")
plt.legend()
plt.show()
