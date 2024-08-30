import random
from builtins import enumerate
from docplex.mp.model import Model
import Port
import Stack
import Slot
import Container
import logging

cplex_ins_path = '/opt/ibm/ILOG/CPLEX_Studio2211'
logging.basicConfig(filename='terminal_output.log', level=logging.INFO, filemode='w')

asp_model = Model('ASP')
#Data
#get Port
listPort = Port.getPort('', 2)

D = listPort

#get Stack
listStack = Stack.getStack('',0)

J = [j[0] for j in listStack]
Ws = {j[0]:j[1] for j in listStack}
Hs = {j[0]:j[2] for j in listStack}

#Get Slot
listSlot = Slot.getSlot('',0)
K ={ j: [s[0] for s in listSlot if s[1] == j] for j in J}
R ={ j: [s[3] for s in listSlot if s[1] == j] for j in J}
#Get Container
listCont = Container.getContainer('',80)

I = [i[0] for i in listCont]
Wc = {i[0]:i[2] for i in listCont}
Hc = {i[0]:i[3] for i in listCont}
Rc = {i[0]:i[5] for i in listCont}
T = [i[0] for i in listCont if i[1] == '20']
F = [i[0] for i in listCont if i[1] == '40']

A ={(i[0], d): Container.loadingPort(i[4],d) for i in listCont for d in D}

L = [i[0] for i in listCont if i[5] == 1]

M = [(i[6],i[7],i[0]) for i in listCont if i[5] == 1]

# Variables
#Cont qua tải
o = {i[0]:i[6] for i in listCont}
o = asp_model.binary_var_dict(o,name='o')

#Contaitner trong bay j dỡ cảng d
P = [(j,d) for j in J for d in D]
p = asp_model.binary_var_dict(P,name='p')

#Stack đang sử dụng
EJ = [j for j  in J]
ej = asp_model.binary_var_dict(EJ,name='ej')

#Cont được để trong row i tier k bay j
C = [(j,k,i) for j in J for k in K[j] for i in I]
c=asp_model.binary_var_dict(C,name='c')

#Cont dưới ô k ngăn j dở trước cảng d
q = {(j,k,d):0 for j in J for k in K[j] for d in D}


#2
asp_model.add_constraints((0.5*sum(c[j,K[j][k-1],i] for i in T)
                           + sum(c[j,K[j][k-1],i] for i in F)
                           - sum(c[j,K[j][k],i] for i in F)) >=0
                          for j in J for k in range(len(K[j])) if k>0)
print('Done add constraint #2')
#3
asp_model.add_constraints((sum(c[j,K[j][k],i] for i in T)
                           - sum(c[j,K[j][k-1],i] for i in T))<=0
                          for j in J for k in range(len(K[j])) if k>0)
print('Done add constraint #3')
#4
asp_model.add_constraints((0.5*sum(c[j,k,i] for i in T)
                           + sum(c[j,k,i] for i in F)) <= 1
                          for j in J for k in K[j])
print('Done add constraint #4')
#5
asp_model.add_constraints(sum(sum(c[j,k,i] for k in K[j])
                              for j in J) == 1
                          for i in I)
print('Done add constraint #5')
#6
asp_model.add_constraints((sum(c[j,k,ii] for ii in T)
                           - 2*c[j,k,i]) >= 0
                          for j in J for k in K[j] for i in T)
print('Done add constraint #6')
# 7
for j in J:
    for k in range(len(K[j])):
        constraint_expr = asp_model.sum(Rc[i] * c[j, K[j][k], i] for i in I) - R[j][k]
        asp_model.add_constraint(constraint_expr <= 0)
print('Done add constraint #7')
#8
asp_model.add_constraints((asp_model.sum(asp_model.sum(Wc[i]*c[j,K[j][k],i] for i in I)
                               for k in range(len(K[j]))) <= Ws[j])
                          for j in J)
print('Done add constraint #8')
# #9
asp_model.add_constraints(asp_model.sum((0.5*asp_model.sum(Hc[i]*c[j,k,i] for i in T)
                                + asp_model.sum(Hc[i]*c[j,k,i] for i in F))
                               for k in K[j]) <= Hs[j]
                          for j in J)
print('Done add constraint #9')
#10
#asp_model.add_constraints()
# print('Done add constraint #10')
# #11
asp_model.add_constraints((A[i,d] * c[j,k,i] + q[j,k,d] - o[i]) <= 1
                          for j in J for k in K[j] for d in D for i in I)
print('Done add constraint #11')
#12
asp_model.add_constraints((ej[j] - c[j,k,i]) >=0
                          for j in J for k in K[j] for i in I)
print('Done add constraint #12')
#13
asp_model.add_constraints((p[j,d] - A[i,d] * c[j,k,i]) >=0
                          for j in J for k in K[j] for d in D for i in I)
print('Done add constraint #13')
#14
asp_model.add_constraints(c[j,k,i] == 1
                          for j in J for k in K[j] for i in L if (j,k,i) in M)
print('Done add constraint #14')
# 15
z = 0.5

# 16
x = 0.5

#Config Objecttive
asp_model.minimize(100*sum(o[i] for i in I)
                   + 20*sum(p[j,D[d]] for j in J for d in range(len(D)) if d>0)
                   + 10*sum(ej[j] for j in J))
#Run
# asp_model.parameters.timelimit=60
asp = asp_model.solve(log_output=True)
#asp.display()
logging.info("<===========INFORMATION==================>")
logging.info(asp_model.print_information())
# f.write(str(asp_model.print_information()))
logging.info("<===========SOLUTION==================>")
logging.info(asp_model.print_solution())
# f.write(str(asp_model.print_solution()))
logging.info("<===========DISPLAY==================>")
#Fail
if asp is None:
    logging.info("Infeasible")
else:
    logging.info(asp.display())
    # f.write(str(asp.display()))
    logging.info("<===========RES==================>")
    #A_activos=[i for i in C if c[i].solution_value>0.9]
    #print(A)
    logging.info("<===========C==================>")
    B_activos=[i for i in C if c[i].solution_value]
    logging.info(B_activos)
    # f = open("../Data/res.txt","a")
    # f.write(B_activos)
    # f.close()
