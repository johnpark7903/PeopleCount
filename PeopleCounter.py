##from picamera.array import PiRGBArray
##from picamera import PiCamera
import numpy as np
import cv2 as cv
import Person
import time

try:
    log = open('log.txt',"w")
except:
    print("Cannot open log file")

#지나가는 사람 숫자를 담을 변수를 선언한다.
cnt_up   = 0
cnt_down = 0
cnt_left = 0
cnt_right = 0

#영상을 연다.

#cap = cv.VideoCapture(0)
#cap = cv.VideoCapture('Test Files/TestVideo.avi')
cap = cv.VideoCapture('Test Files/walking.avi')

#print("cap type",type(cap))
#print("cap", cap)
#camera = PiCamera()
##camera.resolution = (160,120)
##camera.framerate = 5
##rawCapture = PiRGBArray(camera, size=(160,120))
##time.sleep(0.1)

#Propiedades del video
#Video Properties

##cap.set(3,160) #Width
##cap.set(4,120) #Height

#Imprime las propiedades de captura a consola
#Print capture properties to console
for i in range(19):
    print( i, cap.get(i))

#가로 세로 크기의 정보를 담는다.
h = 480
w = 640
frameArea = h*w
areaTH = frameArea/250
print( 'Area Threshold', areaTH)

#총 4개의 선을 그린다.

line_up = int(2*(h/20))
line_down = int(18*(h/20))
line_left = int(2*(w/20))
line_right = int(18*(w/20))

up_limit = int(1*(h/20))
down_limit = int(19*(h/20))
left_limit = int(1*(w/20))
right_limit = int(19*(w/20))

print( "Blue line y:",str(line_down))
print( "Red line y:", str(line_up))
line_down_color = (255,0,0)
line_up_color = (0,0,255)

pt1 =  [0, line_down];
pt2 =  [w, line_down];
print("pt1 pt2", pt1, pt2)

pts_L1 = np.array([pt1,pt2], np.int32)
print("pts_L1", pts_L1)
pts_L1 = pts_L1.reshape((-1,1,2))
print("pts_L1", pts_L1, pts_L1.shape)

pt3 =  [0, line_up];
pt4 =  [w, line_up];
print("pt3 pt4", pt3, pt4)

pts_L2 = np.array([pt3,pt4], np.int32)
print("pts_L2", pts_L2)
pts_L2 = pts_L2.reshape((-1,1,2))
print("pts_L2", pts_L2, pts_L2.shape)

pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))



pt9 =  [line_left, 0];
pt10 =  [line_left, h];
pts_L5 = np.array([pt9,pt10], np.int32)
pts_L5 = pts_L5.reshape((-1,1,2))

pt11 =  [line_right, 0];
pt12 =  [line_right, h];
pts_L6 = np.array([pt11,pt12], np.int32)
pts_L6 = pts_L6.reshape((-1,1,2))

pt13 =  [left_limit, 0];
pt14 =  [left_limit, h];
pts_L7 = np.array([pt13,pt14], np.int32)
pts_L7 = pts_L7.reshape((-1,1,2))

pt15 =  [right_limit, 0];
pt16 =  [right_limit, h];
pts_L8 = np.array([pt15,pt16], np.int32)
pts_L8 = pts_L8.reshape((-1,1,2))




#배경을 분리하여 사람을 추출하여 fgbg에 담는다.
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

#마스크 생성 오프닝 클로징에 사용할 커널의 크기를 정의한다.
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#그외 폰트, 사람객체를 담을 리스트, 최대 age 및 pid 변수선언
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 30
pid = 1

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame = cv.resize(frame, (640, 480))

##  frame = image.array

    for i in persons:
        i.age_one() #age every person one frame
        # j = i.age_one()
        # person [<Person.MyPerson object at 0x000001ECE684D5D0>]
        # print("person", persons)

    #배경을 분리한 마스크를 생성한다.
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #이진화를 진행한다.
    try:
        ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
        ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)

        #cv.imshow('imBin', imBin)
        #cv.imshow('imBin2', imBin2)
        #Opening (erode->dilate) para quitar ruido.
        #Opening (erode->dilate) to remove noise.
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regiones blancas.
        #Closing (dilate -> erode) to close white regions.
        mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print( 'UP:',cnt_up)
        print ('DOWN:',cnt_down)
        print('LEFT:', cnt_left)
        print('RIGHT:', cnt_right)
        break
    #################
    #   컨투어   #
    #################
    
    # 컨투어를 추출한다.
    contours0, hierarchy = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt) #컨투어를 area에 담고 미리 선언한 유효area 쓰레싱과 비교하여 클 경우에만 감지 및 추적한다.
        if area > areaTH:
            #################
            #   추적 트래킹    #
            #################
            
            #여러 사람 탐지 및 출구와 입구 지정
            
            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit): #최대 구역 사이에서만 cy 무게중심 좌표를 선정한다.

                for i in persons: #persons 에 담긴 객체 하나하나에 대해 값을 도출한다.처음일 경우 아직 담긴 객체가 없으므로 그냥 넘어간다.
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:

                        #컨투어의 x값에 객체의 x값을 뺀 후 w너비값과 비교하여 작거나 같고 높이도 작거나 같을 경우에는 new = False 를 넣어서 기존의 객체임을 플래그에 담는다.
                        #그런데 x의 값이 w보다 높을 수는 없다. 그러면 x - 객체의 x값은 항상 w보다 낮은게 아닌가?
                        #여기서는 w는 객체의 w구나. w보다 그 차가 커지는 경우라면 객체의 x 값이 매우 큰차이가 나는 경우이다.그럼 왜 w를 기준으로 하는것을까?
                        #The object is close to one that was detected before
                        # p = Person.MyPerson(pid, cx, cy, max_p_age)
                        # persons.append(p)
                        # pid += 1 이걸로 객체를 생성하여 persons 리스트에 추가하게 된다.
                        new = False #움직임이 허용범위 이내일 경우 기존객체라는 것을 표시하고 객체의 무게중심을 업데이트하고, age를 리셋한다.
                        i.updateCoords(cx,cy)   #기존의 xy값은 track 리스트에 추가하고, x,y에 cx,cy를 넣는다.actualiza coordenadas en el objeto and resets age
                        if i.going_UP(line_down,line_up) == True: #이미 정보가 2개 이상 들어가 있을 경우는 cnt_up을 1증가시키고
                            cnt_up += 1;
                            print( "ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                            print("trackUp", len(i.tracks), i.tracks)
                            log.write("ID: "+str(i.getId())+' crossed going up at ' + time.strftime("%c") + '\n')
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1;
                            print( "ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                            print("trackDown", len(i.tracks), i.tracks)
                            log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                        elif i.going_LEFT(line_left,line_right) == True:
                            cnt_left += 1;
                            print( "ID:",i.getId(),'crossed going left at',time.strftime("%c"))
                            print("trackDown", len(i.tracks), i.tracks)
                            log.write("ID: " + str(i.getId()) + ' crossed going left at ' + time.strftime("%c") + '\n')
                        elif i.going_RIGHT(line_left,line_right) == True:
                            cnt_right += 1;
                            print( "ID:",i.getId(),'crossed going right at',time.strftime("%c"))
                            print("trackDown", len(i.tracks), i.tracks)
                            log.write("ID: " + str(i.getId()) + ' crossed going right at ' + time.strftime("%c") + '\n')
                        break
                    if i.getState() == '1': #State의 값이 1일 경우, Dir의 값이 down이고 y의 값이 최대하한선보다 클 경우에 done에 true를 설정
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit: #dir 값이 up이고 y의 값이 최대 상한선 보다 작을 경우 done=True로 설정
                            i.setDone()
                        elif i.getDir() == 'left' and i.getX() < left_limit: #dir 값이 up이고 y의 값이 최대 상한선 보다 작을 경우 done=True로 설정
                            i.setDone()
                        elif i.getDir() == 'right' and i.getX() < right_limit: #dir 값이 up이고 y의 값이 최대 상한선 보다 작을 경우 done=True로 설정
                            i.setDone()

                    if i.timedOut(): #done 이 true일 경우 리스트에서, 객체를 제거한다.
                        #remove i from the persons list
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #liberar la memoria de i #free i memory
                if new == True: #만약에 새로운 객체가 탐지 된 경우, 객체를 MyPerson 클래스로 만들어서 persons 리스트에 넣은 후 pid값을 1증가시킨다.
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1

            #################
            #   DIBUJOS     #
            #################
            cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv.drawContours(frame, cnt, -1, (0,255,0), 3)
            
    #END for cnt in contours0
            
    #########################
    # DIBUJAR TRAYECTORIAS  #
    #   DRAW PATHS          #
    #########################
    for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1,1,2))
##            frame = cv.polylines(frame,[pts],False,i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,1,i.getRGB(),1,cv.LINE_AA)
        
    #마무리 부분으로 선을 그리고 카운팅등 정보 표시하기.
    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    str_left = 'LEFT: ' + str(cnt_left)
    str_right = 'RIGHT: ' + str(cnt_right)
    frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame, [pts_L5], False, line_down_color, thickness=2)
    frame = cv.polylines(frame, [pts_L6], False, line_up_color, thickness=2)
    frame = cv.polylines(frame, [pts_L7], False, (255, 255, 255), thickness=1)
    frame = cv.polylines(frame, [pts_L8], False, (255, 255, 255), thickness=1)

    cv.putText(frame, str_up ,(10,40),font,1,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_up ,(10,40),font,1,(0,0,255),1,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,1,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,1,(255,0,0),1,cv.LINE_AA)
    cv.putText(frame, str_left, (10, 140), font, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str_left, (10, 140), font, 1, (0, 0, 255), 1, cv.LINE_AA)
    cv.putText(frame, str_right, (10, 190), font, 1, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str_right, (10, 190), font, 1, (255, 0, 0), 1, cv.LINE_AA)

    cv.imshow('Frame',frame)
    cv.imshow('Mask',mask)    

    #print("people num", len(persons))
    #print("pid", pid)
##    rawCapture.truncate(0)
#preisonar ESC para salir
#press ESC to exit
    k = cv.waitKey(20) & 0xff
    if k == 27:
        break
#END while(cap.isOpened())
    
#################
#   LIMPIEZA    #
#   CLEANING    #
#################
log.flush()
log.close()
cap.release()
cv.destroyAllWindows()
