# agc028 B Removing Blocks

## 题面

给出一个序列，每个点都有一个权值，一开始他们都是连通的。

Snuke将执行以下操作N次：

+   选择一个点并将其移除，移除这个点所用的代价为此时他所在的块内所有点的权值和（包括自己），将这个点移除之后原本所在的块会因为其被删除而被分成两个块。

对于所有可能的 $N!$ 个选择方案，算出他们的代价总和。

比如：

Input

2

1 2

Output

9

## 题解

我在比赛的时候没有写出来这一题，第二天看题解，感觉还是非常神奇的。

我们忽略选择顺序，来算一个选择方案中的所有代价的总和的**期望**。

考虑单点对整体算贡献的方法，我们考虑一个点，其会被包括（也就是有贡献）的期望概率。

假设删除某个点 $i$ 时,点 $j$ 和它在同一个块中的概率为 $P(i,j)$ ，那么如果要满足此时两点在同一个块，就需要选择 $i$ 时：$i,i+1,\cdots ,j$ 都没有被选择过。

那么概率其实就是 $1/(|j-i|+1)$,就是$i$~$j$中只选则到$i$的概率。

我们设$b[j]=\sum_{i=1}^{N} P(i,j)$：

然后一个点 $i$ 的期望贡献就是 $a[i]*b[i]$

最后将所有点的期望值相加 $\times N!$ 就是答案。

可以通过预处理 $1/1,1/2,1/3,\cdots ,1/N$ 的前缀和（模$10^9+7$意义下）做到时间复杂度$O(N)$。

## 代码

``` cpp
#include <bits/stdc++.h>
#define MAX_N 100007
#define MOD 1000000007
using namespace std;
typedef long long ll;

int N;
ll a[MAX_N], b[MAX_N];
ll inv[MAX_N], sum[MAX_N], res;

inline void init () {
    inv[0] = inv[1] = 1;
    for (int i = 2;i <= N; ++i)
        inv[i] = inv[MOD % i] * (MOD - MOD / i) % MOD;
    for (int i = 1;i <= N; ++i)
        sum[i] = sum[i - 1] + inv[i];
}

int main () {
    scanf("%d", &N);
    for (int i = 1;i <= N; ++i)
        scanf("%d", a + i);
    init();
    for (int i = 1;i <= N; ++i)
        b[i] = (sum[N - i + 1] - 1 + sum[i] + MOD) % MOD;
    for (int i = 1;i <= N; ++i)
        (res += a[i] * b[i]) %= MOD;
    for (int i = 2;i <= N; ++i)
        res = res * i % MOD;
    printf("%lld\n", res % MOD);
    return 0;
}

```

