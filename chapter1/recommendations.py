#!/usr/bin/python
# -*- coding:utf-8 -*-
from math import sqrt
#一个词典，包含影迷以及电影评价
#hello,a little test
critics = {
	'Lisa Rose':{
		'Lady in the Water': 2.5, 
         'Snakes on a Plane': 3.5, 
         'Just My Luck': 3.0, 
         'Superman Returns': 3.5, 
         'You, Me and Dupree': 2.5, 
         'The Night Listener': 3.0, 
	},
	'Gene Seymour': { 
         'Lady in the Water': 3.0, 
         'Snakes on a Plane': 3.5, 
         'Just My Luck': 1.5, 
         'Superman Returns': 5.0, 
         'The Night Listener': 3.0, 
         'You, Me and Dupree': 3.5, 
     }, 
     'Michael Phillips': { 
         'Lady in the Water': 2.5, 
         'Snakes on a Plane': 3.0, 
         'Superman Returns': 3.5, 
         'The Night Listener': 4.0, 
     }, 
     'Claudia Puig': { 
         'Snakes on a Plane': 3.5, 
         'Just My Luck': 3.0, 
         'The Night Listener': 4.5, 
         'Superman Returns': 4.0, 
         'You, Me and Dupree': 2.5, 
     }, 
     'Mick LaSalle': { 
         'Lady in the Water': 3.0, 
         'Snakes on a Plane': 4.0, 
         'Just My Luck': 2.0, 
         'Superman Returns': 3.0, 
         'The Night Listener': 3.0, 
         'You, Me and Dupree': 2.0, 
     }, 
     'Jack Matthews': { 
         'Lady in the Water': 3.0, 
         'Snakes on a Plane': 4.0, 
         'The Night Listener': 3.0, 
         'Superman Returns': 5.0, 
         'You, Me and Dupree': 3.5, 
     }, 
     'Toby': {
     	'Snakes on a Plane': 4.5,
      	'You, Me and Dupree': 1.0, 
       	'Superman Returns': 4.0}, 
}
#hello
#返回一个有关person1与person2的基于距离的相似度评价
def sim_distance(prefs,person1,person2):
	#得到shared_items的列表
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1

		if len(si)==0: return 0

		sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                            for item in prefs[person1] if item in prefs[person2]])

        return 1/(1+sqrt(sum_of_squares))


#同样是返回一个有关person1和person2的相似度评价，但与之前不相同的是如果一个人一般总比另一个人评分高一点，利用基于距离的评价会
#判断有误，所以此方法提供一个基于拟合直线的评价方法，利用点距离你和直线的偏移量来判断，如果相关系数为1，则证明完全一样
def sim_pearson(prefs,person1,person2):

#该函数将返回一个介于1和-1之间的数，如果返回1，则认为两个人完全相同    

    si={}
    #得到双方都曾评价过的物品
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #限制列表元素个数
    n=len(si)
    #如果没有共同之处，则返回1
    if n==0: return 1

    #对所有偏好求和
    sum1=sum([prefs[person1][item] for item in si])
    sum2=sum([prefs[person2][item] for item in si])

    #求平方和
    sum1Sq=sum([pow(prefs[person1][item],2) for item in si])
    sum2Sq=sum([pow(prefs[person2][item],2) for item in si])

    #求乘积之和
    pSum=sum([prefs[person1][item]*prefs[person2][item] for item in si])

    #计算皮尔逊评价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0:return 0

    r=num/den
    return r

    pass

def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]

#利用所有他人的加权评价值进行平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}

    for other in prefs:
    #不要和自己比较
        if other==person: continue
        sim=similarity(prefs,person,other)

        #忽略评价值为零或者小于零的情况
        if sim<0 or sim ==0 :continue
        for item  in prefs[other]:


            #只对自己还没看过的电影进行评价
            if item not in prefs[person] or prefs[person][item] == 0:
            #相似度*评价值 
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
            #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim 

    #建立一个归一化的列表
    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    #返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings