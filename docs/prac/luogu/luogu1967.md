# luogu1967 货车运输

## 题解

这题应该纯粹是用来长信心或者练板子的大水题。

还是稍微说一下。

首先可以想到贪心的方法，就是选取两个点的所有路径中道路权值最小值最大的去做。

然后就可以想到 ~~二分~~ 最大生成树，转化成树后这个问题就好维护多了。

于是我们可以将询问转化为两个点之间的唯一路径上的最小道路权值。

因为我们的任务是 ~~长信心~~ 刷题，而不是练板子，所以考虑哪种方法比较容易。

于是我用了 ~~LCT~~ ~~数链剖分~~ 倍增。

## 程序

``` cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstring>
#define MAX_N 10007
#define MAX_M 50007
typedef long long ll;

int N, M;
int fa[MAX_N];
int head[MAX_N], to[MAX_N * 2], nxt[MAX_N * 2], cap;
int f[MAX_N][18], dep[MAX_N];
ll mn[MAX_N][18], dis[MAX_N * 2];
bool vis[MAX_N];

struct edge {
    int u, v;
    ll w;

    bool operator < (const edge& rhs) const {
        return w > rhs.w;
    }
}e[MAX_M];

inline ll read () {
    ll x = 0;
    char c = getchar();
    while (c < '0' || '9' < c ) c = getchar();
    while ('0' <= c && c <= '9') x = x * 10 + c - '0', c = getchar();
    return x;
}

inline void addEdge (int u, int v, ll w) {
    nxt[++cap] = head[u];
    head[u] = cap;
    to[cap] = v;
    dis[cap] = w;
}

int find (int x) {return x == fa[x] ? x : fa[x] = find(fa[x]);}

void dfs (int x) {
    vis[x] = true;
    for (int i = 1;i <= 17; ++i) {
        f[x][i] = f[f[x][i - 1]][i - 1];
        mn[x][i] = std::min(mn[x][i - 1], mn[f[x][i - 1]][i - 1]);
    }
    for (int i = head[x]; i; i = nxt[i])
        if (to[i] != f[x][0]) {
            f[to[i]][0] = x;
            mn[to[i]][0] = dis[i];
            dep[to[i]] = dep[x] + 1;
            dfs(to[i]);
        }
}

inline int getLca (int u, int v) {
    if (dep[u] < dep[v]) std::swap(u, v); //dep[u] >= dep[v];
    for (int i = 17;i >= 0; --i)
        if (dep[v] <= dep[u] - (1 << i))
            u = f[u][i];
    if (u == v) return u;
    for (int i = 17;i >= 0; --i) {
        if (f[u][i] == f[v][i]) continue;
        u = f[u][i], v = f[v][i];
    }
    return f[u][0];
}

inline ll query (int x, int y) {
    ll ans = 1e15;
    for (int i = 17;i >= 0; --i)
        if (dep[f[x][i]] >= dep[y]) {
            ans = std::min(ans, mn[x][i]);
            x = f[x][i];
        }
    return ans;
}

int main () {
    N = read(), M = read();
    for (int i = 1;i <= M; ++i)
        e[i] = (edge){read(), read(), read()};
    std::sort(e + 1, e + M + 1);
    for (int i = 1;i <= N; ++i)
        fa[i] = i;
    int p, q;
    for (int i = 1;i <= M; ++i) {
        p = find(e[i].u), q = find(e[i].v);
        if (p != q) {
            fa[p] = q;
            addEdge(e[i].u, e[i].v, e[i].w);
            addEdge(e[i].v, e[i].u, e[i].w);
        }
    }
    for (int i = 1;i <= N; ++i)
        if (!vis[i])
            dep[i] = 1, dfs(i);
    int Q = read(), lca;
    while (Q--) {
        p = read(), q = read();
        if (find(p) != find(q)) {
            puts("-1");
        } else {
            lca = getLca(p, q);
            printf("%lld\n", std::min(query(p, lca), query(q, lca)));
        }
    }
    return 0;
}

```

