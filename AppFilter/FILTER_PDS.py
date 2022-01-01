"""
Created on 3 13:27:05 2021
@author: MBI
"""
# Modulos
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk,Menu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import os
from Filtros_backend import Filters

# Clases

class Tooltip():
    def __init__(self, widget, tip_text=None):
        self.widget = widget
        self.tip_text = tip_text
        widget.bind("<Enter>", self.mouse_enter)
        widget.bind("<Leave>", self.mouse_leave)
      
    def mouse_enter(self,_event):
        self.show_tooltip()

    def mouse_leave(self,_event):
        self.hide_tooltip()

    def show_tooltip(self):
        if self.tip_text:
            x_left = self.widget.winfo_rootx()
            y_top = self.widget.winfo_rooty() - 15
            self.tip_window = tk.Toplevel(self.widget)
            self.tip_window.overrideredirect(True)
            self.tip_window.geometry("+%d+%d" % (x_left, y_top))
            label = tk.Label(self.tip_window, text=self.tip_text, justify=tk.LEFT, background="#FFFFe0",
                             relief=tk.SOLID,
                             borderwidth=1, font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)

    def hide_tooltip(self):
        if self.tip_window:
            self.tip_window.destroy()


class FilterGUI():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title(" Aplicacion ")
        self.win.iconbitmap("Python.ico")
        self.win.geometry("728x450")
        self.win.resizable(True,True)
        self.backedFilter = Filters()
        self.listFilters = [
            "Chebyshev_ord1",
            "Butterworth",
            "Kaiser"]
        self.path = "C:/Users/"+os.getlogin()+'/Documents'
        self.create_widget()

    def create_widget(self):
        menu_bar = Menu(master=self.win)
        self.win.config(menu=menu_bar)
        file_menu = Menu(menu_bar,tearoff=0)
        file_menu.add_command(label='Sobre',command=self.credict)
        file_menu.add_command(label='Informacion',command=self.info)
        menu_bar.add_cascade(label='Ayuda',menu=file_menu)
        

        tabcontrol = ttk.Notebook(self.win)
        tab = ttk.Frame(tabcontrol)
        tabcontrol.add(tab, text='Filtros Digitales')
        self.tab_graf = ttk.Frame(tabcontrol)
        tabcontrol.add(self.tab_graf,text='Graficos')
        tabcontrol.pack(expand=1,fill='both')

        subwin_1 = ttk.Labelframe(tab, text="Filtro")
        subwin_1.grid(column=0, row=0, sticky='WE',padx=10,pady=5)
        subwin_2 = ttk.Labelframe(tab,text='Variables')
        subwin_2.grid(column=0,row=2,sticky='WE',padx=10,pady=5)
        subwin_3 = ttk.Labelframe(tab,tex='Resultados')
        subwin_3.grid(column=0,row=3,sticky='WE',padx=10,pady=5)

        # Seleccion del Metodo y del Filtro
        ttk.Label(subwin_1, text="Seleccione Filtro").grid(column=0, row=0, sticky="W",padx=20,pady=2)  # Etiqueta de seleccion filtro
        self.filterstring = tk.StringVar()
        self.selectedFilter = ttk.Combobox(subwin_1, textvariable=self.filterstring, width=20, value=self.listFilters,state='readonly')
        self.selectedFilter.grid(column=0, row=1, sticky="W",padx=20,pady=2)

        ttk.Label(subwin_1,text='Seleccione metodo').grid(column=2,row=0,sticky='W',padx=20,pady=2) # Etiqueta de seleccion del metodo
        self.metodostring = tk.StringVar()
        self.selectedMetodo = ttk.Combobox(subwin_1, textvariable=self.metodostring,width=20, value=['bilineal','invarianza','ventana'],state='readonly')
        self.selectedMetodo.grid(column=2,row=1,sticky='W',padx=20,pady=2)
        Tooltip(self.selectedMetodo,"El metodo de ventana solo es utilizado para los diseños de ventana")

        # Variables a introducir
        self.freq = tk.StringVar()
        self.freq.set('10.0')
        selectedFreq = tk.Entry(subwin_2, textvariable=self.freq,width=10)
        selectedFreq.grid(column=0,row=0,sticky='E',pady=2,padx=1)
        Tooltip(selectedFreq,"Frecuencia de muestreo")
    
        self.scala = tk.StringVar()
        self.scala.set('Hz')
        selectedScala = ttk.Combobox(subwin_2, textvariable=self.scala,width=5,value=['Hz','KHz','MHz','GHz'])
        selectedScala.grid(column=1,row=0,sticky='W',pady=2)
        Tooltip(selectedScala,'Escala de frecuencia')
        
        self.atenuation_0 = tk.StringVar()
        self.atenuation_0.set('1.0')
        selectAte0 = tk.Entry(subwin_2,textvariable=self.atenuation_0,width=10)
        selectAte0.grid(column=2,row=0,sticky='E',padx=20,pady=2)
        Tooltip(selectAte0,'Atenuación en banda de paso')
        
        self.atenuation_1 = tk.StringVar()
        self.atenuation_1.set('12.0')
        selectAte1 = tk.Entry(subwin_2,textvariable=self.atenuation_1,width=10)
        selectAte1.grid(column=3,row=0,sticky='E',padx=20,pady=2)
        Tooltip(selectAte1,'Atenuación en banda de atenuación')
        
        self.freqAngularCorte = tk.StringVar()
        self.freqAngularCorte.set('0.10')
        selectedFreqAngularCorte = tk.Entry(subwin_2,textvariable=self.freqAngularCorte,width=10)
        selectedFreqAngularCorte.grid(column=4,row=0,sticky='E',padx=20,pady=2)
        Tooltip(selectedFreqAngularCorte,'Seleccione valor para multiplicar por pi (frec angular corte [radianes])')
        
        self.freqAngularAten = tk.StringVar()
        self.freqAngularAten.set('0.143')
        selectedFreqAngularAten = tk.Entry(subwin_2,textvariable=self.freqAngularAten,width=10)
        selectedFreqAngularAten.grid(column=5,row=0,sticky='E',padx=20,pady=2)
        Tooltip(selectedFreqAngularAten,'Selecione valor para multiplicar por pi (frec angular atenuación [radianes])')

        # Calcular filtro
        action  = ttk.Button(subwin_2,text='Calcular',command=self.operations,width=10)
        action.grid(column=0,row=3,sticky='W',pady=10,padx=20)

        self.scroll = scrolledtext.ScrolledText(subwin_3,width=80,height=8,wrap=tk.WORD)
        self.scroll.grid(column=0,row=0,columnspan=1,sticky='WE',padx=20,pady=2)
        Tooltip(self.scroll,'Obtencion de los coeficientes del calculo')

        save = ttk.Button(subwin_3,text='Guardar',command=self.save,width=10)
        save.grid(column=0,row=1,sticky='W',padx=20,pady=2)
        clean = ttk.Button(subwin_3,text='Limpiar',command=self.clean,width=10)
        clean.grid(column=0,row=2,sticky='W',padx=20,pady=2)


    def info(self):
        return messagebox.showinfo('',message="""
        Amplicación para el diseño de filtros digitales
        a partir de un modelo analógico se obtiene un 
        modelo digital con domineo en el plano Z.
        Los valores  de las frecuencias  de conrte y 
        atenuación son en radianes, solo se introduce 
        el valor por el cual se multiplicará pi.
        """)

    def credict(self):
        return messagebox.showinfo('', message="""
        Creado: 3/8/2021
        Auto: MBI
        Licencia: Software de codigo abierto
        Contacto: maikel8807@gmail.com
        Version: 1.0.0
        Derechos Reservados
        """)
        
    def operations(self):
        # Filtrado de variables
        dictScala = {"Hz": 1,"KHz": 1e3,"MHz": 1e6,'GHz': 1e9}
        try:
            if (self.freq.get() == '0' or self.freqAngularAten.get() == '0' or self.freqAngularCorte.get() == '0'
                        or self.atenuation_0.get() == '0' or self.atenuation_1.get() == '0'):
                            self.freq.set('Error')
                            
            freq = abs(float(self.freq.get()))
            freqAngAte = abs(float(self.freqAngularAten.get()))
            freAngCort = abs(float(self.freqAngularCorte.get()))
            Ate0 = abs(float(self.atenuation_0.get()))
            Ate1 = abs(float(self.atenuation_1.get()))
            scala = dictScala[self.scala.get()]
            fs = freq * scala
            self.backedFilter.__setitem__([fs,Ate0,Ate1,freqAngAte,freAngCort])
            if  (self.filterstring.get() is not  None and self.metodostring.get() is not  None):
    
                if (self.filterstring.get() == 'Chebyshev_ord1' and self.metodostring.get() == 'bilineal'):w,H = self.backedFilter.checkbyshev1_bilineal()
                elif (self.filterstring.get() == 'Chebyshev_ord1' and self.metodostring.get() == 'invarianza'):w,H = self.backedFilter.checkbyshev1_invar()
                elif (self.filterstring.get() == 'Butterworth' and self.metodostring.get() == 'bilineal'):w,H = self.backedFilter.butterworth_bilineal()
                elif (self.filterstring.get() == 'Butterworth' and self.metodostring.get() == 'invarianza'):w,H = self.backedFilter.butterworth_invar()
                elif (self.filterstring.get() == 'Kaiser' and self.metodostring.get() == 'ventana'):w,H = self.backedFilter.kaiser()
    
                variables = self.backedFilter.__getitem__()  # self._freq,self._A0,self._A1,self._Wc,self._Wa,self._T,self.Bz,self.Az
                if (w is not None and H is not None):
                    self.scroll.insert(tk.INSERT,"Modelo: " + self.filterstring.get() + '\n' + 'Metodo: ' + self.metodostring.get() + '\n' +\
                                       "Fs: " + str(freq) + ' ' + self.scala.get() + '\n'
                                        "Atenuacion 0: " + str(variables[1]) + ' ' + 'dB' + '\n'
                                        "Atenuacion 1: " + str(variables[2]) + ' ' + 'dB' + '\n'
                                        "Wc: " + str(variables[3]) + ' ' + 'radianes/s' + '\n'
                                        "Wa: " + str(variables[4]) + ' ' + 'radianes/s' + '\n'
                                        "Ts: " + str(variables[5]) + ' ' + 'seg' + '\n'
                                        "Numerador (Bz): " + str(variables[6]) + '\n'
                                      "Denominador (Az): " + str(variables[7]) + '\n')

                    self.showGraf(w,H)
            else:
                    messagebox.showwarning('Advertencia', message='Seleccione modelo y metodo a usar')
        except:
            messagebox.showerror('Error','Hay valores erróneos')


    def save(self):
        # Metodo para guardar los coeficientes y las graficas
        if self.figure is None:
            return messagebox.showwarning('Alerta', message='Para guardar datos,primero tiene que crearlos')
        try:
            self.figure.savefig(self.path+'/'+self.filterstring.get()+'_'+self.metodostring.get()+'.jpg',dpi=100,format='jpg')

            with open(self.path+'/'+self.filterstring.get()+'_'+self.metodostring.get()+'.txt','w') as txtFile:
                txtFile.write(self.scroll.get('1.0',tk.END))

            txtFile.close()
            messagebox.showinfo('Informacion','Datos gaurdados en Documentos!')
        except:
            messagebox.showerror('Error', message='No se pudo guardar datos,revise proteccion de carpetas en el antivirus')

    def clean(self):
        # Metodo para limpiar el scroll
        self.scroll.delete('1.0', tk.END) # Borrar texto
        self.canvas.get_tk_widget().destroy() # Limpiar imagen


    def showGraf(self,w,H):
        self.figure = plt.figure(figsize=(12,8),facecolor='white')
        axis_1 = self.figure.add_subplot(121)
        axis_2 = self.figure.add_subplot(122)
        plt.suptitle(self.filterstring.get()+' '+self.metodostring.get())
        axis_1.set_title('H(z)')
        axis_1.plot(w,20*np.log10(np.abs(H)),color='r')
        axis_1.set_xlabel('W [radianes/s]')
        axis_1.set_ylabel('Amplitud [dB]',rotation=90)
        axis_1.grid(linestyle='-')

        axis_2.set_title('Fase (z)')
        axis_2.plot(w,np.unwrap(np.angle(H)),color='b')
        axis_2.set_xlabel("W [radianes/s]")
        axis_2.set_ylabel('Angulo [radianes]',rotation=90)
        axis_2.grid(linestyle='-')
        self.canvas = FigureCanvasTkAgg(self.figure,master=self.tab_graf)
        self.canvas.get_tk_widget().pack(side='top',fill='both',expand=True)


if __name__ == '__main__':
    win  = FilterGUI()
    win.win.mainloop()



