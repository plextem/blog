# luogu2831 愤怒的小鸟

## 题解

是一个比较显然的状压dp。

直接设状态$f[S]$表示已经打了的小猪的集合为$S$需要的最小花费。

那么可以枚举抛物线来进行转移。

一条抛物线至少要经过一个点才有可能有价值，一开始我想$O(n^2)$枚举两个点表示通过这两个点的抛物线（如果只通过一个点就直接枚举转移一下就行）然后再$O(n)$枚举这条抛物线通过哪些点，然后进行转移。

但是这样子单次转移是$O(n^3)$，实际上可以通过$O(n^3)$预处理通过某两个点的抛物线可以经过的点的状态然后每次转移就是$O(n^2)$的，这样总复杂度是$O(T\cdot 2^n\cdot n^2)$，可以通过此题。

## 程序

``` cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstring>
#define eps 1e-6
#define MAX_N 20
#define MAX_M 300007

int N, M;
long double x[MAX_N], y[MAX_N];
int g[MAX_N][MAX_N];
int f[MAX_M];

inline int read () {
    int x = 0;
    char c = getchar();
    while (c < '0' || '9' < c)
        c = getchar();
    while ('0' <= c && c <= '9')
        x = x * 10 + c - '0', c = getchar();
    return x;
}

inline void calc (double& a, double& b, double x1, double y1, double x2, double y2) {
    a = (y1 * x2 - y2 * x1) / (x1 * x2 * (x1 - x2));
    b = (y1 - a * x1 * x1) / x1;
}

inline int eq (double a, double b) {return fabs(a - b) < eps;}

int main () {
    int T = read();
    while (T--) {
        N = read(), M = read();
        for (int i = 1;i <= N; ++i)
            scanf("%llf%llf", x + i, y + i);
        memset(g, 0, sizeof(g));
        double a, b;
        for (int i = 1;i <= N; ++i) {
            g[i][i] = 1 << i - 1;
            for (int j = i + 1, vis = 0; j <= N; ++j) {
                if ((vis >> (j - 1)) & 1) continue;
                else {
                    if (eq(x[i], x[j])) continue;
                    calc(a, b, x[i], y[i], x[j], y[j]);
                    if (a >= 0) continue;
                    for (int k = 1;k <= N; ++k) {
                        if (eq(a * x[k] * x[k] + b * x[k], y[k]))
                            vis |= (1 << k - 1), g[i][j] |= (1 << k - 1);
                    }
                }
            }
        }
        int tot = (1 << N) - 1;
        for (int i = 1;i <= tot; ++i)
            f[i] = 1e9;
        f[0] = 0;
        for (int i = 0;i < tot; ++i) {
            for (int j = 1;j <= N; ++j) {
                for (int k = j;k <= N; ++k) {
                    f[i | g[j][k]] = std::min(f[i | g[j][k]], f[i] + 1);
                }
            }
        }
        printf("%d\n", f[tot]);
    }
    return 0;
}

```



