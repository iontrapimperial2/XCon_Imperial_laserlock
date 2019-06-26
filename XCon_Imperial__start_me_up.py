# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:29:59 2018

@author: IonTrap/JMHeinrich
"""

import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg

from XCon_Imperial_params import params
from XCon_Imperial_main import laser_control
from XCon_Imperial_GUI import Ui_XCon_Imperial

brush_background = (255,255,255,255)

blueBrush = (109,123,205,255)
blueBrush_alpha = (109,123,205,100)
bluePen = pg.mkPen(color = blueBrush, width = 2)

redBrush = (209,111,111,255)
redBrush_alpha = (209,111,111,100)
redPen = pg.mkPen(color = redBrush, width = 2)

blackBrush = (0,0,0,255)
blackPen = pg.mkPen(color = blackBrush, width = 2) 

labelstyle_L = {'color': '#000', 'font-size': '12pt'}

class window(Ui_XCon_Imperial):
    
    def __init__(self, dialog, laser_control):
        Ui_XCon_Imperial.__init__(self)
        self.setupUi(dialog)



        self.pushButton_debug.clicked.connect(self.pushButton_debug_clicked)
        
        #---------------------------------------------------------------------#
        #--- SET DEFAULT PARAMETERS ------------------------------------------#
        #---------------------------------------------------------------------#
        self.spinBox_debug.setValue(params['debug']['number'])
        self.doubleSpinBox_lock_blue_1_alpha.setValue(params['lock']['b1_alpha'])
        self.doubleSpinBox_lock_blue_1_alpha.setMaximum(params['lock']['b1_alpha_max'])
        self.doubleSpinBox_lock_blue_1_beta.setValue(params['lock']['b1_beta'])
        self.doubleSpinBox_lock_blue_1_beta.setMaximum(params['lock']['b1_beta_max'])

        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS AND TIMERS FOR LASER BLUE 1 -----------------#
        #---------------------------------------------------------------------#        
        self.plot_nu_blue_1 = pg.PlotWidget(name = 'widget_plot_nu_blue_1')
        self.plot_nu_blue_1.setBackground(background = brush_background)
        self.plot_nu_blue_1.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_nu_blue_1.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_nu_blue_1.showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_blue_1.addWidget(self.plot_nu_blue_1)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        self.pushButton_lock_laser_blue_1_on.clicked.connect(self.pushButton_lock_laser_blue_1_on_clicked)
        self.pushButton_lock_laser_blue_1_off.clicked.connect(self.pushButton_lock_laser_blue_1_off_clicked)
        
        self.pushButton_smooth_change_laser_blue_1_start.clicked.connect(self.pushButton_smooth_change_laser_blue_1_start_clicked)
        self.pushButton_smooth_change_laser_blue_1_stop.clicked.connect(self.pushButton_smooth_change_laser_blue_1_stop_clicked)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#
        self.timer_t_dependent_plots_laser_blue_1 = QtCore.QTimer()
        self.timer_t_dependent_plots_laser_blue_1.setInterval(250)
        self.timer_t_dependent_plots_laser_blue_1.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_t_dependent_plots_laser_blue_1.timeout.connect(self.t_dependent_updates_laser_blue_1)
        self.timer_t_dependent_plots_laser_blue_1.start()
        #---------------------------------------------------------------------#



        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS AND TIMERS FOR LASER BLUE 2 -----------------#
        #---------------------------------------------------------------------#        
        self.plot_nu_blue_2 = pg.PlotWidget(name = 'widget_plot_nu_blue_2')
        self.plot_nu_blue_2.setBackground(background = brush_background)
        self.plot_nu_blue_2.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_nu_blue_2.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_nu_blue_2.showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_blue_2.addWidget(self.plot_nu_blue_2)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        self.pushButton_lock_laser_blue_2_on.clicked.connect(self.pushButton_lock_laser_blue_2_on_clicked)
        self.pushButton_lock_laser_blue_2_off.clicked.connect(self.pushButton_lock_laser_blue_2_off_clicked)
        
        self.pushButton_smooth_change_laser_blue_2_start.clicked.connect(self.pushButton_smooth_change_laser_blue_2_start_clicked)
        self.pushButton_smooth_change_laser_blue_2_stop.clicked.connect(self.pushButton_smooth_change_laser_blue_2_stop_clicked)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#
        self.timer_t_dependent_plots_laser_blue_2 = QtCore.QTimer()
        self.timer_t_dependent_plots_laser_blue_2.setInterval(250)
        self.timer_t_dependent_plots_laser_blue_2.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_t_dependent_plots_laser_blue_2.timeout.connect(self.t_dependent_updates_laser_blue_2)
        self.timer_t_dependent_plots_laser_blue_2.start()
        #---------------------------------------------------------------------#        
 


        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS AND TIMERS FOR LASER RED 1 ------------------#
        #---------------------------------------------------------------------#        
        self.plot_nu_red_1 = pg.PlotWidget(name = 'widget_plot_nu_red_1')
        self.plot_nu_red_1.setBackground(background = brush_background)
        self.plot_nu_red_1.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_nu_red_1.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_nu_red_1.showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_red_1.addWidget(self.plot_nu_red_1)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        self.pushButton_lock_laser_red_1_on.clicked.connect(self.pushButton_lock_laser_red_1_on_clicked)
        self.pushButton_lock_laser_red_1_off.clicked.connect(self.pushButton_lock_laser_red_1_off_clicked)
        
        self.pushButton_smooth_change_laser_red_1_start.clicked.connect(self.pushButton_smooth_change_laser_red_1_start_clicked)
        self.pushButton_smooth_change_laser_red_1_stop.clicked.connect(self.pushButton_smooth_change_laser_red_1_stop_clicked)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#
        self.timer_t_dependent_plots_laser_red_1 = QtCore.QTimer()
        self.timer_t_dependent_plots_laser_red_1.setInterval(250)
        self.timer_t_dependent_plots_laser_red_1.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_t_dependent_plots_laser_red_1.timeout.connect(self.t_dependent_updates_laser_red_1)
        self.timer_t_dependent_plots_laser_red_1.start()
        #---------------------------------------------------------------------#
        
        
        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS AND TIMERS FOR LASER RED 2 ------------------#
        #---------------------------------------------------------------------#        
        self.plot_nu_red_2 = pg.PlotWidget(name = 'widget_plot_nu_red_2')
        self.plot_nu_red_2.setBackground(background = brush_background)
        self.plot_nu_red_2.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_nu_red_2.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_nu_red_2.showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_red_2.addWidget(self.plot_nu_red_2)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        self.pushButton_lock_laser_red_2_on.clicked.connect(self.pushButton_lock_laser_red_2_on_clicked)
        self.pushButton_lock_laser_red_2_off.clicked.connect(self.pushButton_lock_laser_red_2_off_clicked)
        
        self.pushButton_smooth_change_laser_red_2_start.clicked.connect(self.pushButton_smooth_change_laser_red_2_start_clicked)
        self.pushButton_smooth_change_laser_red_2_stop.clicked.connect(self.pushButton_smooth_change_laser_red_2_stop_clicked)
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#
        self.timer_t_dependent_plots_laser_red_2 = QtCore.QTimer()
        self.timer_t_dependent_plots_laser_red_2.setInterval(250)
        self.timer_t_dependent_plots_laser_red_2.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_t_dependent_plots_laser_red_2.timeout.connect(self.t_dependent_updates_laser_red_2)
        self.timer_t_dependent_plots_laser_red_2.start()
        #---------------------------------------------------------------------#    



        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS AND TIMERS FOR SAWTOOTH ---------------------#
        #---------------------------------------------------------------------#         
        self.plot_sawtooth1 = pg.PlotWidget(name = 'widget_plot_sawtooth')
        self.plot_sawtooth1.setBackground(background = brush_background)
        self.plot_sawtooth1.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_sawtooth1.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_sawtooth1.showGrid(x = True, y = True)
        
        self.verticalLayout_sawtooth_blue_1.addWidget(self.plot_sawtooth1)
        #---------------------------------------------------------------------#
        
        #---------------------------------------------------------------------#        
        self.plot_sawtooth2 = pg.PlotWidget(name = 'widget_plot_sawtooth')
        self.plot_sawtooth2.setBackground(background = brush_background)
        self.plot_sawtooth2.setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plot_sawtooth2.setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plot_sawtooth2.showGrid(x = True, y = True)
        
        self.verticalLayout_sawtooth_blue_2.addWidget(self.plot_sawtooth2)
        #---------------------------------------------------------------------#
        
        self.pushButton_sawtooth_laser_blue_1_and_2_start.clicked.connect(lc.sawtooth_laser_blue_1_and_2_on)
        self.pushButton_sawtooth_laser_blue_1_and_2_stop.clicked.connect(lc.sawtooth_laser_blue_1_and_2_off)
        
        #---------------------------------------------------------------------#
        self.timer_t_dependent_plots_sawtooth = QtCore.QTimer()
        self.timer_t_dependent_plots_sawtooth.setInterval(250)
        self.timer_t_dependent_plots_sawtooth.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_t_dependent_plots_sawtooth.timeout.connect(self.t_dependent_updates_sawtooth)
        self.timer_t_dependent_plots_sawtooth.start()
        #---------------------------------------------------------------------#   
    ###########################################################################
    ###########################################################################
    ### THE FUNCTIONS FOR THE PUSH BUTTONS ####################################
    ###########################################################################
    ########################################################################### 
    
    def pushButton_debug_clicked(self):
        lc.debug_number = self.spinBox_debug.value()
        lc.debug_flag = True
    
    
    ###########################################################################
    ### FUNCTIONS FOR LASER BLUE 1 ############################################
    ###########################################################################           
        
    ###########################################################################
    def pushButton_lock_laser_blue_1_on_clicked(self):
        lc.nu_blue_1_want = float(self.doubleSpinBox_nu_blue_1_want.value())
        lc.nu_setpoint['blue_1'] = float(self.doubleSpinBox_nu_blue_1_want.value())
        lc.lock_laser_blue_1_on()
                
        
    def pushButton_lock_laser_blue_1_off_clicked(self):
        lc.lock_laser_blue_1_off()
        
        
    def pushButton_smooth_change_laser_blue_1_start_clicked(self):
        lc.nu_blue_1_smooth_want = float(self.doubleSpinBox_nu_blue_1_smooth_want.value())
        lc.nu_blue_1_smooth_delta_t = float(self.doubleSpinBox_nu_blue_1_smooth_delta_t.value())
        lc.smooth_change_laser_blue_1_start()

    def pushButton_smooth_change_laser_blue_1_stop_clicked(self):
        lc.smooth_change_laser_blue_1_stop()
    ###########################################################################   
        
    ###########################################################################        
    def t_dependent_updates_laser_blue_1(self):
        
        self.label_nu_blue_1_is.setText(f'{lc.nu_blue_1_is:.7f}')
        
#        self.doubleSpinBox_nu_blue_1_want.setValue(lc.nu_blue_1_want)
           
        lc.lock_blue_1_alpha = float(self.doubleSpinBox_lock_blue_1_alpha.value())
        lc.lock_blue_1_beta = float(self.doubleSpinBox_lock_blue_1_beta.value())
        
        lc.lock_pars['blue_1']['k_p'] = float(self.doubleSpinBox_lock_blue_1_alpha.value())
        lc.lock_pars['blue_1']['k_i'] = float(self.doubleSpinBox_lock_blue_1_beta.value())
        
        if lc.lock_blue_1:
            self.label_lock_blue_1_status.setText('ON')
            self.label_lock_blue_1_status.setStyleSheet('color: black')
        else:
            self.label_lock_blue_1_status.setText('OFF')
            self.label_lock_blue_1_status.setStyleSheet('color: red')
       
        try:
            self.plot_nu_blue_1.plot(np.arange(500),lc.nu_blue_1_was[-500:],pen = blackPen, symbol = 'o', symbolBrush = blueBrush, name = 'nu_blue_1_was', clear = True)
        except Exception:
            pass
            
        nu_blue_1_upper = pg.PlotCurveItem([0,500],[755.186881,755.186881],pen = bluePen)
        nu_blue_1_lower = pg.PlotCurveItem([0,500],[755.186879,755.186879],pen = bluePen)
        nu_blue_1_fill = pg.FillBetweenItem(nu_blue_1_upper,nu_blue_1_lower,blueBrush_alpha)
        
        self.plot_nu_blue_1.addItem(nu_blue_1_upper)
        self.plot_nu_blue_1.addItem(nu_blue_1_lower)
        self.plot_nu_blue_1.addItem(nu_blue_1_fill)        
    ###########################################################################    
        


    ###########################################################################
    ### FUNCTIONS FOR LASER BLUE 2 ############################################
    ###########################################################################           
        
    ###########################################################################
    def pushButton_lock_laser_blue_2_on_clicked(self):
        lc.nu_blue_2_want = float(self.doubleSpinBox_nu_blue_2_want.value())
        lc.lock_laser_blue_2_on()
        self.label_lock_blue_2_status.setText('ON')
        self.label_lock_blue_2_status.setStyleSheet('color: black')        
        
    def pushButton_lock_laser_blue_2_off_clicked(self):
        lc.lock_laser_blue_2_off()
        self.label_lock_blue_2_status.setText('OFF')
        self.label_lock_blue_2_status.setStyleSheet('color: red')
        
    def pushButton_smooth_change_laser_blue_2_start_clicked(self):
        lc.nu_blue_2_smooth_want = float(self.doubleSpinBox_nu_blue_2_smooth_want.value())
        lc.nu_blue_2_smooth_delta_t = float(self.doubleSpinBox_nu_blue_2_smooth_delta_t.value())
        lc.smooth_change_laser_blue_2_start()

    def pushButton_smooth_change_laser_blue_2_stop_clicked(self):
        lc.smooth_change_laser_blue_2_stop()
    ###########################################################################   
        
    ###########################################################################        
    def t_dependent_updates_laser_blue_2(self):
        
        self.label_nu_blue_2_is.setText(str(lc.nu_blue_2_is))
        
#        self.doubleSpinBox_nu_blue_1_want.setValue(lc.nu_blue_1_want)
           
        lc.lock_blue_2_alpha = float(self.doubleSpinBox_lock_blue_2_alpha.value())
        lc.lock_blue_2_beta = float(self.doubleSpinBox_lock_blue_2_beta.value())
       
        try:
            self.plot_nu_blue_2.plot(np.arange(500),lc.nu_blue_2_was[-500:],pen = blackPen, symbol = 'o', symbolBrush = blueBrush, name = 'nu_blue_2_was', clear = True)
        except Exception:
            pass
            
        nu_blue_2_upper = pg.PlotCurveItem([0,500],[755.258221,755.258221],pen = bluePen)
        nu_blue_2_lower = pg.PlotCurveItem([0,500],[755.258219,755.258219],pen = bluePen)
        nu_blue_2_fill = pg.FillBetweenItem(nu_blue_2_upper,nu_blue_2_lower,blueBrush_alpha)
        
        self.plot_nu_blue_2.addItem(nu_blue_2_upper)
        self.plot_nu_blue_2.addItem(nu_blue_2_lower)
        self.plot_nu_blue_2.addItem(nu_blue_2_fill)        
    ###########################################################################         
 


    ###########################################################################
    ### FUNCTIONS FOR LASER RED 1 #############################################
    ###########################################################################           
        
    ###########################################################################
    def pushButton_lock_laser_red_1_on_clicked(self):
        lc.nu_red_1_want = float(self.doubleSpinBox_nu_red_1_want.value())
        lc.lock_laser_red_1_on()
        self.label_lock_red_1_status.setText('ON')
        self.label_lock_red_1_status.setStyleSheet('color: black')        
        
    def pushButton_lock_laser_red_1_off_clicked(self):
        lc.lock_laser_red_1_off()
        self.label_lock_red_1_status.setText('OFF')
        self.label_lock_red_1_status.setStyleSheet('color: red')
        
    def pushButton_smooth_change_laser_red_1_start_clicked(self):
        lc.nu_red_1_smooth_want = float(self.doubleSpinBox_nu_red_1_smooth_want.value())
        lc.nu_red_1_smooth_delta_t = float(self.doubleSpinBox_nu_red_1_smooth_delta_t.value())
        lc.smooth_change_laser_red_1_start()

    def pushButton_smooth_change_laser_red_1_stop_clicked(self):
        lc.smooth_change_laser_red_1_stop()
    ###########################################################################   
        
    ###########################################################################        
    def t_dependent_updates_laser_red_1(self):
        
        self.label_nu_red_1_is.setText(str(lc.nu_red_1_is))
        
#        self.doubleSpinBox_nu_blue_1_want.setValue(lc.nu_blue_1_want)
           
        lc.lock_red_1_alpha = float(self.doubleSpinBox_lock_red_1_alpha.value())
        lc.lock_red_1_beta = float(self.doubleSpinBox_lock_red_1_beta.value())
       
        try:
            self.plot_nu_red_1.plot(np.arange(500),lc.nu_red_1_was[-500:],pen = blackPen, symbol = 'o', symbolBrush = redBrush, name = 'nu_red_1_was', clear = True)
        except Exception:
            pass
            
        nu_red_1_upper = pg.PlotCurveItem([0,500],[346.000255,346.000255],pen = redPen)
        nu_red_1_lower = pg.PlotCurveItem([0,500],[346.000245,346.000245],pen = redPen)
        nu_red_1_fill = pg.FillBetweenItem(nu_red_1_upper,nu_red_1_lower,redBrush_alpha)
        
        self.plot_nu_red_1.addItem(nu_red_1_upper)
        self.plot_nu_red_1.addItem(nu_red_1_lower)
        self.plot_nu_red_1.addItem(nu_red_1_fill)        
    ###########################################################################   



    ###########################################################################
    ### FUNCTIONS FOR LASER RED 2 #############################################
    ###########################################################################           
        
    ###########################################################################
    def pushButton_lock_laser_red_2_on_clicked(self):
        lc.nu_red_2_want = float(self.doubleSpinBox_nu_red_2_want.value())
        lc.lock_laser_red_2_on()
        self.label_lock_red_2_status.setText('ON')
        self.label_lock_red_2_status.setStyleSheet('color: black')        
        
    def pushButton_lock_laser_red_2_off_clicked(self):
        lc.lock_laser_red_2_off()
        self.label_lock_red_2_status.setText('OFF')
        self.label_lock_red_2_status.setStyleSheet('color: red')
        
    def pushButton_smooth_change_laser_red_2_start_clicked(self):
        lc.nu_red_2_smooth_want = float(self.doubleSpinBox_nu_red_2_smooth_want.value())
        lc.nu_red_2_smooth_delta_t = float(self.doubleSpinBox_nu_red_2_smooth_delta_t.value())
        lc.smooth_change_laser_red_2_start()

    def pushButton_smooth_change_laser_red_2_stop_clicked(self):
        lc.smooth_change_laser_red_2_stop()
    ###########################################################################   
        
    ###########################################################################        
    def t_dependent_updates_laser_red_2(self):
        
        self.label_nu_red_2_is.setText(str(lc.nu_red_2_is))
        
#        self.doubleSpinBox_nu_blue_1_want.setValue(lc.nu_blue_1_want)
           
        lc.lock_red_2_alpha = float(self.doubleSpinBox_lock_red_2_alpha.value())
        lc.lock_red_2_beta = float(self.doubleSpinBox_lock_red_2_beta.value())
       
        try:
            self.plot_nu_red_2.plot(np.arange(500),lc.nu_red_2_was[-500:],pen = blackPen, symbol = 'o', symbolBrush = redBrush, name = 'nu_red_2_was', clear = True)
        except Exception:
            pass
            
        nu_red_2_upper = pg.PlotCurveItem([0,500],[350.862605,350.862605],pen = redPen)
        nu_red_2_lower = pg.PlotCurveItem([0,500],[350.862595,350.862595],pen = redPen)
        nu_red_2_fill = pg.FillBetweenItem(nu_red_2_upper,nu_red_2_lower,redBrush_alpha)
        
        self.plot_nu_red_2.addItem(nu_red_2_upper)
        self.plot_nu_red_2.addItem(nu_red_2_lower)
        self.plot_nu_red_2.addItem(nu_red_2_fill)        
    ###########################################################################   


    ###########################################################################        
    def t_dependent_updates_sawtooth(self):
       
        lc.sawtooth_nu_blue_1_init = self.doubleSpinBox_sawtooth_nu_blue_1_init.value()
        lc.sawtooth_nu_blue_1_detuned = self.doubleSpinBox_sawtooth_nu_blue_1_detuned.value()
        lc.sawtooth_nu_blue_2_init = self.doubleSpinBox_sawtooth_nu_blue_2_init.value()
        lc.sawtooth_nu_blue_2_detuned = self.doubleSpinBox_sawtooth_nu_blue_2_detuned.value()
        lc.sawtooth_delta_t1 = self.doubleSpinBox_sawtooth_delta_t1.value()
        lc.sawtooth_delta_t2 = self.doubleSpinBox_sawtooth_delta_t2.value()
        lc.sawtooth_total_reps = self.spinBox_sawtooth_total_reps.value()
        
        lc.f_prepare_sawtooth_laser_blue_1_and_2()
            
        self.plot_sawtooth1.plot(lc.sawtooth_t_total,lc.sawtooth_nu1_total, order = 0, pen = bluePen, name = 'nu_sawtooth1', clear = True)
        self.plot_sawtooth2.plot(lc.sawtooth_t_total,lc.sawtooth_nu2_total, order = 0, pen = bluePen, name = 'nu_sawtooth2', clear = True)
    ###########################################################################   

      
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    lc = laser_control()
    
    dialog_lc = QtWidgets.QMainWindow()
    
    programm_lc = window(dialog_lc,lc)
    dialog_lc.show()
    
    sys.exit(app.exec_())