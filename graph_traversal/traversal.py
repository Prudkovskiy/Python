import queue
from sys import stdin

adj = dict() #список смежности
vertexes = set() #список посещенных вершин

def RunGraph(v, q): #функция обхода в ширину
   if not adj.get(v):
       print(v)
       return

   for i in adj[v]:
       q.put(i);  # добавляем соседей в очередь
   vertexes.add(v)
   print(v)
   while(not q.empty()): #пока в очереди есть хотя бы одна вершина
         w = q.get() #извлекаем вершину из очереди
         if w in vertexes: #если вершина уже была посещена, то пропускаем ее
             continue
         if adj.get(w):
            for i in adj[w]:
                q.put(i);  # добавляем соседей текущей вершины в очередь
         print(w)
         vertexes.add(w) #добавляем вершину в список посещенных

s = stdin.readline()
command = s.split()
graph_type = command[0] # тип графа, ориентированный ('d') или неориентированный ('u')
start_vertex = command[1] # стартовая вершина
search_type = command[2] # тип обхода, в ширину ('b') или в глубину ('d')

s = stdin.readline()
while (s):
    command = s.split()
    if len(command) != 2:
        s = stdin.readline()
        continue
    if not command[0] in adj:
        adj[command[0]] = [command[1]]
    else:
        adj[command[0]].append(command[1])
    if graph_type == 'u':
        if not command[1] in adj:
            adj[command[1]] = [command[0]]
        else:
            adj[command[1]].append(command[0])

    s = stdin.readline()

if search_type == 'b':
    for i in adj:
        adj[i].sort()
    RunGraph(start_vertex, queue.Queue())
if search_type == 'd':
    for i in adj:
        adj[i].sort(reverse = True)
    RunGraph(start_vertex, queue.LifoQueue())