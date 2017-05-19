# -*- coding: utf-8 -*-

"""
Created on Sun Aug 28 21:25:34 2016

@author: yangz
"""

import numpy as np
import mne
import datetime
import time
import scipy.io as scio

class getData:

    # simulate reading EEG source
    @staticmethod
    def getDataFrame(tm, opt):
        global arr_dat
        ed = tm * opt['sr']
        st = ed - opt['w_win']*opt['sr']
        if ed>arr_dat.shape[1]:
            return -999
        if st<0:
            st = 0
        dat_win = arr_dat[:,st:ed]
        return dat_win

    # simulate reading start button
    @staticmethod
    def getStartFlag(tm, opt):
        if tm > 1:
            return 1
        else:
            return 0

class rater:
    def __init__(self, opt):
        self.dur_total = 0     # total time
        self.count_H_Att = 0    # index of high attention state
        self.dur_L_Att = [0]   # time of low attention states
        self.count_L_Att = 0    # index of low attention state
        self.dur_H_Att = [0]   # time of high attention states
        self.count_ascend = 0   # index of ascending attention L->H
        self.dur_ascend = [0]  # time of ascending
        self.count_descend = 0   # index of descending attention L->H
        self.dur_descend = [0]  # time of descending
        self.sta_curr = 0       # initial current state
        self.sta_last = 0       # initial last state
        self.flag_exitL = 0         # flag exited L state
        self.flag_exitH = 0         # flag exited H state
        self.max_Att = 0        # updated max Att
        self.min_Att = 1        # updated min Att
        self.tp_start_H = [0]
        self.tp_start_L = [0]
        self.tp_start_rampup = [0]
        self.tp_start_rampdn = [0]

        # load parameters
        self.H = opt['H']
        self.L = opt['L']
        self.inc_update = opt['inc_update']
        self.targ = opt['targ']
        self.dur_H = opt['maxt_H_Att']
        # calc star parameters
        self.thr_star = [0,0,0,0,0]
        self.curr_star = 0
        for i in range(5):
            self.thr_star[i] = self.dur_H * (1+self.targ/5*i)

        self.report_dict=dict()

    def timeCounter(self, Att):
        # add total time
        self.dur_total = self.dur_total + self.inc_update

        # judge state
        if Att > self.H:
            self.sta_curr = 1
        elif Att < self.L:
            self.sta_curr = -1
        else:
            self.sta_curr = 0

        # update min and max
        self.max_Att = max(self.max_Att, Att)
        self.min_Att = min(self.min_Att, Att)

        # set event flags
        if self.sta_curr < 1 and self.sta_last == 1:
            self.flag_exitH = 1
            self.tp_start_rampdn[self.count_descend] = self.dur_total

        if self.sta_curr > -1 and self.sta_last == -1:
            self.flag_exitL = 1
            self.tp_start_rampup[self.count_ascend] = self.dur_total

        # record time of entering H and L
        if self.sta_curr == 1 and self.sta_last < 1:
            self.tp_start_H.extend([self.dur_total])

        if self.sta_curr == -1 and self.sta_last > -1:
            self.tp_start_L.extend([self.dur_total])

        # four stopwatches
        # H watch
        if self.sta_curr == 1:
            self.dur_H_Att[self.count_H_Att] = self.dur_H_Att[self.count_H_Att]\
            + self.inc_update
        if self.sta_curr < 1 and self.sta_last == 1:     # stop the watch and prepare for next time
            self.count_H_Att = self.count_H_Att + 1
            self.dur_H_Att.extend([0])

        # L watch
        if self.sta_curr == -1:
            self.dur_L_Att[self.count_L_Att] = self.dur_L_Att[self.count_L_Att] \
            + self.inc_update
        if self.sta_curr > -1 and self.sta_last == -1:
            self.count_L_Att = self.count_L_Att + 1
            self.dur_L_Att.extend([0])

        # ascend watch
        if self.sta_curr > -1 and self.flag_exitL:
            self.dur_ascend[self.count_ascend] = self.dur_ascend[self.count_ascend] \
            + self.inc_update
            if self.sta_last < 1 and self.sta_curr == 1:      # extend one if just finish ascending
                self.count_ascend = self.count_ascend + 1
                self.dur_ascend.extend([0])
                self.tp_start_rampup.extend([0])
                self.flag_exitL = 0
        if self.sta_curr == -1 and self.sta_last > -1:    # reset watch if Att go back to L
            self.dur_ascend[self.count_ascend] = 0
            self.tp_start_rampup[self.count_ascend] = self.dur_total

        # descend watch
        if self.sta_curr < 1 and self.flag_exitH:
            self.dur_descend[self.count_descend] = self.dur_descend[self.count_descend] \
            + self.inc_update
            if self.sta_curr == -1 and self.sta_last > -1:
                self.count_descend = self.count_descend + 1
                self.dur_descend.extend([0])
                self.tp_start_rampdn.extend([0])
                self.flag_exitH = 0
        if self.sta_curr == 1 and self.sta_last < 1:
            self.dur_descend[self.count_descend] = 0
            self.tp_start_rampdn[self.count_descend] = self.dur_total

        # update last state
        self.sta_last = self.sta_curr

    def getStar(self):
        if self.curr_star == 5:
            return self.curr_star
        if max(self.dur_H_Att) >= self.thr_star[self.curr_star]:
            self.curr_star = self.curr_star + 1
        return self.curr_star

    def getRtReport(self):
#        print "time of ramp-up: ", self.dur_ascend
#        print "time of High Att: ", self.dur_H_Att
#        print "time of ramp-dw: ", self.dur_descend
#        print "time of Low Att: ", self.dur_L_Att
#        print "tp of start H: ", self.tp_start_H
#        print "tp of start L: ", self.tp_start_L
#        print "tp of start rampup: ", self.tp_start_rampup
#        print "tp of start rampdn: ", self.tp_start_rampdn

        # star system
        star = self.getStar()
#        print "stars: ", star
#        print "========================"
        return np.sum(self.dur_H_Att)

    def getPostReport(self):
        print("Post Report:")
        print("----------------------------------")
        H_dur_total=sum(self.dur_H_Att)
        self.report_dict["H_dur_total"]=H_dur_total
        print("total H Att time: ", H_dur_total)

        self.report_dict["count_H_Att"]= self.count_H_Att
        self.report_dict["max"] = self.max_Att
        self.report_dict["min"] = self.min_Att

        lgth = len(self.dur_H_Att)
        if self.dur_H_Att[-1] == 0:
            lgth = lgth - 1
        if lgth > 0:
            H_dur_mean = H_dur_total/lgth
        else:
            H_dur_mean = H_dur_total
        self.report_dict["H_dur_mean"] = H_dur_mean
        print("mean H Att duration: ", H_dur_mean)

        H_dur_total_ratio=100.0*(float(H_dur_total)/float(self.dur_total))
        self.report_dict["H_dur_total_ratio"]=H_dur_total_ratio
        print("percentage of H Att time: ", H_dur_total_ratio)

        H_cur_dur_max=max(self.dur_H_Att)
        self.report_dict["H_cur_dur_max"]=H_cur_dur_max
        print("max single time of H Att: ", H_cur_dur_max)

        if len(self.tp_start_H) > 1 & self.tp_start_H[-1] == 0:  # remove the last 0
            del self.tp_start_H[-1]
        if len(self.dur_H_Att) > 1 & self.dur_H_Att[-1] == 0:  # remove the last 0
            del self.dur_H_Att[-1]
        #ed_H = np.add(self.tp_start_H, self.dur_H_Att)

        #ed_H = ed_H[0:len(ed_H)-1]
        #st_H = self.tp_start_H[1:len(self.tp_start_H)]
        #interval_H = st_H - ed_H

        # speed of ramp-up
        lgth = len(self.dur_ascend)
        if self.dur_ascend[-1] == 0:  # remove the last 0
            lgth = lgth - 1
        if lgth > 0:
            speed_up = 1.0/(sum(self.dur_ascend)/float(lgth))
        else:
            speed_up = 0

        self.report_dict["Rampup_speed_mean"]=speed_up
        print("mean speed of Att ramp-up: ", speed_up)

        # speed of ramp-down
        lgth = len(self.dur_descend)
        if self.dur_descend[-1] == 0:
            lgth = lgth - 1
        if lgth > 0:
            speed_down = 1.0/(sum(self.dur_descend)/float(lgth))
        else:
            speed_down = 0

        self.report_dict["Rampdown_speed_mean"]=speed_down
        print("mean speed of Att ramp-down: ", speed_down)

        # star
        self.report_dict["Achievement"]=self.curr_star
        print("achievement: ", self.curr_star)

        print("----------------------------------")

        return self.report_dict

class compute:
    @staticmethod
    def manager(opt):
        tm = 0  # time for current window end
        flag_has_base = 0;  # one-time flag for setting Att_base
        Att_base = 1; # Att at session base
        # Att = 1;    # value of Att
        rater_Att = rater(opt)
        next_call = time.time()
        while True:
            print datetime.datetime.now()
            tm = tm+opt['inc_update']
            dat_win = getData.getDataFrame(tm, opt)
            flg_start = getData.getStartFlag(tm, opt)

            if isinstance(dat_win, int) and dat_win == -999:
                return rater_Att

            # check data is sufficient and start is clicked
            if flg_start == 1 and dat_win.shape >= opt['w_win']*opt['sr']:
                # calc Att
                Att = compute.computer(dat_win, Att_base, opt)
                print "Att=%f" %Att
                if flag_has_base == 0:
                    Att_base = Att # use it as session base if this is the first window
                    flag_has_base = 1
                rater_Att.timeCounter(Att)
                rater_Att.getRtReport()
            # provide feedback
            # adjust time to fit 2s
            next_call = next_call+opt['inc_update'];

            time.sleep(max(next_call - time.time(), 0))

    @staticmethod
    def computer(dat, Att_base, opt):
        # make dataset
        info_dat = mne.create_info(opt['ch_names'], opt['sr'], opt['ch_types'])
        dat = mne.io.RawArray(dat, info_dat, verbose='ERROR')

        # identify eog
        ev_eog = mne.preprocessing.find_eog_events(dat, event_id=998, ch_name='Fp1,Fp2', verbose='ERROR')
        kk = np.array([], dtype=int)
        for i in range(0, ev_eog.shape[0]):
            kk = np.append(kk, range(int(ev_eog[i,0]-0.2*250), int(ev_eog[i,0]+0.2*250)))
        kk = kk[kk>=0]

        # alpha band
        dat_alpha = dat.copy()
        dat_alpha.filter(8., 13., verbose='ERROR')
        pw_alpha = compute.calPower(dat_alpha, kk, opt)
        pw_alpha = pw_alpha[0]
        inspect.inspect(pw_alpha)

        # beta band
        dat_beta = dat.copy()
        dat_beta.filter(16., 31., verbose='ERROR')
        pw_beta = compute.calPower(dat_beta, kk, opt)
        pw_beta = pw_beta[0]

        # Att


        Att = pw_beta/pw_alpha
        Att = np.mean(Att)
        Att = Att/Att_base
        return Att

    @staticmethod
    def calPower(tc, kk, opt):
        dd = np.array(tc._data)
        dd = np.delete(dd, kk, 1)
        if dd.shape[1] > 0:
            pw = np.sum(np.power(dd, 2),1)
            pw = pw/dd.shape[1]*opt['sr']
        else:
            pw = 1
        return pw

class getOpt:
    def __init__(self):
        # set or load opt
        opt = dict()
        opt['sr'] = 250
        opt['tm_base'] = 10 # in secs
        opt['ch_names'] = ['Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'Cz','Pz']
        opt['ch_types'] = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
        opt['n_ch'] = 8
        opt['w_win'] = 10 # window width, 10s
        opt['inc_win'] = 1 # step of sliding window, 1s
        opt['inc_update'] = 1 # time interval for updating feedback, 2s

        # paramaters should read from database
        opt['H'] = 0.9 # H threshold
        opt['L'] = 0.4  # L threshold
        opt['maxt_H_Att'] = 5   # max time of H Att state
        # parameters should input from input GUI
        opt['targ'] = 0.10 # target: increase by 5%

        self.opt = opt
# inspect pw
class inspect:
    pw_down = 1000
    pw_up = 10000
    count = 0
    duration = 5 # pw过大或过小持续时间
    @staticmethod
    def inspect(pw):
        if pw == 0:
            print 'No connection'
        if pw > inspect.pw_up:
            inspect.count += 1
            print inspect.count
            if inspect.count > inspect.duration:
                print 'The signal is being affected'
                raw_input('Find out the fault and press any key to continue:')
        elif pw < inspect.pw_down:
            inspect.count -= 1
            if inspect.count < -inspect.duration:
                print 'Not be connected well'
                raw_input('Connect well and press any key to continue:')
        else:
            inspect.count = 0

if __name__ == '__main__':
    # simulate the data source
    h = scio.loadmat('simdat.mat')
    arr_dat = h['dat']  #[:,1:10000]

    rater_Att = compute.manager(getOpt().opt)
    print "end of realtime feedback"

    # postReport(rater_Att)
    
