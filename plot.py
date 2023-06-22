from matplotlib import pyplot as plt
import numpy as np

SIZE = 5
COLORS_GAP = ['#00AAFF', '#ff2a00']
COLORS_NODE = ['#00ffd5', '#FFAA00']

nodes_gurobi = [
  43757,
  33354,
  58365,
  62237,
  80597,
]

nodes_scip = [
  1386,
  1321,
  1336,
  1270,
  2304,
]

nodes_gurobi_nopresolver = [
  28970,
  29165,
  29347,
  29345,
  29628,
]

nodes_scip_nopresolver = [
  1473,
  1343,
  1366,
  1283,
  2403,
]


def double_bar_plot(l1, l2, title, y_label, colors):
    x = np.arange(SIZE)

    WIDTH = 0.35

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - WIDTH/2, l1, WIDTH, label='Pré-processamento ativado', color=colors[1], edgecolor='black')
    rects2 = ax.bar(x + WIDTH/2, l2, WIDTH, label='Pré-processamento desativado', color=colors[0], edgecolor='black')

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)


    ax.set_ylabel(y_label, fontsize=20)
    ax.set_xlabel('Instâncias', fontsize=20)

    ax.set_xticks(x)
    ax.set_xticklabels([f'scpnrh{i}' for i in range(1, SIZE+1)], fontsize=16)

    ax.set_title(title, fontsize=24)
    ax.legend()
    ax.set_axisbelow(True)

    plt.grid(True)
    plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.08)
    plt.show()


if __name__ == '__main__':
    # nodes_title_gurobi = 'Comparação do número de nós GUROBI'
    # nodes_title_scip = 'Comparação do número de nós SCIP'
    # double_bar_plot(nodes_gurobi, nodes_gurobi_nopresolver, nodes_title_gurobi, '# Nós', COLORS_GAP)
    # double_bar_plot(nodes_scip_nopresolver, nodes_scip, nodes_title_scip, '# Nós', COLORS_NODE)


    for i, j in zip(nodes_gurobi, nodes_gurobi_nopresolver):
        print(f'{(i/j-1)*100:.2f}')

    print('\n\n\n')
    
    for i, j in zip(nodes_scip_nopresolver, nodes_scip):
        print(f'{(i/j-1)*100:.2f}')
