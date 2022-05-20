from scipy.optimize import linprog

#Translation of COMP3217-example3.lp to scipy linprog
c = [21,22,22,23,23,24,24,25]
A = [[0,1,0,1,0,1,0,0],
     [1,0,1,0,1,0,1,1]]
b = [3,
     9]
x1_17 = (0,2)
x1_18 = (0,2)
x1_19 = (0,2)
x2_16 = (0,3)
x2_17 = (0,3)
x2_18 = (0,3)
x2_19 = (0,3)
x2_20 = (0,3)

res = linprog(c, A_eq=A, b_eq=b, bounds=[x2_16, x1_17, x2_17, x1_18, x2_18, x1_19, x2_19, x2_20])
print("Minium cost:", res.fun)
print(res)