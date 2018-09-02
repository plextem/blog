# -*- coding:utf-8 -*-
pre = '      - '
mid = ': articles/NetWork24/'
su = '.md'
text = ''
ans=''

for i in range (5, 25):
    text = raw_input()
    ans += (pre+str(i)+'.'+text+mid+str(i)+su+'\n')
print(ans)
