# -*- coding: utf-8 -*-

# Import
import tkFileDialog
import tkMessageBox
from Tkinter import *
from OpenBciCustom import *
import time, threading, os
import json, platform
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Att_feedBack import *

def DefaultTaskOpt():
    opt = dict()    
    opt["sr"] = 250
    opt["tm_base"] = 10 # in secs
    opt["ch_names"] = ["Fp1", "Fp2", "F3", "F4", "F7", "F8", "Cz","Pz"]
    opt["ch_types"] = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg"]
    opt["n_ch"] = 8
    opt["w_win"] = 10 # window width, 10s
    opt["inc_win"] = 1 # step of sliding window, 1s
    opt["inc_update"] = 1 # time interval for updating feedback, 2s

    # att base
    opt["att_base"]=None

    return opt

class CalcThread(threading.Thread):
    def __init__(self, guiObj):
        super(CalcThread, self).__init__()
        self.guiObj=guiObj
        self.is_running=True
        self.running_lock=threading.Lock()

    def run(self):
        guiObj=self.guiObj
        while True:
            # Acquire Lock
            self.running_lock.acquire()
            if not self.is_running: break
            
            # Estimation
            beg_time=time.time()
            if guiObj.readThread.is_record:
                win_array=guiObj.readThread.getWinArray()
                att_base=guiObj.task_opt["att_base"]
                update_att_base=False
                # The first att base
                if att_base is None:
                    att_base=1
                    update_att_base=True
                att=computer(win_array, att_base, guiObj.task_opt)
                print "current att: "
                print att
                # Update att base after the first iteration
                if update_att_base:
                    guiObj.task_opt["att_base"]=att
                guiObj.cognRater.timeCounter(att)

                if att<0.0: showed_att=0.0
                elif att>2.0: showed_att=2.0
                else: showed_att=att
                
                pos=256*(showed_att-0.0)/(2.0-0.0)

                guiObj.attMarker.set_xdata([pos, pos])
                guiObj.attCns.draw()

                hfd=guiObj.cognRater.getRtReport()
                guiObj.hfdStr.set(str(hfd))
                guiObj.hfdEty.update()

                ach=guiObj.cognRater.getStar()
                if ach==0: achImg=guiObj.ach0Img
                elif ach==1: achImg=guiObj.ach1Img
                elif ach==2: achImg=guiObj.ach2Img
                elif ach==3: achImg=guiObj.ach3Img
                elif ach==4: achImg=guiObj.ach4Img
                elif ach==5: achImg=guiObj.ach5Img
                guiObj.achCns["image"]=achImg
                guiObj.achCns.update()

            # Release Lock
            self.running_lock.release()

            end_time=time.time()

            # Waiting
            time.sleep(max([1-(end_time-beg_time), 0]))

    def stop(self): 
        # Acquire Lock
        self.running_lock.acquire()

        # Stop
        self.is_running=False
        
        # Release Lock
        self.running_lock.release()
        
        self.join()

class TaskWindow(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.title('反馈训练')
        if platform.system()=="Windows":
            self.iconbitmap(default='logo.ico')

        task_opt=dict()
        self.task_opt=task_opt

        """
        Input Line
        """
        inputFrm=Frame(self)
        inputFrm.pack(side=TOP, expand=YES, fill=BOTH,
                pady=2)
        # Input Para
        jsfFrm=Frame(inputFrm)
        jsfFrm.pack(side=LEFT, expand=YES, fill=BOTH,
                padx=2)

        jsfLab=Label(jsfFrm, text="被试参数文件：")
        jsfLab.pack(side=LEFT, expand=NO, fill=BOTH)
        self.jsfLab=jsfLab

        jsfStr=StringVar()
        self.jsfStr=jsfStr
        
        jsfEty=Entry(jsfFrm, textvariable=jsfStr)
        jsfEty.pack(side=LEFT, expand=YES, fill=X)
        self.jsfEty=jsfEty 
        
        jsfBtn=Button(jsfFrm, text="加载",
                command=self.openJSON)
        jsfBtn.pack(side=LEFT, expand=YES, fill=BOTH)
        self.jsfBtn=jsfBtn

        # Cognitive Training Target
        cttFrm=Frame(inputFrm)
        cttFrm.pack(side=LEFT, expand=YES, fill=BOTH,
                padx=2)

        cttLab=Label(cttFrm, text="训练目标：")
        cttLab.pack(side=LEFT, expand=NO, fill=BOTH)
        self.cttLab=cttLab

        cttStr=StringVar()
        self.cttStr=cttStr
        
        cttEty=Entry(cttFrm, textvariable=cttStr,
                text=10)
        cttEty.pack(side=LEFT, expand=NO)
        self.cttEty=cttEty 

        perLab=Label(cttFrm, text="%")
        perLab.pack(side=LEFT, expand=NO, fill=BOTH)

        """
        Display Line
        """
        paraFrm=Frame(self)
        paraFrm.pack(side=TOP, expand=YES, fill=X,
                pady=5)
        self.paraFrm=paraFrm

        # Focus Strength
        attFrm=Frame(paraFrm)
        attFrm.pack(side=LEFT, fill=BOTH, padx=2)
        self.attFrm=attFrm

        attLab=Label(attFrm, text="专注力程度：")
        attLab.pack(side=LEFT, fill=BOTH)
        self.attLab=attLab
        
        subAttFrm=Frame(attFrm)
        attFig, attAxe=plt.subplots(figsize=(5, 0.45))
        plt.subplots_adjust(left=0.0, right=1., top=1, bottom=0.0)
        grad=np.linspace(0, 1, 256)
        grad=np.vstack((grad, grad))
        attAxe.imshow(grad, aspect="auto", cmap=plt.get_cmap("rainbow"))
        attAxe.set_axis_off()

        attMarker,=plt.plot([0, 0], [-0.5, 1.5], color="k", linewidth=5)
        attAxe.set_xlim([-1, 256])

        attCns=FigureCanvasTkAgg(attFig, master=subAttFrm)

        attLowLab=Label(subAttFrm, text="低")
        attLowLab.pack(side=LEFT, fill=BOTH)
        attCns.get_tk_widget().pack(side=LEFT, fill=BOTH)
        attHighLab=Label(subAttFrm, text="高")
        attHighLab.pack(side=LEFT, fill=BOTH)

        subAttFrm.pack(side=LEFT, fill=BOTH, padx=1)

        self.attFig=attFig
        self.attAxe=attAxe
        self.attCns=attCns
        self.attMarker=attMarker
        
        # High Focus Duration
        hfdFrm=Frame(paraFrm)
        hfdFrm.pack(side=LEFT, fill=BOTH, padx=2)
        self.hfdFrm=hfdFrm

        hfdLab=Label(hfdFrm, text="持续时间：")
        hfdLab.pack(side=LEFT, fill=BOTH)
        self.hfdLab=hfdLab

        hfdStr=StringVar()
        self.hfdStr=hfdStr
        
        hfdEty=Entry(hfdFrm, textvariable=hfdStr, width=10)
        hfdEty.pack(side=LEFT, fill=X)
        self.hfdEty=hfdEty 

        secLab=Label(hfdFrm, text="Seconds")
        secLab.pack(side=LEFT, fill=BOTH)
        self.secLab=secLab

        # Achievement
        achFrm=Frame(paraFrm)
        achFrm.pack(side=LEFT, fill=BOTH, padx=2)
        self.achFrm=achFrm

        achLab=Label(achFrm, text="专注力水平等级：")
        achLab.pack(side=LEFT, fill=BOTH)
        self.achLab=achLab
        
        ach0Img=PhotoImage(file="ach0.gif")
        ach1Img=PhotoImage(file="ach1.gif")
        ach2Img=PhotoImage(file="ach2.gif")
        ach3Img=PhotoImage(file="ach3.gif")
        ach4Img=PhotoImage(file="ach4.gif")
        ach5Img=PhotoImage(file="ach5.gif")

        achCns=Label(achFrm, image=ach0Img)
        achCns.pack(side=LEFT, fill=BOTH)
        self.achCns=achCns
        self.ach0Img=ach0Img
        self.ach1Img=ach1Img
        self.ach2Img=ach2Img
        self.ach3Img=ach3Img
        self.ach4Img=ach4Img
        self.ach5Img=ach5Img

        # Control Frame
        ctrlFrm=Frame(self)
        ctrlFrm.pack(side=TOP, expand=YES, fill=BOTH,
                pady=5)

        startBtn=Button(ctrlFrm, text="开始",
                command=self.startRecord)
        startBtn.pack(side=LEFT, fill=BOTH, expand=YES)
        self.startBtn=startBtn

        quitBtn=Button(ctrlFrm, text="退出",
                command=self.quit)
        quitBtn.pack(side=LEFT, fill=BOTH, expand=YES)
        self.quitBtn=quitBtn

        print("Initializing main interface...")

        readThread=ReadThread()
        readThread.start()
        while not readThread.is_ready: time.sleep(0.5)
        
        self.readThread=readThread

        calcThread=CalcThread(self)
        calcThread.start()
        self.calcThread=calcThread

        #Show Att Canvas
        self.attCns.show()
        self.mainloop()
        if self.calcThread.isAlive():
            self.calcThread.stop()
        if self.readThread.isAlive():
            self.readThread.stop()
        self.destroy()

    def openJSON(self):
        json_file=tkFileDialog.askopenfilename(\
                filetypes=[("JSON文件", "*.json")])
        if json_file is None: return

        json_path, json_name=os.path.split(json_file)
        self.jsfStr.set(json_name)
        with open(json_file, 'r') as f:
            json_dict=json.load(f)

        task_opt=DefaultTaskOpt()
        task_opt["code"]=json_dict["code"]
        task_opt['H']=json_dict['H']
        task_opt['L']=json_dict['L']
        # max time of H Att state
        task_opt["maxt_H_Att"]=json_dict['H_cur_dur_max']  
        ## parameters should input from input GUI

        self.task_opt=dict(self.task_opt, **task_opt)

    def startRecord(self):
        if self.startBtn["text"]==('开始').decode('utf-8'):
            targ=self.cttStr.get()

            try:
                float(self.task_opt["H"])
            except:
                tkMessageBox.showerror("错误", "无法识别参数文件，请重新加载！")
                return

            try:
                targ=float(targ)
            except:
                tkMessageBox.showerror("错误", "无法识别训练目标！")
                return
            targ=targ/100.
            self.task_opt["targ"]=targ
            
            cognRater=rater(self.task_opt)
            self.cognRater=cognRater
            self.startBtn["text"]="停止并退出"
            self.startBtn.update()
            self.readThread.is_record=True
            self.task_opt["start_time"]=time.time()
        else:
            self.readThread.stop()
            self.calcThread.stop()

            self.startBtn["text"]="完成"
            self.startBtn["state"]=DISABLED
            self.startBtn.update()
            # Get Report
            post_report=self.cognRater.getPostReport()
            # Get Start Time
            time_stramp=self.task_opt["start_time"]
            time_struct=time.localtime(time_stramp)
            time_string=time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
            post_report["start_time"]=time_string
            # Get Target
            post_report["targ"]=str(100*self.task_opt["targ"])+"%"
            # Get Code
            cod=self.task_opt["code"]
            post_report["code"]=cod

            report=dict(self.task_opt, **post_report)
            time_outtag=time.strftime('%Y_%m_%d_%H_%M_%S', time_struct)
            with open("data%s%s_train_%s.json" % (os.path.sep, cod,  time_outtag), "w") as f:
                json.dump(report, f)
            with open("report%strain.json" % os.path.sep, "w") as f:
                json.dump(report, f)
            self.quit()

if __name__=="__main__":
    root=TaskWindow()
