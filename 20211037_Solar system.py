import cv2
import numpy as np

def deg2rad(degree):
    rad = degree * np.pi / 180.0
    return rad

def getRegularNgon(ngon):
    vertices = []
    delta = 360.0/ngon
    for i in range(ngon):
        degree = delta * i
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        vertices.append((x,y))
        
    vertices = np.array(vertices)    
    return vertices
    
def getline(canvas,x0,y0,x1,y1,color):
    # |기울기|<1 --> y =  (x-x0) * (y1-y0) / (x1-x0) +y0
    # |기울기|>1 --> x = (y-y0) * (x1-x0)/(y1-y0) +x0
    if(abs(x1-x0)<abs(y1-y0)): #|기울기|>1인 경우
        if(y1==y0):
            y = y0
            if(x0<x1):
                for x in range(x0,x1+1):
                    canvas[int(y),int(x)] = color
            else:
                for x in range(x0,x1-1,-1):
                    canvas[int(y),int(x)] = color
        else:
            if(y0<y1):
                for y in range(y0,y1+1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    x = (y-y0) * (x1-x0)/(y1-y0) +x0
                    canvas[int(y),int(x)] = color
   
    else:#|기울기|<=1인 경우
        if(x1==x0):
            x = x0
            if(y0<y1):
                for y in range(y0,y1+1):
                    canvas[int(y),int(x)] = color
            else:
                for y in range(y0,y1-1,-1):
                    canvas[int(y),int(x)] = color
        
        else:
            if(x0<x1):
                for x in range(x0,x1+1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
                    
            else:
                for x in range(x0,x1-1,-1):
                    y =  (x-x0) * (y1-y0) / (x1-x0) +y0
                    canvas[int(y),int(x)] = color
    
def getCenter(pts):
    center = np.array([[0.0,0.0]])
    for p in pts:
        center+=p
        
    center = center / pts.shape[0]
    center = center.astype('int')
    
    return center
    
        
def drawPolygon(canvas,pts,color,axis=False):
    num = pts.shape[0]
    for i in range(num-1):
        getline(canvas,pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1],color)   
    
    

          
def makeTmat(a,b):
    T = np.eye(3,3)
    T[0,2] = a
    T[1,2] = b
    return T
    
def makeRmat(deg):
    R = np.eye(3,3)
    radian = deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R[0,0] = c
    R[0,1] = -s
    R[1,0] = s
    R[1,1] = c
    return R

def ctoc(canvas,p1,p2):
    c1 = getCenter(p1)
    c2 = getCenter(p2) 
    
    getline(canvas, c1[0,0],c1[0,1], c2[0,0],c2[0,1], color=(255, 128, 128))
    
def draw_diag(canvas,polygon,axis=False):
    num = polygon.shape[0] #몇각형인지 //5각형이면 5
    for i in range(num): #0-4
        for count in range(num):
            if(2<=abs(i-count)<num-1):
                getline(canvas,polygon[count,0],polygon[count,1],polygon[i,0],polygon[i,1],color=(255, 255, 255))
    if axis==True:
        Center = getCenter(polygon)
        getline(canvas, Center[0,0],Center[0,1], polygon[0,0],polygon[0,1], color=(255, 128, 128))             
       
def cvtto3mat(Mat,ngon):
    l = np.ones(ngon)
    Mat = np.append(Mat,[l],axis=0) 
    return Mat     

def rettomat(Mat):
    Mat = np.delete(Mat,2,axis=0)   
    Mat = Mat.T     
    Mat = Mat.astype('int')
    return Mat
   
def main():
    width,height = 1200,1000
    color = (255,255,255)
    v_rot,v_rev=0,0
    e_rot,e_rev=0,0
    s_rot,s_rev=0,0
    m_rot=0
    r_rot=0
    while True:
        canvas = np.zeros((height,width,3),dtype='uint8')
        ngon=100
        P = getRegularNgon(ngon)
        Sun_p = P.copy()
        Sun_p*=100
        Sun_p = Sun_p.T
        Venus_p = Sun_p.copy()
        Earth_p = Sun_p.copy()
        Moon_p = Sun_p.copy()
        Saturn_P = Sun_p.copy()
        Smoon_P = Sun_p.copy()
        Venus_p /=3.5
        Earth_p/=3
        Moon_p /=4
        Saturn_P /= 2
        Smoon_P /=4
        Sun_p = cvtto3mat(Sun_p,ngon)
        Venus_p = cvtto3mat(Venus_p,ngon)
        Earth_p = cvtto3mat(Earth_p,ngon)
        Moon_p = cvtto3mat(Moon_p,ngon)
        Saturn_P = cvtto3mat(Saturn_P,ngon)
        Smoon_P = cvtto3mat(Smoon_P,ngon)
        
        Sun = makeTmat(530,400) @ Sun_p
        Sun = rettomat(Sun)
        drawPolygon(canvas,Sun,(0,0,255))
        
        Venus = makeTmat(530,400)@ makeRmat(-(v_rev)) @ makeTmat(160,0) @ makeRmat(v_rot)@Venus_p
        Venus = rettomat(Venus)
        drawPolygon(canvas,Venus,(0,255,255),axis=True)
    
        Earth = makeTmat(530,400)@ makeRmat(e_rev) @ makeTmat(260,0)@ makeRmat(e_rot) @Earth_p
        Earth = rettomat(Earth)

        Moon = makeTmat(530,400)@ makeRmat(e_rev) @ makeTmat(260,0)@ makeRmat(e_rot) @makeRmat(m_rot)@makeTmat(100,0)@makeRmat(m_rot)@Moon_p
        Moon = rettomat(Moon)
        
        drawPolygon(canvas,Earth,(255,255,0),axis=True)
        drawPolygon(canvas,Moon,color,axis=True)
        ctoc(canvas,Earth,Moon)

        Saturn = makeTmat(530,400)@ makeRmat(-(s_rev)) @ makeTmat(400,0) @ makeRmat(s_rot)@Saturn_P
        Saturn = rettomat(Saturn)
        
        Smoon = makeTmat(530,400)@ makeRmat(-(s_rev)) @ makeTmat(400,0)@ makeRmat(s_rot) @makeRmat(m_rot)@makeTmat(90,0)@makeRmat(m_rot)@Smoon_P
        Smoon = rettomat(Smoon)
        drawPolygon(canvas,Saturn,color,axis=True)
        drawPolygon(canvas,Smoon,color,axis=True)
        ctoc(canvas,Saturn,Smoon)
        
        cv2.imshow("myWindow",canvas)
        if cv2.waitKey(20) == 27:
            break
        
        v_rev+=5
        v_rot+=2
        e_rev+=3
        e_rot+=5
        m_rot+=1
        s_rev+=0.1
        s_rot+=9
if __name__ =="__main__":
    main()