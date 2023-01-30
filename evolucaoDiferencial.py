from scipy.optimize import NonlinearConstraint, differential_evolution
import numpy as np
import math as math

numero_geradores = 13

potencia_demandada = 2520

potencia_minima = [0, 0, 0, 60, 60, 60, 60, 60, 60, 40, 40, 55, 55]

potencia_maxima = [680, 360, 360, 200, 200, 200, 200, 200, 200, 120, 120, 120, 120]

custo_a = [
    0.00028,
    0.00056,
    0.00056,
    0.00324,
    0.00324,
    0.00324,
    0.00324,
    0.00324,
    0.00324,
    0.00284,
    0.00284,
    0.00284,
    0.00284,
]

custo_b = [8.10, 8.10, 8.10, 7.74, 7.74, 7.74, 7.74, 7.74, 7.74, 8.60, 8.60, 8.60, 8.60]

custo_c = [550, 309, 307, 240, 240, 240, 240, 240, 240, 126, 126, 126, 126]

custo_d = [300, 200, 150, 150, 150, 150, 150, 150, 150, 100, 100, 100, 100]

custo_e = [
    0.035,
    0.042,
    0.042,
    0.063,
    0.063,
    0.063,
    0.063,
    0.063,
    0.063,
    0.084,
    0.084,
    0.084,
    0.084,
]

bound = [
    (potencia_minima[0], potencia_maxima[0]),
    (potencia_minima[1], potencia_maxima[1]),
    (potencia_minima[2], potencia_maxima[2]),
    (potencia_minima[3], potencia_maxima[3]),
    (potencia_minima[4], potencia_maxima[4]),
    (potencia_minima[5], potencia_maxima[5]),
    (potencia_minima[6], potencia_maxima[6]),
    (potencia_minima[7], potencia_maxima[7]),
    (potencia_minima[8], potencia_maxima[8]),
    (potencia_minima[9], potencia_maxima[9]),
    (potencia_minima[10], potencia_maxima[10]),
    (potencia_minima[11], potencia_maxima[11]),
    (potencia_minima[12], potencia_maxima[12]),
]


def func(k):
    soma = 0
    for x in range(len(k)):
        soma += (
            custo_a[x] * k[x]
            + custo_b[x] * k[x]
            + custo_c[x]
            + abs(custo_d[x] * math.sin(custo_e[x] * (potencia_minima[x] - k[x])))
        )
    return soma


def potencia(k):
    soma = 0
    for x in range(len(k)):
        soma += k[x]
    return soma


limitacao = NonlinearConstraint(potencia, potencia_demandada, np.inf)
i = 0
j = 0
m = 0
k = 0
for i in range(5):
    m = m + 0.2
    y = 0
    for k in range(5):
        y = y + 0.2
        p = 0
        for j in range(5):
            p = p + 10
            print("mutação: ", +y)
            print("recombinação: ", +m)
            print("população: ", +p)
            result = differential_evolution(
                func,
                bound,
                args=(),
                strategy="best1bin",
                maxiter=1000,
                popsize=p,
                tol=0.01,
                mutation=(y, 1),
                recombination=m,
                seed=None,
                polish=False,
                init="latinhypercube",
                atol=0,
                updating="immediate",
                workers=1,
                constraints=(limitacao),
                x0=None,
                integrality=None,
                vectorized=False,
            )
            somatorio_potencia = 0
            for x in result.x:
                somatorio_potencia += x
                # print(f"{x:.5f}")
            print("POTENCIA ALCANÇADA: " + str(somatorio_potencia))
            print("CUSTO: " + str(func(result.x)))
            print("CUSTO/POTENCIA: " + str(func(result.x) / somatorio_potencia))
            print()
