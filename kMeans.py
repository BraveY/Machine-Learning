# -*- coding:UTF-8 -*-
from numpy import *
def loadDataSet(filename) :
    dataMat = []
    fr = open(filename)
    for line in fr.readlines() :
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)      #将读取到的数据转换为浮点型
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB) :
    return sqrt(sum(power(vecA - vecB, 2))) #求两个向量的欧式距离

def randCent(dataSet, k) :
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))          #将k，n维的全零数组转换为矩阵
    for j in range(n) :
        minJ = min(dataSet[:,j])           #dataSet中第J列的最小值
        rangeJ = float(max(dataSet[:,j]) - minJ) #确定质心的边界
        centroids[:,j] = minJ + rangeJ*random.rand(k,1)  #生成质心
    return centroids

datMat = mat(loadDataSet('testSet2.txt'))

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent) :
    m = shape(dataSet)[0]                    #确定数据集中的行数，也就是数据集中的点数
    clusterAssment = mat(zeros((m, 2)))      #用来记录每个点的簇分配情况，其中第一列为簇索引值，第二列存储误差
    centroids = createCent(dataSet, k)       #初始化质点
    clusterChanged =True
    while clusterChanged:
        clusterChanged = False
        for i in range(m) :
            minDist = inf                   #初始为正无穷大
            minIndex = -1
            for j in range(k) :
                distJI = distMeas(centroids[j,:], dataSet[i,:])     #对每一个数据点计算它与簇质心的距离
                if distJI < minDist :
                    minDist = distJI                                #在j个质心中寻找到最短的距离，并更新对应的簇索引
                    minIndex = j
            if clusterAssment[i,0] != minIndex :                    #簇分配与之间的索引不同则迭代
                clusterChanged = True
                clusterAssment[i,:] = minIndex, minDist**2          #更新簇分配矩阵中的索引与误差
        # print 'centroids'
        # print centroids
        for cent in range(k) :                                      #重新计算质心
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = mean(ptsInClust,axis=0)             #沿矩阵列的方向计算均值
    return centroids, clusterAssment
# centroids ,clusterAssment = kMeans(datMat, 4)
# print centroids
# print clusterAssment

#二分k- 均值聚类算法

def biKmeans(dataSet, k, distMeans=distEclud) :
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m) :
        clusterAssment[j,1] = distMeans(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k) :
        lowestSSE = inf
        for i in range(len(centList)) :
            ptsInCurrCluster =\
                    dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]           #统计当前簇的全部数据点
            centroidMat, splitClustAss =\
                    kMeans(ptsInCurrCluster, 2, distMeans)                     #对统计到的簇再划分出两个小簇
            sseSplit = sum(splitClustAss[:,1])                                 #计算划分为两个簇后总误差
            sseNotSplit =\
                sum(clusterAssment[nonzero(clusterAssment[:, 0].A!=i)[0],1])  #计算没有划分的簇的总误差
            print "seeSplit, and notSplit: ", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE :
                bestCentTopSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] =\
                            len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = \
                            bestCentTopSplit
        print 'the bestCentTopSplit is :', bestCentTopSplit
        print 'the len of bestClustAss is :', len(bestClustAss)
        centList[bestCentTopSplit] = bestNewCents[0,:]
        centList.append(bestNewCents[1,:])
        clusterAssment[nonzero(clusterAssment[:,0].A == \
                               bestCentTopSplit)[0],:] = bestClustAss
    return  centList, clusterAssment
centList, myNewAssments = biKmeans(datMat, 3)
print centList