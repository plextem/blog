# -*- coding:utf-8 -*-
x = int(input("请输入空格数:"))
pre = ''
for i in range(x):
    pre += ' '
pre += '- '
mid = ': ' + raw_input("请输入对于docs的相对路径:")
su = '.md'
text = ''
ans=''
begin = int(input("输入开始点:"))
end = int(input("输入结束点:"))
end += 1

for i in range (begin, end):
    text = raw_input()
    ans += (pre+str(i)+'.'+text+mid+str(i)+su+'\n')
print(ans)
