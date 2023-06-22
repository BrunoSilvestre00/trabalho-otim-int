import matplotlib.pyplot as plt
import numpy as np

SIZE = 5

GUROBI_DEFAULT = [
  43757,
  33354,
  58365,
  62237,
  80597,
]

GUROBI_MAX_INFEASIBLE = [
  45060,
  40992,
  43869,
  48429,
  54852,
]

GUROBI_STRONG_BRANCHING = [
  1596,
  1686,
  1605,
  1735,
  1810,
]

# ====================

SCIP_DEFAULT = [
  1473,
  1343,
  1366,
  1283,
  2403,
]

SCIP_MAX_INFEASIBLE = [
  1521,
  2138,
  3163,
  3895,
  6045,
]

SCIP_STRONG_BRANCHING = [
  27,
  27,
  22,
  32,
  31,
]

v1, v2, v3 = (SCIP_DEFAULT, SCIP_MAX_INFEASIBLE, SCIP_STRONG_BRANCHING)

instances = [f'scpnrh{i}' for i in range(1,SIZE+1)]

data = {
    'Scip Default': v1,
    'Scip Max Infeasible': v2,
    'Scip Strong Branching': v3,
}

x = np.arange(SIZE)  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

colors = ['#0af', '#af0', '#f0a']
for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute, color=colors[multiplier], edgecolor='black')
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('# Nós explorados')
ax.set_title('Comparação de métodos de seleção de variáveis - SCIP', fontsize=24)

ax.set_xticks(x + width, instances)
ax.legend(loc='upper left', ncols=3)
ax.set_axisbelow(True)

plt.grid(True)
plt.show()
