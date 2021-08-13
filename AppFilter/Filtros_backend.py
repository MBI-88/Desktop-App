"""
Created on Sat Jul 31 11:17:55 2021

@author: MBI
"""
import scipy.signal as sg 
import numpy as np 
import PyDynamic.misc as mic
# Clases

class Filters():
    def __init__(self):
        # Protected
        self._freq = 0
        self._A0 = 0
        self._A1 = 0
        self._Wc = 0
        self._Wa = 0
        self._T = 0
        # globals
        self.Bz,self.Az = 0,0

    def __getitem__(self):
        return self._freq,self._A0,self._A1,self._Wc,self._Wa,self._T,self.Bz,self.Az
    
    def __setitem__(self,args):
        self._freq = args[0]
        self._A0 = args[1]
        self._A1 = args[2]
        self._Wa = np.pi * args[3]
        self._Wc = np.pi * args[4]
        try:
            self._T = 1/self._freq
        except:
            self._T = 1

    
    def checkbyshev1_bilineal(self):
        Ohc = (2/self._T) * np.tan(self._Wc/2)
        Oha = (2/self._T) * np.tan(self._Wa/2) 
        
        Ohnc = Ohc/Ohc
        Ohna = Oha/Ohc
        
        N,Wn = sg.cheb1ord(Ohnc,Ohna,self._A0,self._A1,True)
        B,A = sg.cheby1(N,self._A1,Wn,analog=True)
        
        self.Bz,self.Az = sg.bilinear(B,A,fs=self._freq)
        w,H = sg.freqz(self.Bz,self.Az)
        return w,H

    def checkbyshev1_invar(self):
        Ohc = self._Wc/self._T
        Oha = self._Wa/self._T

        Ohnc = Ohc/Ohc
        Ohna = Oha/Ohc
        
        N,Wn = sg.cheb1ord(Ohnc,Ohna,self._A0,self._A1,True)
        B,A = sg.cheby1(N,self._A1,Wn,analog=True)

        self.Bz,self.Az = mic.impinvar(B,A,fs=self._freq)
        w,H = sg.freqz(self.Bz,self.Az)
        return w,H

    def butterworth_invar(self):
        
        Ohc = self._Wc/self._T
        Oha = self._Wa/self._T    

        Ohnc = Ohc/Ohc
        Ohna = Oha/Ohc

        N,Wn = sg.buttord(Ohnc,Ohna,self._A0,self._A1,analog=True)
        B,A = sg.butter(N,Wn,analog=True)
        
        self.Bz,self.Az = mic.impinvar(B,A,fs=self._freq)
        w,H = sg.freqz(self.Bz,self.Az)
        return w,H
        
        
    def butterworth_bilineal(self):
        Ohc = (2/self._T) * np.tan(self._Wc/2)
        Oha = (2/self._T) * np.tan(self._Wa/2) 
        
        Ohnc = Ohc/Ohc
        Ohna = Oha/Ohc
        
        N,Wn = sg.buttord(Ohnc,Ohna,self._A0,self._A1,analog=True)
        B,A = sg.butter(N,Wn,analog=True)

        self.Bz,self.Az = sg.bilinear(B,A,fs=self._freq)

        w,H = sg.freqz(self.Bz,self.Az)
        return w,H

    def kaiser(self):
        fc = self._Wc / (2 * np.pi)
        fa = self._Wa / (2 * np.pi)
        whidth = fa - fc

        N,B = sg.kaiserord(self._A1, whidth / (0.5 * self._freq))
        taps = sg.firwin(N, fc, window=("kaiser", B), scale=False, nyq=0.5 * self._freq)
        w,H = sg.freqz(taps, worN=8000)
        return w,H





            
        
    
    
    
        
       
           
            
       
            
            



    
        

