import random
from builtins import enumerate
from docplex.mp.model import Model
import Port
import Stack
import Slot
import Container


asp_model = Model('ASP')
#Data
#get Port
listPort = Port.getPort('',3)

D = listPort

#get Stack
listStack = Stack.getStack('',0)

J = [j[0] for j in listStack]
Ws = {j[0]:j[1] for j in listStack}
Hs = {j[0]:j[2] for j in listStack}
#Get Slot
listSlot = Slot.getSlot('',0)
K=[]
for j in J:
    lstKj = [s[0] for s in listSlot if s[1] == j]
    K.append(lstKj)

#Get Container
listCont = Container.getContainer('',100)
I = [i[0] for i in listCont]
Wc = {i[0]:i[2] for i in listCont}
Hc = {i[0]:i[3] for i in listCont}
Rc = {i[0]:i[5] for i in listCont}
T = [i[0] for i in listCont if i[1] == '20']
F = [i[0] for i in listCont if i[1] == '40']

Aid ={(i[0], d): Container.loadingPort(i[4],d) for i in listCont for d in D}

L = [i[0] for i in listCont if i[5] == 1]

M = [(i[6],i[7],i[0]) for i in listCont if i[5] == 1]

# Variables
#Cont qua tải
o = {i[0]:i[6] for i in listCont}
#o=asp_model.binary_var_dict(O,name='o')

#Contaitner trong bay j dỡ cảng d
P = [(j,d) for j in J for d in D]
p=asp_model.binary_var_dict(P,name='p')

#Stack đang sử dụng
EJ = [j for j  in J]
ej = asp_model.binary_var_dict(EJ,name='ej')

#Cont được để trong row i tier k bay j
C = [(J[j],K[j][k],i) for j in range(len(J)) for k in range(len(K[j])) for i in I]
c=asp_model.binary_var_dict(C,name='c')

#Cont dưới ô k ngăn j dở trước cảng d
q = [{(J[j],K[j][k],d):0} for j in range(len(J)) for k in range(len(K[j])) for d in D]


# print(I)
# print(Wc)
# print(Hc)
# print(Ws)
# print(Hs)
print('Start logic')
#Logic
#add Contraint
#2
asp_model.add_constraints((0.5*sum(c[J[j],K[j][k-1],i] for i in T)
                           + sum(c[J[j],K[j][k-1],i] for i in F)
                           - sum(c[J[j],K[j][k],i] for i in F)) >=0
                          for j in range(len(J)) for k in range(len(K[j])) if k>0)
print('Done add constraint #2')
#3
asp_model.add_constraints((sum(c[J[j],K[j][k],i] for i in T)
                           - sum(c[J[j],K[j][k-1],i] for i in T))<=0
                          for j in range(len(J)) for k in range(len(K[j])) if k>0)
print('Done add constraint #3')
#4
asp_model.add_constraints((0.5*sum(c[J[j],K[j][k],i] for i in T)
                           + sum(c[J[j],K[j][k],i] for i in F)) <= 1
                          for j in range(len(J)) for k in range(len(K[j])))
print('Done add constraint #4')
#5
asp_model.add_constraints(sum(sum(c[J[j],K[j][k],i] for k in range(len(K[j])))
                              for j in range(len(J))) == 1
                          for i in I)
print('Done add constraint #5')
#6
asp_model.add_constraints((sum(c[J[j],K[j][k],ii] for ii in T)
                           - 2*c[J[j],K[j][k],i]) >= 0
                          for j in range(len(J)) for k in range(len(K[j])) for i in T)
print('Done add constraint #6')
#7
# asp_model.add_constraints()
#print('Done add constraint #7')
#8
asp_model.add_constraints((sum(sum(Wc[i]*c[J[j],K[j][k],i] for i in I)
                               for k in range(len(K[j]))) <= Ws[J[j]])
                          for j in range(len(J)))
print('Done add constraint #8')
#9
asp_model.add_constraints((sum((0.5*sum(Hc[i]*c[J[j],K[j][k],i] for i in T)
                                + sum(Hc[i]*c[J[j],K[j][k],i] for i in F))
                               for k in range(len(K[j]))) <= Hs[J[j]])
                          for j in range(len(J)))
print('Done add constraint #9')
#10
#asp_model.add_constraints()
print('Done add constraint #10')
#11
# asp_model.add_constraints((A[i,d] * c[J[j],K[j][k],i] + q[J[j],K[j][k],d] - o[i]) <= 1
#                           for j in range(len(J)) for k in range(len(K[j]))
#                           for d in D for i in I)
print('Done add constraint #11')
#12
# asp_model.add_constraints((ej[J[j]] - c[J[j],K[j][k],i]) >=0
#                           for j in range(len(J)) for k in range(len(K[j])) for i in I)
print('Done add constraint #12')
#13
# asp_model.add_constraints((p[J[j],d] - A[i,d] * c[J[j],K[j][k],i]) >=0
#                           for j in range(len(J)) for k in range(len(K[j]))
#                           for d in D for i in I)
print('Done add constraint #13')
#14
asp_model.add_constraints(c[J[j],K[j][k],i[0]] == 1
                                    for j in range(len(J)) for k in range(len(K[j]))
                          for i in I if (J[j],K[j][k],i) in M)
print('Done add constraint #14')
#15
#asp_model.add_constraints()
print('Done add constraint #15')

#Config Objecttive
asp_model.minimize(100*sum(o[i] for i in I)
                   + 20*sum(p[J[j],D[d]] for j in range(len(J)) for d in range(len(D)) if d>0)
                   + 10*sum(ej[J[j]] for j in range(len(J))))
#Run
asp_model.parameters.timelimit=5200
asp = asp_model.solve(log_output=True)
#asp.display()
print("<===========INFORMATION==================>")
asp_model.print_information()
print("<===========SOLUTION==================>")
asp_model.print_solution()
print("<===========DISPLAY==================>")
#Fail
if asp is None:
    print("Infeasible")
else:
    asp.display()
    print("<===========RES==================>")
    #A_activos=[i for i in C if c[i].solution_value>0.9]
    #print(A)
    print("<===========C==================>")
    B_activos=[i for i in C if c[i].solution_value]
    print(B_activos)