import gurobipy as gp

INPUTS_PER_ROW = 15
TIME_LIMIT = float(5*60)

GUROBI_STATUS_DICT = {
  2: 'OPTIMAL',
  3: 'INF_OR_UNBD',
  4: 'INFEASIBLE',
  5: 'UNBOUNDED',
  6: 'CUTOFF',
  7: 'ITERATION_LIMIT',
  8: 'NODE_LIMIT',
  9: 'TIME_LIMIT',
  10: 'SOLUTION_LIMIT',
  11: 'INTERRUPTED',
  12: 'NUMERIC',
  13: 'SUBOPTIMAL',
  14: 'LOADED',
  15: 'INPROGRESS',
  16: 'USER_OBJ_LIMIT'
}

GUROBI_PARAM_DICT = {
  'VarBranch': {
    'MAX_INFEASIBILITY': 2,
    'STRONG_BRANCHING': 3,
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
  model = gp.Model('Problema de Cobertura - Trabalho Etapa 2')

  # variáveis de decisão
  X = model.addVars(N, vtype=gp.GRB.BINARY, name='x')

  # função objetivo
  obj_expr = gp.quicksum(X[i]*C[i] for i in range(N))
  model.setObjective(expr=obj_expr, sense=gp.GRB.MINIMIZE)

  # restrições
  for j in range(M):
    constr = (gp.quicksum(X[i] for i in range(M) if A[j][i]) >= 1)
    model.addConstr(constr)
  
  return X, model

def main():
  M, N, C, A = read_data()
  X, model = build_model(M, N, C, A)

  params = {
    gp.GRB.Param.TimeLimit: TIME_LIMIT, # Definir limite de tempo
    gp.GRB.Param.Cuts: 0, # Desativar cortes
    # gp.GRB.Param.Presolve: 0, # Desativar pre processamento
    # gp.GRB.Param.VarBranch: GUROBI_PARAM_DICT['VarBranch']['STRONG_BRANCHING'], # Seleção de variavel
  }

  for k in params:
    model.setParam(k, params[k])
  
  # principais cortes para o problema de cobertura
  cuts = [
    gp.GRB.Param.CoverCuts,
    gp.GRB.Param.CliqueCuts,
    gp.GRB.Param.GUBCoverCuts,
    gp.GRB.Param.FlowCoverCuts,
  ]
  
  for k in cuts:
    model.setParam(k, 2)


  model.optimize()
  

  nodes = [f'{i+1}' for i in range(M) if bool(X[i].X)]

  print('-'*80)
  print(f'Status: {GUROBI_STATUS_DICT[model.status]}')
  print(f'Numero de nós selecionados: {len(nodes)}')
  print(f'Nós selecionados: {", ".join(nodes)}')
  print(f'Valor da função objetivo: {model.objVal}')
  print('-'*80)

if __name__ == '__main__':
  main()
