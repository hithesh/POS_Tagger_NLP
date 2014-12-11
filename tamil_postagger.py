#!/usr/bin/python
import sys
f=open("train_tamil.txt","r")
li=f.readlines()
f.close()
tags=[]		
count_tags={}
for i in li :
	j=i.split(' ')
	j=j[2:-1]
	for k in j :
		m=k.split('_')
		if(len(m)==2) :
			if m[1] not in tags :
				tags.append(m[1])
				count_tags[m[1]]=0
			count_tags[m[1]]+=1
def Get_Matrix_1() :
	global li
	global tags
	Matrix_1={}
	for i in li :
		j=i.split(' ')
		j=j[2:-1]
		for k in j :
			m=k.split('_')
			if len(m)==2 :
				if m[0] not in Matrix_1 :
					Matrix_1[m[0]]=[]
					for z in tags :
						Matrix_1[m[0]].append(0)
				Matrix_1[m[0]][tags.index(m[1])]+=1
	for i in Matrix_1.keys() :
		k=0
		for j in range(len(Matrix_1[i])) :
			Matrix_1[i][j]/=float(count_tags[tags[j]])
	return Matrix_1
def Get_Matrix_2() :
	global li
	global tags
	Matrix_2={}
	for i in li :
		j=i.split(' ')
		j=j[2:-1]
		prev=["NULL","#"]			# '#' Tag for starting element
		for k in  j :
			m=k.split('_')
			if(len(m) ==2) :
				if m[1] not in Matrix_2 :
					Matrix_2[m[1]]=[]
					for z in tags:
						Matrix_2[m[1]].append(0)
					Matrix_2[m[1]].append(0)
				if prev[1]=="#" :
					Matrix_2[m[1]][0]+=1
				else :
					Matrix_2[m[1]][tags.index(prev[1])+1]+=1
				prev=m
	count=[]
	for i in tags :
		count.append(0)
	count.append(0)
	for i in Matrix_2.keys() :
		for j in range(len(Matrix_2[i])) :
			count[j]+=Matrix_2[i][j]
	for i in Matrix_2.keys() :
		for j in range(len(Matrix_2[i])) :
			Matrix_2[i][j]/=float(count[j])
	return Matrix_2
Matrix_1=Get_Matrix_1()
Matrix_2=Get_Matrix_2()
def RNN_Tagger(test) :
	global Matrix_1
	global Matrix_2
	global tags
	test=test.split(' ')
	test=test[2:-1]
	viter=[]
	for i in range(len(test)+1) :
		viter.append([])
		for j in tags :
			viter[-1].append([1,[]])
	k=1
	final=[]
	temp1=[]
	for i in test :
		if i not in Matrix_1 :			# If given word is not there in training data
			for v in tags :
				p=-1
				TAG=[]
				if k==1 :
					if -3==3:
						viter[k][tags.index(v)]=[float(1/(len(Matrix_1)*len(Matrix_1))),[v]]
					else :
						viter[k][tags.index(v)]=[float(Matrix_2[v][0]/(len(Matrix_1)+count_tags[v])),[v]]
				else :
					for u in tags :
						z=1
						if -3==3:
							z=viter[k-1][tags.index(u)][0]/float(len(Matrix_1)*len(Matrix_1))
						else :
							z=viter[k-1][tags.index(u)][0]*Matrix_2[v][tags.index(u)+1]/float(count_tags[v]+len(Matrix_1))
						if p<z :
							p=z
							TAG=viter[k-1][tags.index(u)][1]*1
							TAG.append(v)
					viter[k][tags.index(v)]=[p,TAG]
		else :						# If given word is present in training data
			for v in tags :
				p=-1
				TAG=[]
				if k==1 :			# Exception case for first word
					if -2==2:
						viter[k][tags.index(v)]=[Matrix_1[i][tags.index(v)]/float(len(Matrix_1)),[v]]
					else :
						viter[k][tags.index(v)]=[Matrix_2[v][0]*Matrix_1[i][tags.index(v)],[v]]
				else :
					for u in tags :
						if -2==2 :
							z=viter[k-1][tags.index(u)][0]*Matrix_1[i][tags.index(v)]/float(len(Matrix_1))
						else :
							z=viter[k-1][tags.index(u)][0]*Matrix_1[i][tags.index(v)]*Matrix_2[v][tags.index(u)+1]
						if p < z :
							p=z
							TAG=viter[k-1][tags.index(u)][1]*1
							TAG.append(v)
					viter[k][tags.index(v)]=[p,TAG]
		k+=1
	for i in viter[-1] :	
		final.append(i)
	return final		#final list contains the all outputs

symbols = ['"',"'",'!','@','#','$','%','^','&','*','(',')','-','_','+','=',';',':''/',',','.']
m=1
if len(sys.argv) < 2 :
	print "No Argument Given"
	sys.exit(0)
try :
	m = open(sys.argv[1],'r')
except :
	print "File Doesn't Exists"
	sys.exit(0)
input_lines = m.readlines()
m.close()
for t in input_lines:
    test=t
    t=t.split(' ')
    c  = t[:2]
    t=t[2:-1]
    final=RNN_Tagger(test)
    p=-1
    list1=[]
    for i in final :
	    if p < i[0] :
		    p=i[0]
		    list1=i[1]
    print ' '.join(c),
    for i in range(0,len(t)):
	if t[i] in symbols :
	    	print t[i]+'_SYM',
	else :
		print t[i]+'_'+list1[i],
    print '"'
