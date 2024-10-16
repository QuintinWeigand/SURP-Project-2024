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

global FUNKYPOWER
FUNKYPOWER = ((N-S) / (N-3) * (3-S))

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
    q = (((3-S) * m_csm) / (4.0 * np.pi * (r_csm**(3-S) - radius_p**(3-S))))
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

def calculateVSN(esn, massOfEjecta):
    vsn = np.sqrt( (10 * (N-5) * esn) / (3 * (N-3) * massOfEjecta) )
    return vsn

def calculateT_I(VSN, radius_p):
    return (radius_p / VSN)

def calcualteG_N(ESN, massOfEjecta):
    G_N = np.abs(1 / (4 * np.pi * (DELTA - N))) * \
        ( ( (2 * (5 - DELTA) * (N-5) * ESN)**((N-3)/2) ) / 
         ((3 - DELTA) * (N-3) * massOfEjecta)**((N-5) / 2))
    return G_N

def calculateT_FS_STAR(q, m_csm_th, g_n):
    FUNKYPOWER = ((N-S) / (N-3) * (3-S))
    #print((A * g_n)**((S-3) / (N-S)))
    #print((3-S) * q**((3-N)/(N-S)), (A * g_n)**((S-3) / (N-S)))
    #print((np.abs( ((3-S) * q**((3-N)/(N-S)) * (A * g_n)**((S-3) / (N-S))) / (4 * np.pi * B_F**(3-S))))) #NOTE:THIS RESULTS IN NAN CURRENTLY
    t_fs_star = np.abs(( ( (3-S) * q**((3-N)/(N-S)) * (A * g_n)**((S-3) / (N-S)) ) / 
                  (4 * np.pi * B_F**(3-S))))**(FUNKYPOWER) * m_csm_th**(FUNKYPOWER)
    #print('t_fs_star', q, m_csm_th, FUNKYPOWER, g_n, t_fs_star)
    return t_fs_star

def calculateT_RS_STAR(v_sn, g_n, q, massOfEjecta):
    t_rs_star = ( ( (v_sn) / ((B_R) * ((A * g_n) / q))**(1/(N-S)) ) * 
                 (1 - ((3-N) * massOfEjecta) / 
                  (4 * np.pi * (v_sn)**(3-N) * g_n))**(1/(3-N)) )**((N-S) / (S-3))
    #print('t_rs_star', (v_sn), ((B_R) * ((A * g_n) / q))**(1/(N-S)), 
    #      (v_sn) / ((B_R) * ((A * g_n) / q))**(1/(N-S)))
    return t_rs_star

def stepFunction(x):
    returnValue = 0
    if x > 0:
        returnValue = 1
    return returnValue

def function_1(t_prime, t_0, t_i, g_n, q, m_csm_th, v_sn, ejectaMass, t_fs_star, t_rs_star):
    # t_0 = calculateT_0(m_csm = 0, r_ph = 0)
    # t_i = calculateT_I(VSN=0, radius_p=0) #NOTE: WE CALCULATED THIS OUTSIDE OF SCOPE (THIS IS TEMPORARY)
    # g_n = calcualteG_N(ESN=0, massOfEjecta=0) #NOTE ESN WAS CALCULATED OUT OF SCOPE #NOTE G_N WAS CALCULATED OUT OF SCOPE  (TEMP)
    # q = calcualteQ(m_csm=0,r_csm=0,radius_p=0) #NOTE q WAS CALCULATED OUT OF SCOPE (TEMP)

    instance = (
        ( (2 * np.pi) / (N - S)**3 ) * g_n**( (5-S) / (N-S) ) * q**( (N-5) / (N-S) ) * (N-3)**2 * (N-5) * B_F**(5-S) *
        A**( (5-S) / (N-S) ) * (t_prime + t_i)**( (2*N + 6 * S - N*S - 15) / (N-S) ) * stepFunction(t_fs_star - t_prime) + 2 * np.pi * ( (A*g_n) / (q) )**( (5-N) / (N-S) ) *
        B_R**(5-N) * g_n * ( (3-S) / (N-S) )**3 * (t_prime + t_i)**( (2*N + 6 * S - N*S - 15) / (N-S) ) * stepFunction(t_rs_star - t_prime)
    )    


    return instance;

#This is where the nickel decay integral goes
def function_2(t_prime, ejectaMass, r_ph, massNI, m_csm_th, t_0_prime):
    #m_csm_th = calculateM_CSM_TH(q=0, r_ph=0,r_p=0) #NOTE: I FORGOT WHAT R_PH IS
    # t_0_prime = (K * (ejectaMass + m_csm_th)) / (BETA * SPEED_OF_LIGHT * r_ph) #NOTE NEED R_PH TO CALCULATE

    instance = (
        np.exp( (t_prime) / (t_0_prime) ) * massNI * ( (3.9e10 - 6.8e9) * np.exp((-t_prime) / (8.8 * 86400)) + 6.8e9 * np.exp((-t_prime) / (111.3 * 86400)) )

    )

    return instance

def returnCSMLuminosity(t, ejectaMass, v_sn, massNI, massCSM, r_p, csm_radius, esn, g_n, q, r_ph, m_csm_th, t_0, t_0_prime, t_fs_star, t_rs_star):
    
    #q = calcualteQ(massCSM, csm_radius, r_p)
    #r_ph = calculateR_ph(q, csm_radius)
    #m_csm_th = calculateM_CSM_TH(q, r_ph, r_p) # This is calculated out of scope 

    #t_0 = calculateT_0(m_csm_th,r_ph) # This is calculated out of scope 
    #t_0_prime = (K * (ejectaMass + m_csm_th)) / (BETA * SPEED_OF_LIGHT * r_ph) # This is calculated out of scope ! 

    t = t * 86400 #Converting t to CSM so we do not have to worry about conversion beyond this point

    x_prime = np.linspace(0, t, 100)
    #We need a list for each integral (2 total lists)
    #List 1
    list_1 = np.array([np.exp(t_prime / t_0) * 
                       function_1(t_prime, t_0, t_0_prime, g_n, q, 
                                  m_csm_th, v_sn, ejectaMass, t_fs_star, t_rs_star) 
                                  for t_prime in x_prime])
    list_2 = np.array([np.exp(t_prime / t_0_prime) * 
                       function_2(t_prime, ejectaMass, r_ph, 
                                  massNI, m_csm_th, t_0_prime) 
                                  for t_prime in x_prime])
    #print(m_csm_th, calculateT_FS_STAR(q, m_csm_th, g_n) / 86400, 
    #      calculateT_RS_STAR(v_sn, g_n, q, ejectaMass) / 86400)
    integral_1 = simpson(x_prime, list_1)
    integral_2 = simpson(x_prime, list_2)

    part_1 = (1 / t_0) * np.exp((-t) / t_0) * integral_1
    part_2 = ( ( 1/t_0_prime) * np.exp( (-(t) / (t_0_prime) ) ) ) * integral_2

    #print(part_1, part_2)
    luminosity = part_1 + part_2

    return luminosity


#x_list = np.linspace(1,200,398)
#x_list = [20,40] 
x_list = np.linspace(1,200,398)

#These are temporary representing the inevitable inputs (I am acting as if I had the inputs right now)
# ejectaMass = 0
# v_sn = 0
# massNI = 0  
# massCSM = 0
# r_p = 0
# radiusCSM = 0

#These need to be converted first
ejectaMass = [12] 
v_sn = [calculateVSN(1e51, (12 * 1.989e33))]
massNI = [0.08]
massCSM = [1]
r_p = [1.0e12]
radiusCSM = [6.59e14]

# Conversions
for i in range(len(ejectaMass)):
    ejectaMass[i] = ejectaMass[i] * 1.989e33
# for j in range(len(v_sn)):
#     v_sn[j] = v_sn[j] * 100000
for k in range(len(massCSM)):
    massCSM[k] = massCSM[k] * 1.989e33
for l in range(len(massNI)):
    massNI[l] = massNI[l] * 1.989e33

#Radius values do not need to be converted as they are already in CGM

# calculateT_FS_STAR(q, m_csm_th, g_n) - t_prime
# calculateT_RS_STAR(v_sn, g_n, q, ejectaMass)


#TODO: SUMMARY WE NEED TO FIGURE OUT WHAT R_PH IS AND ALL THE VARIABLES WILL COME TOGETHER THEN FIGURE OUT WHAT TO SEND TO FUNCTIONS TO CALCULATE
#NOTE 5 MINUTES OF WORK!!!

for e_mass in range(len(ejectaMass)):
    for vel_sn in range(len(v_sn)):
        esn = calcualteESN(v_sn[vel_sn], ejectaMass[e_mass]) #TODO: THIS NEEDS TO BE PASSED INTO THE RETURNCSM FUNCTION
        g_n = calcualteG_N(esn, ejectaMass[e_mass]) #TODO: THIS NEEDS TO BE PASSED INTO RETURNCSM FUNCTION
        for ni_mass in range(len(massNI)):
            for csm_mass in range(len(massCSM)):
                for radius_p in range(len(r_p)):
                    t_initial = calculateT_I(v_sn[vel_sn], r_p[radius_p])
                    for csm_radius in range(len(radiusCSM)):
                        #Calculating these these for the 1 time I want to run it (better than calling it when we need it) 
                        #TODO: WE NEED TO PASS THESE TO THE returnCSMLuminosity FUNCTION STILL 
                        q = calcualteQ(massCSM[csm_mass], radiusCSM[csm_radius], r_p[radius_p])
                        r_ph = calculateR_ph(q, radiusCSM[csm_radius])
                        m_csm_th = calculateM_CSM_TH(q, r_ph, r_p[radius_p])
                        t_0 = calculateT_0(m_csm_th, r_ph)
                        t_0_prime = (K * (ejectaMass[e_mass] + m_csm_th)) / (BETA * SPEED_OF_LIGHT * r_ph) 
                        t_fs_star = calculateT_FS_STAR(q, m_csm_th, g_n)
                        t_rs_star = calculateT_RS_STAR(v_sn[vel_sn], g_n, q, ejectaMass[e_mass])


                        y_list = np.array([returnCSMLuminosity(t, ejectaMass[e_mass], v_sn[vel_sn], massNI[ni_mass], 
                                                               massCSM[csm_mass], r_p[radius_p], radiusCSM[csm_radius], 
                                                               esn, g_n, q, r_ph, m_csm_th, t_0, t_0_prime, t_fs_star, t_rs_star) for t in x_list])
                        
                        # We know x_list and y_list should be of the same length

                        filename = "temporaryName.data" # TODO: Dyanimc file naming has to be done

                        file = open(filename, "w") #File is opened

                        for m, (first, second) in enumerate(zip(x_list, y_list)):
                            file.write(str("{:3.1f}".format(first)) + "    " + str("{:.5e}".format(second)) + '\n')


                        file.close() #File is closed


                        # TODO: All I want to add now is a output thing to show off what is being done





#NOTE: All I need is to verify what values are being passed in and what 
#      to copy from the nickel decay model. It seems like a lot but I believe it really isn't

# This is bogus for not bull I'll just have it commented out.
fig, ax = plt.subplots()
ax.plot(x_list, y_list,
        linestyle = '-',
        color = 'black',
        linewidth = 2)

ax.set_title('Luminosity ( L(t) ) vs. Time (Days)')
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Luminosity ( L(t) )')

#Displays the plot
plt.show()
#plt.savefig("temp.png")

