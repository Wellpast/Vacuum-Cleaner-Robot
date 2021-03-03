#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 22:30:12 2021

@author: wellpast
"""

from random import randint

def individual(length, min, max):
    return [randint(min,max) for x in range(length)]

def population(count, length, min, max):
    return[individual(length, min, max) for x in range(count)]
    
from operator import add
from functools import reduce

def fitness(individual, target):
    sum = reduce(add, individual, 0)
    return abs(target-sum)
    
def grade(pop, target):
    summed = reduce(add,(fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)

from random  import random

print("Üretilecek popülasyonun sayısını 10 adettir.")
print("Sayı aralığının başlangıç değerini 0'dır.")
print("Sayı aralığının son değerini 5'dir.")
print("Popülasyon oranımız 50'dir")
g=population(50,2,0,10)
newg=g
print(g)
def mutatx(ga):
    chance_to_mutate =0.9
    print('İlk çiftleşme:',ga)
    print("İlk çözüm kümesi popülasyon:",g)
    n=0
    for i in ga:
        r=random()
        if chance_to_mutate > r:
            print('Anne ve babadan',n,'Mutasyanlar meydana geldi.')
            place_to_modify = randint(0,len(i)-1)
            print('Bu sayıya göre:', place_to_modify)
            i[place_to_modify] = randint(min(i), max(i))
        ga[n]=i
        n=n+1
        print(i)
    return ga
print("Nesillerin uygunluk derecesi 20 belirlenmiştir.")
print("Nesillerin mutasyon oranı 0.2 ihtimalken random seçilim oranı 0.01 olarak seçilmiştir.")
target=20
pop=population(10,2,0,5)
retain=0.3
mutate=0.2
random_select=0.01

gradeda = [(fitness(x, target), x) for x in pop]
graded=[ x[1] for x in sorted(gradeda)]
graded0=[ x[0] for x in sorted(gradeda)]
retain_length = int (len(graded)*retain)
parents=graded[:retain_length]      
print("Anne ve baba ebebeyler için en iyi seçimler",parents)      

for individu in graded[retain_length:]:
    if random_select > random():
        parents.append(individu)
        
print("Ebebeyn popülasyonunda elemeler sonucunda en iyi seçimler", parents)

for individu in parents:
    if mutate > random():
        pos_to_mutate = randint(0, len(individu)-1)
        #this mutation is not ideal because it
        #restriscts the range of possible values,
        #but the function is unware of the min/max
        #values used to create the individual,
        individu[pos_to_mutate] = randint(min(individu), max(individu))
print("Popülasyon mutasyonları devam ediyor.",parents)

#crossover
parents_length = len (parents)
desired_length = len(pop) - parents_length
children = []
while len(children) < desired_length:
    malenumber = randint(0, parents_length-1)
    femalenumber = randint(0, parents_length-1)
    if malenumber!= femalenumber:
        male = parents[malenumber]
        female = parents[femalenumber]
        half = round(len(male)/2)
        child = male[:half] + female[half:]
        children.append(child)
parents.extend(children)
print("Mutasyonlar sonucunda en iyi popülasyonlar",parents)
#x=parents[1][0]
#y=parents[1][1]

#print("x=",x)
#print("y=",y)
        
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

x_guncel=3
y_guncel=2
k=0
for k in range(10):
    x=parents[k][0] 
    y=parents[k][1]
    print("Gidilecek konum noktaları: x=",x,"y=",y)
    
    if  (x_guncel != x and y_guncel != y):
        def movebase_client():
            client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
            client.wait_for_server()
            target = MoveBaseGoal()
            target.target_pose.header.frame_id = "map"
            target.target_pose.pose.position.x = x 
            target.target_pose.pose.position.y = y
            target.target_pose.pose.orientation.w = 1.0
            client.send_goal(target)
            wait = client.wait_for_result()
            if not wait:
                rospy.signal_shutdown("Action Servisi yok!")
            else:
                return client.get_result()
        if __name__ == '__main__':
            try:
                rospy.init_node('Move_Target')
                result = movebase_client()
                if result:
                     rospy.loginfo("Hedef noktaya varıldı!")
                     x_guncel=x
                     y_guncel=y
                else:
                     rospy.loginfo("Hedefe gidiliyor...")
            except rospy.ROSInterruptException:
                pass
    















    

