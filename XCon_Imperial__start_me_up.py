# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:29:59 2018

@author: IonTrap/JMHeinrich
"""

import sys
import time
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
        self.mainWindow = dialog
        print('initialising gui')



        self.pushButton_debug.clicked.connect(self.pushButton_debug_clicked)
        
        #---------------------------------------------------------------------#
        #--- SET DEFAULT PARAMETERS ------------------------------------------#
        #---------------------------------------------------------------------#
        self.spinBox_debug.setValue(params['debug']['number'])
        
        self.doubleSpinBox_lock_blue_1_k_p.setValue(params['lock']['blue_1']['k_p'])
        self.doubleSpinBox_lock_blue_1_k_p.setMaximum(params['lock']['blue_1']['k_p_max'])
        self.doubleSpinBox_lock_blue_1_k_i.setValue(params['lock']['blue_1']['k_i'])
        self.doubleSpinBox_lock_blue_1_k_i.setMaximum(params['lock']['blue_1']['k_i_max'])

        self.doubleSpinBox_lock_blue_2_alpha.setValue(params['lock']['blue_2']['k_p'])
        self.doubleSpinBox_lock_blue_2_alpha.setMaximum(params['lock']['blue_2']['k_p_max'])
        self.doubleSpinBox_lock_blue_2_beta.setValue(params['lock']['blue_2']['k_i'])
        self.doubleSpinBox_lock_blue_2_beta.setMaximum(params['lock']['blue_2']['k_i_max'])
        
        self.plots = {}

        #---------------------------------------------------------------------#
        #--- PLOTS AND PUSH BUTTONS FOR LASER BLUE 1 -----------------#
        #---------------------------------------------------------------------#
        self.plots['blue_1'] = pg.PlotWidget(name = 'widget_plot_nu_blue_1')
        self.plots['blue_1'].setBackground(background = brush_background)
        self.plots['blue_1'].setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plots['blue_1'].setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plots['blue_1'].showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_blue_1.addWidget(self.plots['blue_1'])
        
        self.base_freqs = {'blue_1': self.doubleSpinBox_nu_blue_1_want.value(), 'blue_2': self.doubleSpinBox_nu_blue_2_want.value()}
        self.offset_freqs = {'blue_1': self.doubleSpinBox_blue_1_offset.value(), 'blue_2': 0}
        self.setpoint_freqs = {'blue_1': self.base_freqs['blue_1']+self.offset_freqs['blue_1']*1e-6, 'blue_2':  self.base_freqs['blue_2']+self.offset_freqs['blue_2']*1e-6}
        
        self.smooth_change_flags = {'blue_1': False, 'blue_2': False, 'red_1': False, 'red_2': False}
        
        self.smooth_change_params_blue_1 = {'initial offset': 0, 'final_offset': 10, 'change time': 1, 'start time': 0}
        self.smooth_change_params = {'blue_1': self.smooth_change_params_blue_1.copy(), 'blue_2': self.smooth_change_params_blue_1.copy()}
        
        self.label_blue_1_setpoint.setText(f'{self.setpoint_freqs["blue_1"]:.7f}')
        
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        #self.pushButton_lock_laser_blue_1_on.clicked.connect(lambda: self.pushButton_lock_laser_on_clicked('blue_1'))
        self.pushButton_lock_laser_blue_1_on.clicked.connect(self.lock_laser_on)
        self.pushButton_lock_laser_blue_1_off.clicked.connect(self.lock_laser_off)
        
        self.pushButton_smooth_change_laser_blue_1_start.clicked.connect(self.start_smooth_scan)
        self.pushButton_smooth_change_laser_blue_1_stop.clicked.connect(self.stop_smooth_scan)
        
        self.doubleSpinBox_nu_blue_1_want.valueChanged.connect(self.base_freq_changed)
        self.doubleSpinBox_nu_blue_2_want.valueChanged.connect(self.base_freq_changed)
        
        self.doubleSpinBox_blue_1_offset.valueChanged.connect(self.offset_freq_changed)
        
        self.doubleSpinBox_lock_blue_1_k_p.valueChanged.connect(self.k_p_changed)
        self.doubleSpinBox_lock_blue_1_k_i.valueChanged.connect(self.k_i_changed)
        #---------------------------------------------------------------------#

     


        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS FOR LASER BLUE 2 -----------------#
        #---------------------------------------------------------------------#        
        self.plots['blue_2'] = pg.PlotWidget(name = 'widget_plot_nu_blue_2')
        self.plots['blue_2'].setBackground(background = brush_background)
        self.plots['blue_2'].setLabel('left', 'nu', units = '[THz]', **labelstyle_L)
        self.plots['blue_2'].setLabel('bottom', 'time', units = '', **labelstyle_L)
        self.plots['blue_2'].showGrid(x = True, y = True)
        
        self.verticalLayout_nu_laser_blue_2.addWidget(self.plots['blue_2'])
        #---------------------------------------------------------------------#

        #---------------------------------------------------------------------#   
        self.pushButton_lock_laser_blue_2_on.clicked.connect(self.lock_laser_on)
        self.pushButton_lock_laser_blue_2_off.clicked.connect(self.lock_laser_off)
        
        self.pushButton_smooth_change_laser_blue_2_start.clicked.connect(self.pushButton_smooth_change_laser_blue_2_start_clicked)
        self.pushButton_smooth_change_laser_blue_2_stop.clicked.connect(self.pushButton_smooth_change_laser_blue_2_stop_clicked)
        #---------------------------------------------------------------------#
     
 


        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS FOR LASER RED 1 ------------------#
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
        #--- PLOTS, PUSH BUTTONS FOR LASER RED 2 ------------------#
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



        #---------------------------------------------------------------------#
        #--- PLOTS, PUSH BUTTONS FOR SAWTOOTH ---------------------#
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
        #self.doubleSpinBox_lock_blue_1_alpha
        #---------------------------------------------------------------------#
        #--- SET UP TIMERS ---------------------#
        #---------------------------------------------------------------------#          
        
        # Plot updater
        self.timer_update_plots = QtCore.QTimer()
        self.timer_update_plots.setInterval(250)
        self.timer_update_plots.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_update_plots.timeout.connect(self.update_plots)
        self.timer_update_plots.start()
        
        # Setpoint updater
        self.timer_update_setpoints = QtCore.QTimer()
        self.timer_update_setpoints.setInterval(250)
        self.timer_update_setpoints.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer_update_setpoints.timeout.connect(self.update_setpoints)
        self.timer_update_setpoints.start()
        
        # Sawtooth scanner
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
        print(self.base_freqs, self.offset_freqs, self.setpoint_freqs)
    
    
    ###########################################################################
    ### FUNCTIONS FOR LASER BLUE 1 ############################################
    ###########################################################################           
    
    def get_spinBox(self, spinBox_name):
        return self.tab_3.findChild(QtWidgets.QDoubleSpinBox, spinBox_name)
    
    def get_label(self, label_name):
        return self.tab_3.findChild(QtWidgets.QLabel, label_name)
    
    ###########################################################################
    def lock_laser_on(self):
        laser_id = self.mainWindow.sender().property('laserID')
        lc.lock_laser_on(laser_id)                
        
    def lock_laser_off(self):
        laser_id = self.mainWindow.sender().property('laserID')
        lc.lock_laser_off(laser_id)
        
    def start_smooth_scan(self):
        laser_id = self.mainWindow.sender().property('laserID')
        if not self.smooth_change_flags[laser_id]:
            initial_offset = self.offset_freqs[laser_id]
            final_offset = self.get_spinBox(f'doubleSpinBox_nu_{laser_id}_smooth_want').value()
            change_time = self.get_spinBox(f'doubleSpinBox_nu_{laser_id}_smooth_delta_t').value()
            start_time = time.monotonic()
            self.smooth_change_params[laser_id] =  {'initial offset': initial_offset, 'final offset': final_offset, 'change time': change_time, 'start time': start_time}
            self.smooth_change_flags[laser_id] = True
        else:
            print('already scanning')
    
    def stop_smooth_scan(self):
        laser_id = self.mainWindow.sender().property('laserID')
        self.smooth_change_flags[laser_id] = False
        
    def base_freq_changed(self):
        laser_id = self.mainWindow.sender().property('laserID')
        self.base_freqs[laser_id] = self.mainWindow.sender().value()
    
    def offset_freq_changed(self):
        laser_id = self.mainWindow.sender().property('laserID')
        self.offset_freqs[laser_id] = self.mainWindow.sender().value()
    
    def k_p_changed(self):
        laser_id = self.mainWindow.sender().property('laserID')
        lc.lock_pars[laser_id]['k_p'] = self.mainWindow.sender().value()

    def k_i_changed(self):
        laser_id = self.mainWindow.sender().property('laserID')
        lc.lock_pars[laser_id]['k_i'] = self.mainWindow.sender().value()
        
    ###########################################################################   
        
    ###########################################################################      
    
    def update_plots(self):
        self.t_dependent_updates_laser('blue_1')
        self.t_dependent_updates_laser('blue_2')
        self.t_dependent_updates_laser_red_1()
        self.t_dependent_updates_laser_red_2()
    
    def update_setpoints(self):
        # smooth change updates offset
        for laser_id in self.smooth_change_flags:
            if self.smooth_change_flags[laser_id]:
                current_time = time.monotonic() - self.smooth_change_params[laser_id]['start time']
                change_time = self.smooth_change_params[laser_id]['change time']
                initial_offset = self.smooth_change_params[laser_id]['initial offset']
                final_offset = self.smooth_change_params[laser_id]['final offset']
                if current_time >= change_time:
                    new_offset = final_offset
                    self.smooth_change_flags[laser_id] = False
                else:
                    new_offset = initial_offset + (current_time/change_time)*(final_offset - initial_offset)
                offset_spinBox = self.get_spinBox(f'doubleSpinBox_{laser_id}_offset')
                offset_spinBox.setValue(new_offset)     # this will automatically change offset_freqs
                    
        
        self.setpoint_freqs['blue_1'] = self.base_freqs['blue_1']+self.offset_freqs['blue_1']*1e-6
        self.label_blue_1_setpoint.setText(f'{self.setpoint_freqs["blue_1"]:.7f}')
        lc.nu_setpoint['blue_1'] = self.setpoint_freqs['blue_1']
        
        self.setpoint_freqs['blue_2'] = self.base_freqs['blue_2']+self.offset_freqs['blue_2']*1e-6
        #self.label_blue_2_setpoint.setText(f'{self.setpoint_freqs["blue_2"]:.7f}')
        lc.nu_setpoint['blue_2'] = self.setpoint_freqs['blue_2']        
        
        
        
    def t_dependent_updates_laser(self, laser_id):
        self.get_label(f'label_nu_{laser_id}_is').setText(f'{lc.nu[laser_id]:.7f}')
                
        if laser_id == 'blue_2':
            lc.lock_pars[laser_id]['k_p'] = float(self.get_spinBox(f'doubleSpinBox_lock_{laser_id}_alpha').value())
            lc.lock_pars[laser_id]['k_i'] = float(self.get_spinBox(f'doubleSpinBox_lock_{laser_id}_beta').value())
        
        lock_status_label = self.get_label(f'label_lock_{laser_id}_status')
        if lc.lock_lasers[laser_id]:
            lock_status_label.setText('ON')
            lock_status_label.setStyleSheet('color: black')
        else:
            lock_status_label.setText('OFF')
            lock_status_label.setStyleSheet('color: red')
       
        try:
            self.plots[laser_id].plot(np.arange(500),lc.nu_history[laser_id][-500:],pen = blackPen, symbol = 'o', symbolBrush = blueBrush, name = f'nu_{laser_id}_was', clear = True)
        except Exception:
            pass
            
        #nu_blue_1_upper = pg.PlotCurveItem([0,500],[755.186881,755.186881],pen = bluePen)
        #nu_blue_1_lower = pg.PlotCurveItem([0,500],[755.186879,755.186879],pen = bluePen)
        #nu_blue_1_fill = pg.FillBetweenItem(nu_blue_1_upper,nu_blue_1_lower,blueBrush_alpha)
        
        #self.plot_nu_blue_1.addItem(nu_blue_1_upper)
        #self.plot_nu_blue_1.addItem(nu_blue_1_lower)
        #self.plot_nu_blue_1.addItem(nu_blue_1_fill)        
    ###########################################################################    
        


    ###########################################################################
    ### FUNCTIONS FOR LASER BLUE 2 ############################################
    ###########################################################################           
        
    ###########################################################################        
    def pushButton_smooth_change_laser_blue_2_start_clicked(self):
        lc.nu_blue_2_smooth_want = float(self.doubleSpinBox_nu_blue_2_smooth_want.value())
        lc.nu_blue_2_smooth_delta_t = float(self.doubleSpinBox_nu_blue_2_smooth_delta_t.value())
        lc.smooth_change_laser_blue_2_start()

    def pushButton_smooth_change_laser_blue_2_stop_clicked(self):
        lc.smooth_change_laser_blue_2_stop()
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