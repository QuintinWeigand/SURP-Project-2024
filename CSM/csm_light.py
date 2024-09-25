import numpy as np
import matplotlib.pyplot as plt

global N
N = 12 
global B_F
B_F = 1.226
global B_R
B_R = 0.987
global A
A = 0.038
global S
S = 2
global BETA
BETA = 13.8
global DELTA
DELTA = 0
global SPEED_OF_LIGHT
SPEED_OF_LIGHT = 3.0e10
global K
K = 0.33

def simpson(ts_ex1, vs_ex1):
    
    #Calculates the area with the data points from the lists sent
    area_Simp = vs_ex1[0]

    for i in range(1,len(ts_ex1)-1):
        if i%2 == 1:
            area_Simp += 4.0 * vs_ex1[i]
        else:
            area_Simp += 2.0 * vs_ex1[i]
    area_Simp += vs_ex1[-1]
        
    area_Simp *= (ts_ex1[1] - ts_ex1[0]) / 3.0

    #Returns the final area (the integral) to the calling environment
    return area_Simp

def calcualteQ(m_csm, r_csm, radius_p):
    q = (((3-S) * m_csm) / (r_csm**(3-S) - radius_p**(3-S)))
    return q

def calculateR_ph(q, r_csm):
    r_ph = ((((2/3) * ((1-S) / (K * q))) + r_csm**(1-S)))**((1) / (1-S))
    return r_ph

def calculateM_CSM_TH(q, r_ph, r_p):
    m_csm_th = ( ((4 * np.pi * q) / (3-S)) * (r_ph**(3-S) - r_p**(3-S)) )
    return m_csm_th

def calculateT_0(m_csm_th, r_ph):
    t_naught = (K * m_csm_th) / (BETA * SPEED_OF_LIGHT * r_ph)
    return t_naught

def calcualteESN(v_sn, massOfEjecta):
    ESN = (((3 * (N-3) / (10 * (N-5)))) * v_sn**2 * massOfEjecta)
    return ESN

def calculateT_I(VSN, radius_p):
    return (radius_p / VSN)

def calcualteG_N(ESN, massOfEjecta):
    G_N = (1 / (4 * np.pi * (DELTA - N))) * ( ( (2 * (5 - DELTA) * (N-5) * ESN)**((N-3)/2) ) / ((3 - DELTA) * (N-3) * massOfEjecta)**((N-5) / 2))
    return G_N

def calculateT_FS_STAR(q, m_csm_th, g_n):
    funkyPower = ((N-S) / (N-3) * (3-S))
    t_fs_star = (np.abs( ((3-S) * q**((3-N)/(N-S)) * (A * g_n)**((S-3) / (N-S))) / (4 * np.pi * B_F**(3-S))))**(funkyPower) * m_csm_th**(funkyPower)
    return t_fs_star

def calculateT_RS_STAR(v_sn, g_n, q, massOfEjecta):
    t_rs_star = ( ( ( (v_sn) / ((B_R) * ((A * g_n) / q))**(1/(N-S)) ) * 
                 (1 - ((3-N) * massOfEjecta) / (4 * np.pi * (v_sn)**(3-N) * g_n)))**(1/(3-N)) )**((N-S) / (S-3))
    return t_rs_star

def stepFunction(x):
    returnValue = 0
    if x > 0:
        returnValue = 1
    return returnValue

def function_1(t_prime):
    t_0 = calculateT_0(m_csm = 0, r_ph = 0)
    t_i = calculateT_I(VSN=0, radius_p=0)
    g_n = calcualteG_N(ESN=0, massOfEjecta=0)
    q = calcualteQ(m_csm=0,r_csm=0,radius_p=0)

    instance = (
        ( (2 * np.pi) / (N - S)**3 ) * g_n**( (5-S) / (N-S) ) * q**( (N-5) / (N-S) ) * (N-3)**2 * (N-5) * B_F**(5-S) *
        A**( (5-S) / (N-S) ) * (t_prime + t_i)**( (2*N + 6 * S - N*S - 15) / (N-S) ) * stepFunction(x=0) + 2 * np.pi * ( (A*g_n) / (q) )**( (5-N) / (N-S) ) *
        B_R**(5-N) * g_n * ( (3-S) / (N-S) )**3 * (t_prime + t_i)**( (2*N + 6 * S - N*S - 15) / (N-S) ) * stepFunction(x=0)
    )    


    return instance;

#This is where the nickel decay integral goes
def function_2():

    instance = 0
    return instance

def returnCSMLuminosity():
    luminosity = 0
    t_0 = calculateT_0(m_csm_th=0,r_ph=0)

    t = t * 86400

    x_prime = np.linspace(0, t ,1000)
    #We need a list for each integral (2 total lists)
    #List 1
    list_1 = np.array([function_1(t_prime)] for t_prime in x_prime)
    list_2 = np.array([function_2(t_prime) for t_prime in x_prime])

    integral_1 = simpson(x_prime, list_1)
    integral_2 = simpson(x_prime, list_2)

    part_1 = (1 / t_0) * np.exp((-t) / t_0)
    part_2 = integral_1
    part_3 = integral_2

    luminosity = part_1 * part_2 * part_3

    return luminosity


x_list = np.linspace(1,200,398)


#These are temporary representing the inevitable inputs (I am acting as if I had the inputs right now)
ejectaMass = 0
ejectaVelocity = 0
massNI = 0
massCSM = 0
radius = 0
radiusCSM = 0

y_list = np.array([returnCSMLuminosity(t, ejectaMass) for t in x_list])


#NOTE: All I need is to verify what values are being passed in and what 
#      to copy from the nickel decay model. It seems like a lot but I believe it really isn't

#This is bogus for not bull I'll just have it commented out.
# fig, ax = plt.subplots()
# ax.plot(x_list, y_list,
#         linestyle = '-',
#         color = 'black',
#         linewidth = 2)

# ax.set_title('Luminosity ( L(t) ) vs. Time (Days)')
# ax.set_xlabel('Time (Days)')
# ax.set_ylabel('Luminosity ( L(t) )')

# #Displays the plot
# plt.show()
