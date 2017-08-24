from numpy import *
data = [[1,2],
        [1,3],
        [2,5],
        [2,4]]
data = mat(data)
print data
print data.A
# list = [[0],[1],[2],[3]]
# print list
# list = mat(list)
# print list.B
l = data[:,0]
# print data[:,0].A==2
print l
print l==2