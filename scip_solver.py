import pyscipopt as scip

INPUTS_PER_ROW = 15
TIME_LIMIT = float(5*60)

SCIP_PARAM_DICT = {
  'VarBranch': {
    'MAX_INFEASIBILITY': 'mostinf',
    'STRONG_BRANCHING': 'fullstrong',
  },
}

def number_of_inputs(x):
  from math import ceil
  return ceil(x/INPUTS_PER_ROW)

def read_integers():
  return list(map(int, input().split()))

def read_data():
  m, n = read_integers()
  c = [x for _ in range(number_of_inputs(n)) for x in read_integers()]
  a = [[0]*n for _ in range(m)]
  for i in range(m):
    qtd_cover_columns = int(input())
    cover_columns = [x for _ in range(number_of_inputs(qtd_cover_columns)) for x in read_integers()]
    for index in cover_columns:
      a[i][index-1] = 1
  return m, n, c, a

def build_model(M, N, C, A):
  model = scip.Model('Problema de Cobertura - Trabalho Etapa 2')

  # variáveis de decisão
  X = [model.addVar(vtype="B", name=f"x{i}") for i in range(N)]

  # função objetivo
  obj_expr = (scip.quicksum(X[i]*C[i] for i in range(N)))
  model.setObjective(obj_expr, sense='minimize')

  # restrições
  for j in range(M):
    constr = (scip.quicksum(X[i] for i in range(M) if A[j][i]) >= 1)
    model.addCons(constr)
  
  return X, model

def main():
  M, N, C, A = read_data()
  X, model = build_model(M, N, C, A)

  params = {
    "limits/time": TIME_LIMIT, # Definir limite de tempo
    "separating/maxrounds": 0, # Desativar cortes
    # f"branching/{SCIP_PARAM_DICT['VarBranch']['MAX_INFEASIBILITY']}/priority": 10001 # Seleção de variavel
  }

  for k in params:
    model.setParam(k, params[k])

  cuts = {
    'separating/clique/priority': 5000,
    'separating/flowcover/priority': 5000,
    'separating/knapsackcover/priority': 5000,
    'constraints/cumulative/usecovercuts': True,
    'constraints/knapsack/usegubs': True,
  }

  for k in cuts:
    model.setParam(k, cuts[k])

  model.setPresolve(False)
  model.optimize()

  nodes = [f'{i+1}' for i in range(M) if bool(model.getVal(X[i]))]

  print('-'*80)
  print(f'Status: {model.getStatus()}')
  print(f'Numero de nós selecionados: {len(nodes)}')
  print(f'Nós selecionados: {", ".join(nodes)}')
  print(f'Limitante Primal: {model.getPrimalbound()}')
  print(f'Limitante Dual: {model.getDualbound()}')
  print(f'GAP: {model.getGap():.3f}%')
  print('-'*80)


if __name__ == '__main__':
  main()