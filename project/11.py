import wx
import wx.xrc
import wx.adv
import dlib
import numpy as np
import face_recognition
from scipy.spatial import distance as dist
import cv2
import os
import time
from imutils import face_utils
encoding_list=[]
name_list=[]
name=None
# for root ,dirs,files in os.walk("facedata"):
#     for file in files:
#         img=face_recognition.load_image_file(os.path.join(root,file))
#         encoding=face_recognition.face_encodings(img)[0]
#         encoding_list.append(encoding)
#         name_list.append(os.path.splitext(file)[0])
###########################################################################
## Class MyFrame1
###########################################################################
COVER = 'C:\\Users\\Xs\\Desktop\\project\\camera.png'
PREDICTOR_PATH = "C:\\Users\\Xs\\Desktop\\project\\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


# COVER ='D:/360MoveData/Users/LYJ/Desktop/1.jpg'
class MyFrame1 ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "驾驶疲劳检测系统", pos = wx.DefaultPosition, size = wx.Size( 650,691 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_animCtrl1 = wx.adv.AnimationCtrl( self, wx.ID_ANY, wx.adv.NullAnimation, wx.DefaultPosition, wx.DefaultSize, wx.adv.AC_DEFAULT_STYLE )
        bSizer1.Add( self.m_animCtrl1, 3, wx.ALL|wx.EXPAND, 5 )
        
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"操作板" ), wx.VERTICAL )
        
        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
        
        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"视频开关" ), wx.VERTICAL )
        
        gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.m_button3 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"打开摄像头,开始行车", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_button3, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button4 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"关闭摄像头，停止行车", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_button4, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button31 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"人脸库加载", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_button31, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_button41 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"驾驶员识别", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_button41, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        sbSizer2.Add( gSizer2, 1, wx.EXPAND, 10 )
        
        
        gSizer1.Add( sbSizer2, 1, wx.EXPAND, 5 )
        
        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"驾驶员状态" ), wx.VERTICAL )
        
        self.m_textCtrl2 = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        sbSizer4.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 1 )
        
        
        gSizer1.Add( sbSizer4, 1, wx.EXPAND, 1 )
        
        
        sbSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( sbSizer1, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
          
          		# Connect Events
        self.m_button3.Bind( wx.EVT_BUTTON, self.Camera_on )
        self.m_button4.Bind( wx.EVT_BUTTON, self.off )
        self.m_button31.Bind( wx.EVT_BUTTON, self.face_data )
        self.m_button41.Bind( wx.EVT_BUTTON, self.face_find )
        self.image_cover = wx.Image(COVER, wx.BITMAP_TYPE_ANY)
        self.bmp = wx.StaticBitmap(self.m_animCtrl1, -1, wx.Bitmap(self.image_cover))
        """计数"""
        self.name="None"
        self.eCOUNTER = 0
        self.TOTAL = 0
        self.mCOUNTER = 0
        self.mTOTAL = 0
        self.hCOUNTER = 0
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("C:\\Users\\Xs\\Desktop\\project\\shape_predictor_68_face_landmarks.dat")
        self.m_textCtrl2.AppendText(u"加载模型成功!!!\n")
    def face_data( self, event ):
        for root ,dirs,files in os.walk("C:\\Users\\Xs\\Desktop\\project\\facedata"):
            for file in files:
                img=face_recognition.load_image_file(os.path.join(root,file))
                encoding=face_recognition.face_encodings(img)[0]
                encoding_list.append(encoding)
                name_list.append(os.path.splitext(file)[0])
        print(name_list)
        self.m_textCtrl2.AppendText(u"人脸库加载成功!!!\n")
                
    def face_find_1( self, event ):
        self.name="None"
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened()==True:
            self.CAMERA_STYLE = True
            self.m_textCtrl2.AppendText(u"打开摄像头成功!!!\n")
        else:
            self.m_textCtrl2.AppendText(u"摄像头打开失败!!!\n")
        while(self.cap.isOpened()):
            flag, im_rd = self.cap.read()
            test_locations=face_recognition.face_locations(im_rd)
            test_encodings=face_recognition.face_encodings(im_rd,test_locations)
            face_name=[]
            face_score=[]
            for face_encoding in test_encodings:
                face_distances=face_recognition.face_distance(encoding_list,face_encoding)
                best_index=np.argmin(face_distances)
                if face_distances[best_index]<=0.55:
                    face_name.append(name_list[best_index])
                else:
                    face_name.append("unknown")
                face_score.append(face_distances[best_index])
            for i,(top,right,bottom,left)in enumerate(test_locations):
                self.name=face_name[i]
                score=face_score[i]
                cv2.rectangle(im_rd,(left,top),(right,bottom),(0,0,255),2)
                cv2.rectangle(im_rd,(left,bottom),(right,bottom+50),(0,0,255),cv2.FILLED)        
                cv2.putText(im_rd,self.name,(left+6,bottom+25),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),1)
                cv2.putText(im_rd,"{:.2f}".format(score),(left+6,bottom+45),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
            height,width = im_rd.shape[:2]
            image1 = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(width,height,image1)
            self.bmp.SetBitmap(pic)
            if self.name=="None":
                self.m_textCtrl2.AppendText(u"没有人脸!!!\n")
            else:
                if self.name =='unknown':
                    self.m_textCtrl2.AppendText(u"你不在人脸库中!!!\n")
                else:
                    self.m_textCtrl2.AppendText(u"识别成功，驾驶员"+self.name+"!!!\n")
                    self.cap.release()
                    self.bmp.SetBitmap(wx.Bitmap(self.image_cover))
    def __del__( self ):
        pass
	# Virtual event handlers, overide them in your derived class
    def eye_ratio(self,eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    def mouth_ratio(self,mouth):
        A = np.linalg.norm(mouth[2] - mouth[10])
        B = np.linalg.norm(mouth[4] - mouth[8])
        C = np.linalg.norm(mouth[0] - mouth[6])
        mar = (A + B) / (2.0 * C)
        return mar
    def face( self, event ):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened()==True:
            self.CAMERA_STYLE = True
            self.m_textCtrl2.AppendText(u"打开摄像头成功!!!\n")
        else:
            self.m_textCtrl2.AppendText(u"摄像头打开失败!!!\n")
        if (self.name=="None" or self.name=="unknown"):
            self.m_textCtrl2.AppendText(u"开始行车，驾驶员现处于未识别状态!!!\n")
        else:
            self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"驾驶员"+self.name+"开始行车\n")
        while(self.cap.isOpened()):
            flag, im_rd = self.cap.read()
            img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
            faces = self.detector(img_gray, 0)
            if(len(faces)!=0):
                for k, d in enumerate(faces):
                    cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255),1)
                    shape = self.predictor(im_rd, d)
                    for i in range(68):
                        cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                    shape = face_utils.shape_to_np(shape)
                    mouth = shape[48:68]        
                    mar = self.mouth_ratio(mouth)
                    mouthHull = cv2.convexHull(mouth)
                    cv2.drawContours(im_rd, [mouthHull], -1, (0, 255, 0), 1)    
                    if mar > 1:
                        self.mCOUNTER += 1
                    else:
                        if self.mCOUNTER > 10:
                            self.mTOTAL += 1
                            cv2.putText(im_rd, "Yawning!", (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            if (self.name=="None" or self.name=="unknown"):
                                self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"未知驾驶员打哈欠\n")
                            else:
                                self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"驾驶员"+self.name+"打哈欠了\n")
                            self.mCOUNTER = 0
                        else:
                            self.mCOUNTER = 0
                    cv2.putText(im_rd, "COUNTER: {}".format(self.mCOUNTER), (150, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
                    cv2.putText(im_rd, "MAR: {:.2f}".format(mar), (300, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(im_rd, "Yawn: {}".format(self.mTOTAL), (450, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

                    leftEye = shape[36:42]
                    rightEye = shape[42:48]
                    leftEAR = self.eye_ratio(leftEye)
                    rightEAR = self.eye_ratio(rightEye)
                    ear = (leftEAR + rightEAR) / 2.0
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(im_rd, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(im_rd, [rightEyeHull], -1, (0, 255, 0), 1)
                    if ear < 0.2:
                        self.eCOUNTER += 1
                    else:
                        if self.eCOUNTER > 15:
                            self.TOTAL += 1
                            if (self.name=="None" or self.name=="unknown"):
                                self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"未知驾驶员闭眼了\n")
                            else:
                                self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"驾驶员"+self.name+"闭眼了\n")
                            self.eCOUNTER = 0
                        else:
                            self.eCOUNTER = 0
                    cv2.putText(im_rd, "driver:", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
                    if (self.name=="None" or self.name=="unknown"):
                        cv2.putText(im_rd, "unknown", (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
                    else:
                        cv2.putText(im_rd, self.name, (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
                    cv2.putText(im_rd, "ECOUNTER: {}".format(self.eCOUNTER), (150, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
                    cv2.putText(im_rd, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(im_rd, "SHUT-EYES: {}".format(self.TOTAL), (450, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
                    if (self.TOTAL+self.mTOTAL)>=3:
                        self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"驾驶员疲劳警告，播放警铃！！！！！\n")
                        os.system('C:\\Users\\Xs\\Desktop\\project\\22.mp3')
                        self.TOTAL=0
                        self.mTOTAL=0
            height,width = im_rd.shape[:2]
            image1 = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(width,height,image1)
            self.bmp.SetBitmap(pic)
        self.cap.release()
        
    def Camera_on(self,event):
        import _thread
        _thread.start_new_thread(self.face, (event,))
    def face_find(self,event):
        import _thread
        _thread.start_new_thread(self.face_find_1, (event,))
    def off( self, event ):
        self.cap.release()
        if (self.name=="None" or self.name=="unknown"):
            self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"停止行车，驾驶员未知!!!\n")
        else:
            self.m_textCtrl2.AppendText(time.strftime('%Y-%m-%d %H:%M ', time.localtime())+u"驾驶员"+self.name+"停止行车\n")
        self.bmp.SetBitmap(wx.Bitmap(self.image_cover))
        self.TOTAL=0
        self.mTOTAL=0
        event.Skip()
class main_app(wx.App):
    # OnInit 方法在主事件循环开始前被wxPython系统调用，是wxpython独有的
    def OnInit(self):
        self.frame = MyFrame1(parent=None)
        self.frame.Show(True)
        return True   

    
if __name__ == "__main__":
    app = main_app()
    app.MainLoop()