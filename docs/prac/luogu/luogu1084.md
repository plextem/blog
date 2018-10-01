# luogu1084 疫情控制

loj上也有(2607)，数据稍微强一点，需要卡一下常（可能是我自带大常数）。

## 题意

$N$个城市组成一棵树，$1$号节点是首都，也是根节点。$M$个军队驻扎在某些城市上，军队可移动，从一个点移动到邻接点花费的时间为边权；也可以原地驻扎，但是不能驻扎在首都。求最少的时间，可以将调度军队使得从每个叶子节点到根节点的路径上都有驻军。

$2≤m≤n≤50,000$

## 题解

个人觉得是个好题。

一开始想偏成了dp。

然后看完题解之后觉得很正确阿结果各种打崩卡在80分不知道什么地方出问题了。

后来把倍增和判断的地方按照[litble大佬的思路](https://blog.csdn.net/litble/article/details/78219618)重构了一下才对。

所有军队可以同时移动，那么影响答案的只有移动时间最长的军队，那我们的目的就是要是最长时间最小，可以考虑**二分**。

二分一个答案后考虑如何判断能不能走到，此时有两种类型的军队：

1.  在规定时间内无法走到根结点，那么我们就记录它走到了最上面最多可以走到哪个点。
2.  在规定时间内可以走到根结点，那么我们就记录它走到根结点后在规定时间内还可以走多少路程，他是有可能可以帮助其他子树的。

此时我们发现我们需要涉及到将节点向上提的过程，那么可以考虑使用倍增优化。

现在我们一遍dfs后，只需要考虑其子树未被封死的根结点的子树，对于根结点的某一棵为被封死子树我们有两种方法封死它：

1.  如果自己子树内有能够到达根结点的军队，那么选择其中上去之后剩余路程最小的肯定最优。
2.  如果没有这种军队的话就只能考虑请求其他子树中军队的帮助。

“将我们已经记录好了的**可以到根节点的军队**按照**剩余路程从大到小**排序。 
将**未被“封死”的子树**按照**到子树到根节点的距离从大到小**排序。 
然后依次处理**未被“封死”的子树**要由哪支军队来管辖。”

然后结束了。

程序感觉有点难打。

## 程序

``` cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstring>
#define MAX_N 300007
#define reg register
typedef long long ll;

int N, M;
int head[MAX_N], to[MAX_N * 2], nxt[MAX_N * 2], cap;
int fa[MAX_N][20], top[MAX_N], topn, topr;
int idx[MAX_N], book[MAX_N];
ll dis[MAX_N * 2], d[MAX_N][20], mn[MAX_N];
bool pass[MAX_N], vis[MAX_N];

struct node {
    ll v;
    int idx;
    bool operator < (const node& rhs) const {
        return v > rhs.v;
    }
}need[MAX_N], rest[MAX_N];

inline ll read () {
    reg ll x = 0;
    reg char c = getchar();
    while (c < '0' || '9' < c) c = getchar();
    while ('0' <= c && c <= '9') x = x * 10 + c - '0', c = getchar();
    return x;
}

inline void addEdge (int u, int v, ll w) {
    nxt[++cap] = head[u];
    head[u] = cap;
    to[cap] = v;
    dis[cap] = w;
}

void dfs (int x, int f, int tp) {
    top[x] = tp;
    fa[x][0] = f;
    for (reg int i = 1;i <= 19; ++i) {
        fa[x][i] = fa[fa[x][i - 1]][i - 1];
        d[x][i] = d[x][i - 1] + d[fa[x][i - 1]][i - 1];
    }
    for (reg int i = head[x]; i; i = nxt[i])
        if (to[i] != f) {
            d[to[i]][0] = dis[i];
            dfs(to[i], x, x == 1 ? to[i] : tp);
        }
}

bool search (int x) {
    if (pass[x]) return true;
    if (!nxt[head[x]]) return false;
    reg bool can = true;
    for (reg int i = head[x]; i; i = nxt[i])
        if (to[i] != fa[x][0])
            can &= search(to[i]);
    return can;
}

inline bool check (ll L) {
    memset(pass, false, sizeof(pass));
    memset(book, 0, sizeof(book));
    memset(vis, false, sizeof(vis));
    topn = topr = 0;
    reg int u;
    reg ll L2;
    reg bool can;
    for (reg int i = 1;i <= M; ++i) {
        if (d[idx[i]][19] < L) {
            rest[++topr] = (node){L - d[idx[i]][19], i};
            if (!book[top[idx[i]]] || (mn[top[idx[i]]] > rest[topr].v))
                mn[top[idx[i]]] = rest[topr].v, book[top[idx[i]]] = i;
        } else {
            u = idx[i], L2 = L;
                for(int j = 19;j >= 0; --j)
                    if (d[u][j] <= L2 && fa[u][j] > 1) {
                        L2 -= d[u][j];
                        u = fa[u][j];
                    }
            pass[u] = true;
        }
    }
    for (reg int i = head[1]; i; i = nxt[i])
        if (!search(to[i])) 
            need[++topn] = (node){dis[i], to[i]};
    std::sort(rest + 1, rest + topr + 1);
    std::sort(need + 1, need + topn + 1);
    reg int j = 1;
    vis[0] = 1;
    for (reg int i = 1;i <= topn; ++i) {
        if (!vis[book[need[i].idx]]) {
            vis[book[need[i].idx]] = true;
            continue;
        }
        while (j <= topr && (vis[rest[j].idx] || rest[j].v < need[i].v)) j++;
        if (j > topr) return false;
        vis[rest[j].idx] = true;
    }
    return true;
}

int main () {
    N = read();
    reg int u, v;
    reg ll w;
    for (reg int i = 1;i < N; ++i) {
        u = read(), v = read(), w = read();
        addEdge(u, v, w), addEdge(v, u, w);
    }
    M = read();
    for (reg int i = 1;i <= M; ++i)
        idx[i] = read();
    dfs(1, 0, 0);
    reg ll l = 0, r = 1e12, mid, ans = -1;
    while (l <= r) {
        mid = l + r >> 1;
        if (check(mid))
            r = mid - 1, ans = mid;
        else
            l = mid + 1;
    }
    printf("%lld\n", ans);
    return 0;
}
```

