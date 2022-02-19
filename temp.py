# import sys
# from turtle import st
# a = [i.strip() for i in sys.stdin]
# res_res = []
# for i in a:
#     b = [int(y) for y in i.split()]
#     res = []
#     for j in range(1, len(b) - 1):
#         if b[j] % 2 == 0:
#             res.append(int(str(b[0] // 100) + str(b[j]) + str(b[-1] // 10)))
#     res_res.append(res)
# print(res_res)




# kkk = ('123', 'adsgaz')
# def fff(*arg, ppp = 5*"ccc"):
#     global kkk
#     a = kkk
#     result = []
#     for i in range(len(arg)):
#         count = 0
#         tmp = [x for x in str(arg[i])]
#         try:
#             tmp2 = [x for x in str(a[i])]
#             for i in set(tmp + tmp2):
#                 if (i not in tmp and i in tmp2) or (i in tmp and i not in tmp2):
#                     count += 1
#         except Exception as ex:
#             print(ex)
#     kkk = tuple(result)






def fff(*arg, p1=5, p2=3, p3=None, **args):
    dic = {}
    s1, s2, s3 = [], [], []
    for i in arg:
        if len(i) >= p1 and i.isalpha():
            s1.append(i)
        elif not i.isalpha():
            s3.append(i)
        elif (type(p2) == int and len(set(i)) >= p2) or (len(set(i)) == len(set(p2))):
            s2.append(i)
        else:
            print(1)
    print(s1, s2, s3, sep='\n')

fff('saf', 'Aefwegrarwg', '124sadf')