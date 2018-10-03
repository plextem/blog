# luogu2680 运输计划

(BZOJ4326)

## 题解

二分+倍增LCA+树上差分

首先二分一个答案，然后考虑如何判断这个答案可否达到。

假设这个答案为 $w$ , 然后对于路径长度大于 $w$ 的边将它的端点到LCA之间的路径差分一下。

假设某条路径构成为 $(u,v,lca)$ ，那么可以分两种情况进行差分：

1.  $v\neq lca, u\neq lca$ ，那么直接 `book[u]++,book[v]++,book[lca]-=2`.
2.  $v = lca$ 或 $u=lca$ ，则直接将深度更深的点 `book[]++`，`book[lca]--`。 

接着将这棵树拓扑排序（可以预处理），然后从下到上更新每条边。

如果某条边满足经过它的路径数等于长度 $w$ 的路径数并且 长度最长的路径减去此边边权后$\leq w$，那么 $w$ 作为答案就是合法的。

## 程序

``` cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <queue>
#define reg register
#define MAX_N 300007

int N, M;
int head[MAX_N], to[MAX_N * 2], nxt[MAX_N * 2], dis[MAX_N * 2], cap;
int fa[MAX_N][20], d[MAX_N][20], dep[MAX_N], deg[MAX_N], vertex[MAX_N], top;
int book[MAX_N], bin[20];

struct edge {
    int u, v, w, lca;
}e[MAX_N];

inline int read () {
    reg int x = 0;
    reg char c = getchar();
    while (c < '0' || '9' < c) c = getchar();
    while ('0' <= c && c <= '9') x = x * 10 + c - '0', c = getchar();
    return x;
}

inline void addEdge (int u, int v, int w) {
    nxt[++cap] = head[u];
    head[u] = cap;
    to[cap] = v;
    dis[cap] = w;
}

void dfs (int x) {
    for (reg int i = 1;i <= 19; ++i) {
        fa[x][i] = fa[fa[x][i - 1]][i - 1];
        d[x][i] = d[x][i - 1] + d[fa[x][i - 1]][i - 1];
    }
    for (reg int i = head[x]; i; i = nxt[i])
        if (to[i] != fa[x][0]) {
            deg[to[i]]++;
            fa[to[i]][0] = x;
            d[to[i]][0] = dis[i];
            dep[to[i]] = dep[x] + 1;
            dfs(to[i]);
        }
}

std::queue<int> q;
inline void topSort () {
    for (reg int i = 1;i <= N; ++i)
        if (!deg[i])
            q.push(i);
    while (!q.empty()) {
        int x = q.front(); q.pop();
        vertex[++top] = x;
        for (reg int i = head[x]; i; i = nxt[i])
            if (to[i] != fa[x][0]) {
                deg[to[i]]--;
                if (deg[to[i]] == 0)
                    q.push(to[i]);
            }
    }
}

inline int getLca (int u, int v) {
    // if (dep[u] < dep[v]) std::swap(u, v);
    for (reg int i = 19;i >= 0; --i) 
        if (dep[v] <= dep[u] - (bin[i]))
            u = fa[u][i];
    if (u == v) return u;
    for (reg int i = 19;i >= 0; --i) {
        if (fa[u][i] == fa[v][i]) continue;
        u = fa[u][i], v = fa[v][i];
    }
    return fa[u][0];
}

inline int query (int x, int y, reg int idx) {
    reg int lca = getLca(x, y);
    e[idx].lca = lca;
    reg int sum = 0;
    for (reg int i = 19;i >= 0; --i)
        if (dep[lca] <= dep[x] - (bin[i]))
            sum += d[x][i], x = fa[x][i];
    if (lca == y) return sum;
    for (reg int i = 19;i >= 0; --i)
        if (dep[lca] <= dep[y] - (bin[i]))
            sum += d[y][i], y = fa[y][i];
    return sum;
}

inline bool check (int L) {
    memset(book, 0, sizeof(book));
    reg int tot = 0, mx = 0;
    for (reg int i = 1;i <= M; ++i) {
        if (e[i].w <= L) continue;
        tot++;
        mx = std::max(mx, e[i].w);
        if (e[i].lca != e[i].v) {
            book[e[i].u]++, book[e[i].v]++;
            book[e[i].lca] -= 2;
        } else {
            book[e[i].lca]--, book[e[i].u]++;
        }
    }
    reg int u;
    for (reg int i = top; i > 1; --i) {
        u = vertex[i];
        if (book[u] == tot && d[u][0] >= mx - L) return true;
        book[fa[u][0]] += book[u];
        book[u] = 0;
    }
    return false;
}

int main () {
    for (int i = 0;i <= 19; ++i)
        bin[i] = (1 << i);
    N = read(), M = read();
    reg int u, v, w;
    for (reg int i = 1;i < N; ++i) {
        u = read(), v = read(), w = read();
        addEdge(u, v, w), addEdge(v, u, w);
    }
    dep[1] = 1;
    dfs(1);
    for (reg int i = 1;i <= M; ++i) {
        e[i] = (edge){read(), read(), 0, 0};
        if (dep[e[i].u] < dep[e[i].v]) std::swap(e[i].u, e[i].v); //dep[u] > dep[v]
        e[i].w = query(e[i].u, e[i].v, i);
    }
    topSort();
    reg int l = 0, r = 3e8, mid, ans = -1;
    while (l <= r) {
        mid = l + r >> 1;
        if (check(mid))
            r = mid - 1, ans = mid;
        else
            l = mid + 1;
    }
    printf("%d\n", ans);
    return 0;
}
```

