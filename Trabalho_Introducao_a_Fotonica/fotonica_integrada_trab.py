
import numpy as np
import matplotlib.pyplot as plt

P_dB = []

# comprimento de onda (wavelength)
wl = np.round(np.arange(1.4e-06, 1.6e-06, 0.1e-09), 10)

# epsilon = 3.8*8.85*(10**(-12)) # https://www.electricalelibrary.com/2018/11/02/o-que-e-permissividade-eletrica/
# https://prod-edam.honeywell.com/content/dam/honeywell-edam/pmt/hps/products/pmc/field-instruments/smartline-level-transmitters/smartline-guided-wave-level-transmitters/pmt-hps-dielectric-constant-table.pdf?download=false
# mi = (1-1.128*(10**(-5)))*4*np.pi*(10**(-7)) # https://en.wikipedia.org/wiki/Magnetic_susceptibility
# https://arxiv.org/abs/1403.4760
# https://www.sciencedirect.com/science/article/abs/pii/S1090780714000433?via%3Dihub

epsilon = 8.85*(10**(-12))
mi = 4*np.pi*(10**(-7))


v = 1/np.sqrt(mi*epsilon)  # velocidade da luz dentro do material

d_b1 = 0.02  # braço 1 com tamanho 2 cm
# d_b1 = v/f
d_b2 = 0.02  # braço 2 com tamanho 2 cm
# d_b2 = v/f
delta_b2 = 0.001  # diferença de 1 mm no braço 2

f = v/wl  # frequencia correspondente ao comprimento de onda da luz no vácuo

for i in f:
    beta = 2*np.pi*i/v  # constante de fase dentro do material

    t = np.arange(0, 1/f[-1], (1/f[-1])/1000)

    E1 = np.cos(np.multiply(2*np.pi*i, t) - np.multiply(beta, d_b1))  # onda 1
    E2 = np.cos(np.multiply(2*np.pi*i, t) -
                np.multiply(beta, (d_b2+delta_b2)))  # onda 2

# plt.figure(1)
# plt.plot(t,E1,'r',t,E2,'b',t,E1+E2,'black')
# plt.show()

    P_dB.append(20*np.log10(np.max(E1+E2)))

# print(P_dB)
idx = np.where(P_dB == np.max(P_dB))[0][0]  # Pegando apenas o primeiro índice
P_dBmax = (wl[idx], P_dB[idx])

plt.figure(101)
plt.plot(wl, P_dB, P_dBmax[0], P_dBmax[1], 'b.')
plt.yscale('log')
plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
plt.tight_layout()
plt.savefig('figure101.png', format='png')

wl_min = 1564.5e-09
wl_max = 1.5670e-06

wl_temp = wl[np.where((wl >= wl_min) & (wl < wl_max))]

f = v/wl_temp  # frequencia correspondente ao comprimento de onda da luz no vácuo

P_dBmax = []

plt.figure(102)

for T in np.arange(27.0, 50, 1):

    P_dBtemp = []

    for i in f:
        beta = 2*np.pi*i/v  # constante de fase dentro do material

        t = np.arange(0, 1/f[-1], (1/f[-1])/1000)

        E1 = np.cos(np.multiply(2*np.pi*i, t) -
                    np.multiply(beta, d_b1))  # onda 1
        E2 = np.cos(np.multiply(2*np.pi*i, t) -
                    np.multiply(beta, (d_b2+delta_b2+(0.05e-06)*(T-27))))

        P_dBtemp.append(20*np.log10(np.max(E1+E2)))

    plt.plot(wl_temp, P_dBtemp)
    idx_temp = np.where(P_dBtemp == np.max(P_dBtemp))[0][0]
    P_dBmax.append((wl_temp[idx_temp], P_dBtemp[idx_temp]))

P_dBmax = np.array(P_dBmax)
plt.plot(P_dBmax[:, 0], P_dBmax[:, 1], 'b.')
plt.yscale('log')
plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
plt.tight_layout()
plt.savefig('figure102.png', format='png')

plt.show()

if len(P_dBmax) >= 2:
    print('Sensibilidade do interferômetro: ', np.round(
        P_dBmax[1][0] - P_dBmax[0][0], 10), ' m ou ', (1e9)*np.round(P_dBmax[1][0] - P_dBmax[0][0], 10), 'um [micrômetro]')
else:
    print('Erro: P_dBmax não possui elementos suficientes para calcular a sensibilidade.')
