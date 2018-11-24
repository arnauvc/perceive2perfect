import cv2
import numpy as np

INF = 1000000


POSE_PAIRS_ORIGINAL = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9], [9, 10], [14, 11], [11, 12], [12, 13]]
# Connected nodes information to check
POSE_PAIRS = [[8, 9], [11, 12], [9, 10], [12, 13], [1, 14], [2, 3], [5, 6], [3, 4], [6, 7], [0, 1]]

# Messages acording to area
messages = {0: "Move your head",
            2: "Move your right elbow",
            3: "Move your right hand",
            5: "Move your left elbow", 
            6: "Move your left hand",
            1: "Move your brust",
            8: "Move your right knee",
            9: "Move your right feet",
            11: "Move your left knee",
            12: "Move your left feet"}

# 0
points_1 = [(205, 93), (205, 160), (166, 160), (146, 93), (195, 40), (244, 174), (273, 93), (225, 40), (185, 334), (195, 441), (215, 549), (234, 321), (332, 374), (225, 374), (205, 254)]

# Aleix
points_2 = [(208, 73), (208, 125), (166, 125), (153, 83), (194, 41), (236, 125), (250, 83), (208, 41), (194, 229), (222, 333), (236, 406), (236, 219), (306, 250), (250, 313), (208, 177)]

# 1
#points_1 = [(205, 182), (205, 243), (171, 259), (182, 182), (194, 106), (240, 259), (240, 182), (217, 121), (194, 396), (205, 487), (228, 579), (251, 380), (331, 426), (240, 426), (217, 320)]

# 3
#points_2 = [(146, 110), (146, 165), (124, 187), (139, 110), (139, 66), (176, 176), (169, 110), (154, 66), (139, 286), (146, 374), (154, 451), (176, 275), (235, 319), (169, 308), (154, 231)]


frame = cv2.imread("./images/vrkasana1.jpg")
frameCopy = np.copy(frame)
frameWidth = frame.shape[1]
frameHeight = frame.shape[0]
threshold = 0.1
cv2.circle(frame, (200,300), 400, (255, 255, 255), thickness=-1, lineType=cv2.FILLED)

corrections = {}
directions = {}

# Calculate diferences in inclination for all connections
for pair in POSE_PAIRS:
    partA = pair[0]
    partB = pair[1]

    if points_1[partA] and points_1[partB] and points_2[partA] and points_2[partB]:
        deltaY_1 = (points_1[partA][0] - points_1[partB][0])
        if (abs(deltaY_1) > 0.0000005) :
            incl_1 = (points_1[partA][1] - points_1[partB][1]) / deltaY_1
        else:
            incl_1 = INF
        deltaY_2 = (points_2[partA][0] - points_2[partB][0])
        if (abs(deltaY_2) > 0.0000005) :
            incl_2 = (points_2[partA][1] - points_2[partB][1]) / deltaY_2
        else:
            incl_2 = INF
            
        if (incl_1 != 0):
            diff = abs((incl_1 - incl_2)/incl_1)
        else: 
            diff = abs(incl_1 - incl_2)
            
        #print(diff)
        if partA == 8 or partA == 11:
            thr = 0.8
        else:
            thr = 0.5
        if diff > thr:
            print("Massa diferent en el punt ", partA, " : ", partB )
            if diff > 1:
                corrections[partA] = 2
            else:
                corrections[partA] = 1
            directions[partA] = "to the left."
            # separar casos de cos i cap dels altres i mirar l angle de les pendents per saber cap on pivotar respecte del que pivota
        else:
            corrections[partA] = 0
        

        # PRINT CHIVATO #  
        pA0 = points_1[partA][0] + points_2[14][0] - points_1[14][0]
        pA1 = points_1[partA][1] + points_2[14][1] - points_1[14][1]
        pB0 = points_1[partB][0] + points_2[14][0] - points_1[14][0]
        pB1 = points_1[partB][1] + points_2[14][1] - points_1[14][1]
            
        cv2.line(frame, (pA0, pA1), (pB0, pB1), (40, 40, 200), 2)
        cv2.circle(frame, (pA0, pA1), 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        
        cv2.line(frame, points_2[partA], points_2[partB], (40, 200, 40), 2)
        cv2.circle(frame, points_2[partA], 8, (0, 255, 0), thickness=-1, lineType=cv2.FILLED)
     
        
cv2.imshow('Output-Skeleton', frame)
cv2.imwrite('Output-Skeleton-C.jpg', frame)
            
cv2.waitKey(1)
            
            
for key in corrections:
    if corrections[key] != 0:
        if corrections[key] == 1:
            print(messages[key], "a little", " to the ?.")
        else:
            print(messages[key], " to the ?.")
    #print(key, " has level ", corrections[key], " and message ", messages[key])
    
