import numpy as np

def rk2OneStep(x0, v0, h, A):
    x1 = x0 + h

    E = np.array([[1 , 0],
                  [0 , 1]])
    
    k1 = A @ v0
    k2 = np.linalg.inv(E - (h/2)*A) @ (E + (h/2)*A) @ k1
    v1 = v0 + (h/2)*(k1 + k2)
    return x1, v1

def rk2WithoutControl(x0, u0, h, A, H, Nmax, Egr, Eps):
    x = np.array([])
    u1 = np.array([])
    u2 = np.array([])
    Olp = np.array([0])
    hList = np.array([0])

    x = np.append(x, x0)
    u1 = np.append(u1, u0[0])
    u2 = np.append(u2, u0[1])

    for i in range(Nmax):
        if(x[i] + h > H + Egr and x[i] < H - Egr):
            tempX, tempU = rk2OneStep(x[i], [u1[i] , u2[i]], H - x[i], A)
            tempX_halfStep, tempU_halfStep = rk2OneStep(x[i], [u1[i] , u2[i]], (H - x[i])/2.0, A)
            tempX_2step, tempU_2step = rk2OneStep(tempX_halfStep, tempU_halfStep, (H - x[i])/2.0, A)
        else:
            tempX, tempU = rk2OneStep(x[i], [u1[i] , u2[i]], h, A)
            tempX_halfStep, tempU_halfStep = rk2OneStep(x[i], [u1[i] , u2[i]], h/2.0, A)
            tempX_2step, tempU_2step = rk2OneStep(tempX_halfStep, tempU_halfStep, h/2.0, A)


        x = np.append(x, tempX)
        u1 = np.append(u1, tempU[0])
        u2 = np.append(u2, tempU[1])
        hList = np.append(hList, h)

        Olp = np.append(Olp, np.max((tempU_2step - tempU) *(4/3)))


        if(tempX <= H + Egr and tempX >= H - Egr):
            break
        
    return x, u1, u2, Olp, hList

def rk2WithControl(x0, u0, h, A, H, Nmax, Egr, Eps):
    x = np.array([])
    u1 = np.array([])
    u2 = np.array([])
    Olp = np.array([0])

    x = np.append(x, x0)
    u1 = np.append(u1, u0[0])
    u2 = np.append(u2, u0[1])
    hList = np.array([0])
    
    hChange = h
    i = 0
    while(i < Nmax):
        if(x[i] + hChange > H + Egr and x[i] < H - Egr):
            tempX, tempU = rk2OneStep(x[i], [u1[i] , u2[i]], H - x[i], A)
            tempX_halfStep, tempU_halfStep = rk2OneStep(x[i], [u1[i] , u2[i]], H - x[i]/2.0, A)
            tempX_2step, tempU_2step = rk2OneStep(tempX_halfStep, tempU_halfStep, H - x[i]/2.0, A)
        else:
            tempX, tempU = rk2OneStep(x[i], [u1[i] , u2[i]], hChange, A)
            tempX_halfStep, tempU_halfStep = rk2OneStep(x[i], [u1[i] , u2[i]], hChange, A)
            tempX_2step, tempU_2step = rk2OneStep(tempX_halfStep, tempU_halfStep, hChange, A)
        
        S = (tempU_2step - tempU)/3
        Snorm = np.max(np.abs(S))

        if(((Eps/8) <= Snorm) and (Snorm <= Eps)):
            x = np.append(x, tempX)
            u1 = np.append(u1, tempU[0])
            u2 = np.append(u2, tempU[1])
            Olp = np.append(Olp, Snorm*4)
            hList = np.append(hList, hChange)
        elif(Snorm <= Eps/8):
            x = np.append(x, tempX)
            u1 = np.append(u1, tempU[0])
            u2 = np.append(u2, tempU[1])
            Olp = np.append(Olp, Snorm*4)
            hList = np.append(hList, hChange)
            hChange *= 2
        else:
            hChange /= 2
            continue

        i = i + 1

        if(tempX <= H + Egr and tempX >= H - Egr):
            break
    
    return x, u1, u2, Olp, hList

        
def getTrueSolution(x, x0, u01, u02):
    eigenVal1 = -1000.0
    eigenVal2 = -1.0/100.0
    eigenVect1 = [-1.0,1.0]
    eigenVect2 = [1.0,1.0]

    linSyst = np.array([[eigenVect1[0], eigenVect2[0]],
                        [eigenVect1[1], eigenVect2[1]]])
    
    rightPart = np.array([u01, u02])
    coef = np.linalg.solve(linSyst,rightPart)
    u1 = np.array([])
    u2 = np.array([])
    for i in x:
        u1 = np.append(u1, coef[0] * eigenVect1[0] * np.exp(eigenVal1*(i - x0)) + coef[1] * eigenVect2[0] * np.exp(eigenVal2*(i - x0)))
        u2 = np.append(u2, coef[0] * eigenVect1[1] * np.exp(eigenVal1*(i - x0)) + coef[1] * eigenVect2[1] * np.exp(eigenVal2*(i - x0)))
    return u1, u2
