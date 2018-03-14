def main():
    n = int(input('Введите размер графа: '))

    capacities = []

    print('Введите пропускные способности ребер:')

    for i in range(n):
        capacities.append(list(map(int, input().split())))

    mfs = MaxFlowSearcher(0, n - 1, capacities)

    print("Поток по данному графу:")

    for a in mfs.perform():
        print(a)

class MaxFlowSearcher:
    def __init__(self, start, finish, capacities):
        self.__n = len(capacities)
        self.__c = capacities
        self.__f = [[0 for i in range(self.__n)] for i in range(self.__n)]
        self.__q = [[0 for i in range(self.__n)] for i in range(self.__n)]

        # Исток и устье
        self.__s = start
        self.__t = finish

    def perform(self):
        flow = 0

        while True:
            if not self.__bfs():
                break

            # Индексы предыдущих вершин
            self.__ptr = [0 for i in range(self.__n)]

            while True:
                pushed = self.__dfs(self.__s, float('inf'))

                if pushed == 0:
                    break
                else:
                    flow += pushed

        return self.__f

    def __bfs(self):
        qh = 0
        qt = 0
        
        self.__q[qt] = self.__s
        qt += 1

        # Список дистанций устанавливаем на -1
        self.__d = [-1 for i in range(self.__n)]
        self.__d[self.__s] = 0

        while qh < qt:
            fr = self.__q[qh]
            qh += 1

            for to in range(self.__n):
                if self.__d[to] == -1 and self.__f[fr][to] < self.__c[fr][to]:
                    self.__q[qt] = to
                    qt += 1

		            # Увеличиваем уровень вершины
                    self.__d[to] = self.__d[fr] + 1;

        return self.__d[self.__t] != -1

    def __dfs(self, fr, flow):
        # Пропускная способность больше не позволяет добавить
        if flow == 0:
            return 0

        # Пришли на финиш
        if fr == self.__t:
            return flow

        for to in range(self.__ptr[fr], self.__n):
            if self.__d[to] != self.__d[fr] + 1:
                continue

            # Добавляем к потоку сколько можем
            pushed = self.__dfs(
                to,
                min(flow, self.__c[fr][to] - self.__f[fr][to])
            )
            
            if pushed != 0:
                self.__f[fr][to] += pushed
                self.__f[to][fr] -= pushed
                return pushed;
            
        return 0

main()