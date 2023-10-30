"""Implementação de um Grafo na qual é verificado
   se o mesmo é Euleriano, seguindo algumas condições"""

from collections import defaultdict
import heapq

class Grafo:
    def __init__(self, filename):
        self.vertices = 0
        self.grafo = []
        self.matrizAdj = []
        self.listaAdj = defaultdict(list)
        self.listaAdjPesos = defaultdict(list)
        self.verticesImpares = []
        self.graus = []
        self.file_name = filename
                        
    def preenche_matrizAdj(self):
        #print(self.file_name)

        #Abrindo o arquivo para ler os dados
        with open(self.file_name) as file_object:
            # Le a primeira linha do arquivo que contem a quantidade de vertices
            tipoArquivo = file_object.readline().strip()
            self.vertices = int(file_object.readline()) 

            if (tipoArquivo == 'Arestas'):
                matrizAux = [[0 for i in range(self.vertices)] for j in range(self.vertices)]
                for row in file_object:
                    valores = [int(x) for x in row.split()] 
                    x, y = valores[:2]
                    matrizAux[x-1][y-1] = 1
                    matrizAux[y-1][x-1] = 1
                for i in range(self.vertices):
                    self.matrizAdj.append( matrizAux[i] )
                
                
            elif (tipoArquivo == 'Matriz'):
                for row in file_object:

                    valores = [int(x) for x in row.split()] 
                    self.matrizAdj.append( valores )

            elif (tipoArquivo == 'MatrizTS'):
                matrizAux = [[0 for i in range(self.vertices)] for j in range(self.vertices)]
                j = 1
                for row in file_object:
                    valores = [int(x) for x in row.split()] 
                    for i in range(j, self.vertices):
                        matrizAux[i][j-1] = valores[i-j]
                        matrizAux[j-1][i] = valores[i-j]

                    j += 1

                for row in matrizAux:                    
                    self.matrizAdj.append( row )
        #print(self.matrizAdj)

    def preenche_arestas_grafo(self):
        for i in range(self.vertices ):
            for j in range(i, self.vertices): # simetrico logo vou de i ate j
                if (i != j and self.matrizAdj[i][j] > 0):
                    self.grafo.append( (i+1, j+1, self.matrizAdj[i][j]))
    
    
    def insere_aresta_peso(self, u, v, w):
        self.listaAdjPesos[u].append( (v, w))
        self.listaAdjPesos[v].append( (u, w))

    def insere_aresta(self, u, v):
        self.listaAdj[u].append( v )
        self.listaAdj[v].append( u )

    # Insere os vértices adjacentes
    def preenche_listAdj(self):
        for aresta in self.grafo:
            #(aresta)
            self.insere_aresta(aresta[0], aresta[1])
            self.insere_aresta_peso(aresta[0], aresta[1], aresta[2])


    def remove_aresta(self, u, v):
        for index, chave in enumerate(self.listaAdj[u]):
            if chave == v:
                self.listaAdj[u].pop(index)
        for index, chave in enumerate(self.listaAdj[v]):
            if chave == u:
                self.listaAdj[v].pop(index)

    # Função que cria um par contendo vértice e grau
    def verifica_graus(self):
        for i in range(self.vertices):
            grau = 0
            for j in range(self.vertices):
                if (i != j and self.matrizAdj[i][j] > 0):
                    grau += 1
            self.graus.append( [i+1, grau] )
        return self.graus

    # Função que verifica se o grafo é euleriano
    # Todos os vértices devem possuir grau par 
    # O grafo deve ser conexo 
    def e_euleriano(self):
        eEuleriano = True
        for vertice in self.graus:
          if (vertice[1] % 2 == 1):
            eEuleriano = False
            break
        
        return eEuleriano
    
    # Função que separa os vértices que possuem grau ímpar
    def vertices_grau_impar(self):
        self.verticesImpares = [grau for grau in self.graus if grau[1] % 2 == 1]
        return self.verticesImpares

    # Função de Busca em Profundidade para contar 
    # os vértices alcançáveis a partir de v
    def DFS_adj(self, v, visitado): 
        cont = 1
        visitado[v] = True
        for i in self.listaAdj[v]:
            if visitado[i] == False:
                cont += self.DFS_adj(i, visitado)
        return cont 

    def prox_aresta_e_valida(self, u, v):
        # A aresta u-v é valida em um dos seguintes casos

        # Se v é o único vértice adjacente de u
  
        if len(self.listaAdj[u]) == 1:
            return True
        else:
            visitado = [False] * (self.vertices + 1)
            cont1 = self.DFS_adj(u-1, visitado)

            # Se existem arestas multiplas adjacentes, 
            # logo u-v não é ponte

            # Remove aresta (u, v) e depois da remoção
            # conta os vértices alcançáveis a partir de u
            self.remove_aresta(u, v)
            visitado = [False] * (self.vertices + 1)
            cont2 = self.DFS_adj(u-1, visitado)

            self.insere_aresta(u, v) #Insere a aresta de volta para o grafo

            # Se o cont1 for maior, logo a aresta (u, v) é uma ponte
            return False if cont1 > cont2 else True 

    # Mostra o Circuito Euleriano a partir do vértice u
    def mostra_circuito_aux(self, u):
        for v in self.listaAdj[u]: #Percorre por todos os vértices adjacentes a esse vértice
            if self.prox_aresta_e_valida(u, v): #Se a aresta u-v não foi removida e é uma aresta seguinte válida
                print(f'{u}-{v}', end=" "),   
                self.remove_aresta(u, v)
                self.mostra_circuito_aux(v)

    # A função principal que imprime o Circuito Euleriano. 
    # O primeiro vértice é definido como 1 e logo após a
    # funcão mostra_circuito_aux é chamada
    def mostra_circuito_principal(self):
        u = 1 
        self.mostra_circuito_aux(u)

    #Função com algoritmo de Dijkstra para calcular custo mínimo
    def dijkstra(self, orig, dest):

        # vetor de distâncias
        dist = [float('inf')] * (self.vertices + 1)

        # vetor de visitados
        visitados = [False] * (self.vertices + 1)
        pq = []
        
        # a distância de origem para origem é 0
        dist[orig] = 0

        # insere na fila
        heapq.heappush(pq, (dist[orig], orig)) # remove da fila
        
        # loop do algoritmo
        while pq:
            # extrai o par do topo
            # utiliza o vértice u
            # e remove da fila
            d, u = heapq.heappop(pq) 
            
            # verifica se o vértice não foi expandido
            if visitados[u]:
                continue
            
            # marca como visitado
            visitados[u] = True
            
            # obtém o vértice adjacente e o custo da aresta
            for v, custo in self.listaAdjPesos[u]:
                # relaxamento (u, v)
                if dist[v] > dist[u] + custo:
                    # atualiza a distância de v e insere na fila de prioridade
                    dist[v] = dist[u] + custo
                    heapq.heappush(pq, (dist[v], v))

        # retorna a distância mínima até o destino
        return dist[dest]
    
    # Exibe matriz de adjacência
    def mostra_matrizAdj(self):
        for i in range(self.vertices): 
            for j in range(self.vertices): 
                print(self.matrizAdj[i][j], end=" ")
            print()
    
    def mostra_grafo(self):
        return self.grafo

    def mostra_listaAdj(self):
        return self.listaAdj
    
    def qtd_vertices(self):
        return self.vertices

    def tam_grafo(self):
        return len(self.grafo)
    
    # Função que executa todas as outras
    # funções necessárias
    def solucao(self):
        
        #chamada de funções para a inserção das arestas e pesos
        g.preenche_matrizAdj() 
        g.preenche_arestas_grafo()
        g.preenche_listAdj()
        g.verifica_graus() #verifica os graus de todos os vértices

        if self.e_euleriano():
            print("Grafo possui um circuito euleriano")
            g.mostra_circuito_principal()
        else:
            print("Grafo não possui um circuito euleriano")
            print(g.vertices_grau_impar())
            
            # apenas para grafos completos
            # se grafo possui k vértices e k é positivo, logo todos 
            # os vértices possuem grau ímpar

            #se k é negativo, acontece o contrário
            
            if (self.file_name != "Arestas" and (self.vertices - 1) % 2 == 1):
                origem = 1 # vértice origem
                destino = 3 # vértice destino
                print(f'Custo mínimo entre aresta {origem} e {destino}:')
                print(g.dijkstra(origem, destino))

g = Grafo("4V.txt") # nome do arquivo a ser lido
g.solucao() # chamada de função para rodar o programa

