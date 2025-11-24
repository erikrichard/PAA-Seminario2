import itertools

def solve_tsp_held_karp(dists):
    """
    Resolve o TSP usando o algoritmo Held-Karp.
    
    Args:
        dists: Matriz de adjacência NxN onde dists[i][j] é a distância de i para j.
               
    Returns:
        (custo_minimo, caminho)
    """
    n = len(dists)
    
    # Dicionário para Programação Dinâmica
    # Chave: (mask, last_city)
    # Valor: (custo_acumulado, cidade_anterior) -> Guardamos o anterior para reconstruir o caminho
    C = {}

    # --- PASSO 1: Inicialização (Conjuntos de tamanho 2) ---
    # Calculamos o custo de ir da cidade 0 para cada cidade k.
    # A máscara (1 << k) | 1 significa: o bit k está ligado E o bit 0 está ligado.
    for k in range(1, n):
        C[(1 << k) | 1, k] = (dists[0][k], 0)

    # --- PASSO 2: Iterar sobre tamanhos de subconjuntos crescentes ---
    # Começamos procurando caminhos que passam por 2 cidades intermediárias, depois 3, etc.
    for subset_size in range(2, n):
        # itertools.combinations gera todos os subconjuntos de cidades (excluindo a 0)
        for subset in itertools.combinations(range(1, n), subset_size):
            # Criar a bitmask para esse subconjunto
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            
            # Adicionar a cidade inicial (0) à máscara
            bits |= 1 

            # Para cada cidade 'k' neste subconjunto, qual é o menor custo para terminar nela?
            for k in subset:
                prev_mask = bits & ~(1 << k) # Remove k da máscara atual
                
                res = []
                # 'm' é a cidade visitada imediatamente antes de 'k'
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    
                    # Custo = Custo para chegar em m (com máscara anterior) + dist(m, k)
                    res.append((C[(prev_mask, m)][0] + dists[m][k], m))
                
                # Armazena o mínimo e quem foi o pai (m) para reconstrução
                C[(bits, k)] = min(res)

    # --- PASSO 3: Fechar o ciclo (Voltar para 0) ---
    # Agora temos o custo de visitar TODAS as cidades terminando em qualquer k.
    # Precisamos adicionar o custo de voltar de k para 0.
    all_bits = (1 << n) - 1
    res = []
    for k in range(1, n):
        res.append((C[(all_bits, k)][0] + dists[k][0], k))
    
    opt_cost, parent = min(res)

    # --- PASSO 4: Reconstruir o caminho (Backtracking) ---
    path = []
    # Começamos do fim para o começo, mas sabemos que o fim volta para 0
    curr_bit = all_bits
    curr_node = parent # O último nó antes de voltar para 0
    
    # O ciclo termina em 0
    path.append(0)
    
    # Reconstrói de trás para frente
    for i in range(n - 1):
        path.append(curr_node)
        new_bit = curr_bit & ~(1 << curr_node)
        _, curr_node = C[(curr_bit, curr_node)]
        curr_bit = new_bit

    # Adiciona o ponto de partida
    path.append(0)
    
    # Inverte para mostrar na ordem correta (0 -> ... -> 0)
    path.reverse()

    return opt_cost, path

# --- Exemplo de Uso ---

if __name__ == "__main__":

    # 0: A, 1: B, 2: C, 3: D
    distancias = [
        [0, 10, 15, 20], # Distâncias de A
        [10, 0, 35, 25], # Distâncias de B
        [15, 35, 0, 30], # Distâncias de C
        [20, 25, 30, 0]  # Distâncias de D
    ]

    custo, caminho = solve_tsp_held_karp(distancias)

    print(f"Matriz de Custo:\n{distancias}")
    print("-" * 30)
    print(f"Custo Mínimo: {custo}")
    print(f"Melhor Caminho (índices): {caminho}")
    
    # Mapeando para letras para facilitar leitura
    cidades = ['A', 'B', 'C', 'D']
    caminho_nomes = [cidades[i] for i in caminho]
    print(f"Melhor Caminho (nomes): {' -> '.join(caminho_nomes)}")