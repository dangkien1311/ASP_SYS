# https://www.ibm.com/mysupport/s/question/0D53p00008BgClkCAF/cvrp-threeindex-vehicle-formulation-with-docplex?language=en_US
# https://medium.com/cmsa-algorithm-for-the-service-of-the-capacitated/using-cplex-and-python-for-finding-an-exact-solution-for-the-cvrp-ac789ee0d8c4
# https://medium.com/cmsa-algorithm-for-the-service-of-the-capacitated/state-of-art-of-the-capacitated-vehicle-rooting-problem-30ad4de6c2e9
n=150                     # SỐ KHÁCH HÀNG
N=[x for x in range(1,n+1)] #N=clientes
V=[0]+N     #V = Nodos

Q=20
#K=10
import numpy as np  #tạo tập ngẫu nhiên các node
rnd=np.random

import csv
with open('demand.csv') as demand:
    reader = csv.reader(demand)
    dm = [row for row in reader]
q={i:int(dm[i][1]) for i in range(1,n+1)}  #chuyển xâu sang số. Lưu list cột 2 sang mảng q có 15 phần tử 1->n=15
print(q)

with open('data.csv') as f1:
    reader1 = csv.reader(f1)
    l = [row for row in reader1]
loc_x=[int(l[i][1])*2 for i in range(1,n+3)]  #chuyển xâu sang số. Lưu list cột 2 sang mảng loc_x có 17 phần tử
print(loc_x)
loc_y=[int(l[i][2]) for i in range(1,n+3)] #chuyển xâu sang số. Lưu list cột 3 sang mảng loc_y có 17 phần tử
print(loc_y)

##import matplotlib.pyplot as plt

A=[(i,j) for i in V for j in V if i!=j]                 
print(A,"\n")
c={(i,j):np.hypot(loc_x[i]-loc_x[j],loc_y[i]-loc_y[j])
           for i in V for j in V if i!=j}

#in khoảng cách (i,j) dạng ma tran (tim hieu them)
print(c)

from docplex.mp.model import Model

mdl=Model('CVRP')

x=mdl.binary_var_dict(A,name='x')
u=mdl.continuous_var_dict(N, ub=Q, name='u')

mdl.minimize(mdl.sum(c[i,j]*x[i,j] for i,j in A))



mdl.add_constraints(mdl.sum(x[i,j] for j in V if i!=j)==1
                    for i in N)
mdl.add_constraints(mdl.sum(x[i,j] for i in V if i!=j)==1
                    for j in N)

mdl.add_indicator_constraints(mdl.indicator_constraint(x[i,j],u[i]+q[j]==u[j])
                    for i,j in A if i!=0 and  j!=0)
mdl.add_constraints(u[i]>=q[i] for i in N)

mdl.parameters.timelimit=5200
solution=mdl.solve(log_output=True)

mdl.get_solve_status()      #Xem lại giá trị của hàm này
solution.display()

A_activos=[k for k in A if x[k].solution_value>0.9]
print(A_activos)

import matplotlib.pyplot as plt
plt.figure(figsize=(12,5))
plt.scatter(loc_x,loc_y,color="green")
for i in N:
    plt.annotate('$q_{%d}=%d$'%(i,q[i]),(loc_x[i]+1,loc_y[i]-0.5))
plt.plot(loc_x[0],loc_y[0],color='red',marker='s')
plt.annotate('DC',(loc_x[0]-2,loc_y[0]+2))
for i,j in A_activos:
    plt.plot([loc_x[i],loc_x[j]],[loc_y[i],loc_y[j]],color="blue", alpha=0.3)
plt.xlabel("Trục x")
plt.ylabel("Trục y")
plt.title("Cao Ngọc Ánh - CVRP")
plt.show()
##print(q)
##print(loc_x)
##print(loc_y)
##print(arcos)
##print(distancia)
print(mdl.export_to_string())
