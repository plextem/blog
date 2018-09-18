# luogu3953 逛公园

## 题解

与路径统计很像的一道题。

设$f[i][k]$为起点到$i$点，距离与到其的最短路偏差（肯定大于$d[i]$，$d[i]$为$1$到$i$的最短路）为$k$时的路径数。

然后可以拓扑排序后按照$k$从小到大的对每个点进行$dp$:

设有边$(u,v,w)$，转移方程可以写成$f[v][d[u]+w+k-d[v]]+=f[u][k]$

顺序很重要，需要先枚举$k$然后再枚举点和边。

## 程序

``` cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <queue>
#define MAX_N 100007
#define MAX_M 200007
#define MAX_W 57

int N, M, K, P;
int head[MAX_N], nxt[MAX_M], to[MAX_M], dis[MAX_M], cap;
int d[MAX_N];
int deg[MAX_N], vertex[MAX_N], top;
int f[MAX_N][MAX_W];
bool inq[MAX_N];
std::queue<int> q;

inline int read () {
    int x = 0;
    char c = getchar();
    while (c < '0' || '9' < c)
        c = getchar();
    while ('0' <= c && c <= '9')
        x = x * 10 + c - '0', c = getchar();
    return x;
}

void addEdge (int u, int v, int w) {
    nxt[++cap] = head[u];
    head[u] = cap;
    to[cap] = v;
    dis[cap] = w;
}

void init () {
    memset(head, 0, sizeof(head));
    memset(deg, 0, sizeof(deg));
    memset(inq, false, sizeof(inq));
    memset(vertex, 0, sizeof(vertex));
    memset(f, 0, sizeof(f));
    cap = top = 0;
}

void spfa () {
    for (int i = 1;i <= N; ++i)
        d[i] = 2e9;
    d[1] = 0;
    q.push(1), inq[1] = true;
    while (!q.empty()) {
        int x = q.front(); q.pop();
        for (int i = head[x]; i; i = nxt[i]) {
            if (d[to[i]] > d[x] + dis[i]) {
                d[to[i]] = d[x] + dis[i];
                if (!inq[to[i]])
                    q.push(to[i]), inq[to[i]] = true;
            }
        }
        inq[x] = false;
    }
}

inline bool topSort () {
    top = 0;
    for (int i = 1;i <= N; ++i)
        for (int j = head[i]; j; j = nxt[j])
            if (d[i] + dis[j] == d[to[j]])
                deg[to[j]]++;
    for (int i = 1;i <= N; ++i)
        if (!deg[i])
            vertex[++top] = i, q.push(i);
    while (!q.empty()) {
        int x = q.front(); q.pop();
        for (int i = head[x]; i; i = nxt[i]) {
            if (d[to[i]] == d[x] + dis[i]) {
                deg[to[i]]--;
                if (!deg[to[i]]) {
                    vertex[++top] = to[i];
                    q.push(to[i]);
                }
            }
        }
    }
    return top == N;
}

void dp () {
    memset(f, 0, sizeof(f));
    f[1][0] = 1;
    for (int k = 0;k <= K; ++k) {
        for (int i = 1;i <= N; ++i) {
            int x = vertex[i];
            for (int j = head[x]; j; j = nxt[j]) {
                if (d[x] + dis[j] + k - d[to[j]] <= K) {
                    (f[to[j]][d[x] + dis[j] + k - d[to[j]]] += f[x][k]) %= P;
                }
            }
        }
    }
    int res = 0;
    for (int i = 0;i <= K; ++i)
        (res += f[N][i]) %= P;
    printf("%d\n", res % P);
}

void solve () {
    N = read(), M = read(), K = read(), P = read();
    int u, v, w;
    for (int i = 1;i <= M; ++i) {
        u = read(), v = read(), w = read();
        addEdge(u, v, w);
    }
    spfa();
    if (!topSort()) {puts("-1");return;}
    dp();
}

int main () {
    int T = read();
    while (T--) init(), solve();
    return 0;
}

```

