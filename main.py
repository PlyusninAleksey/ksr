import matplotlib.figure
import numpy as np
import rk2
from tkinter import *
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#линейная система ДУ
A = np.array([[-500.005, 499.995],
              [499.995, -500.005]])


#создание окна и вкладок
root = Tk()     
root.title("КСР жёсткие системы")     
root.geometry("1280x720")    

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Таблица')

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='График v1 и v2')

tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='График E1 и E2')

tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='График v1 и u1')

tab5 = ttk.Frame(tab_control)
tab_control.add(tab5, text='График v2 и u2')

tab6 = ttk.Frame(tab_control)
tab_control.add(tab6, text='Справка')

tab_control.pack(expand=1, fill='both')

# #разметка грида
# for c in range(6): root.columnconfigure(index=c, weight=1)
# root.columnconfigure(index=6, weight=0)
# for r in range(80): root.rowconfigure(index=r, weight=1)

inputframe = ttk.Frame(tab1)
inputframe.pack(pady=10)

#надписи для начальных условий
xLabel = ttk.Label(inputframe, text="Начальное условие для x", font=("Arial", 11))
u01Label = ttk.Label(inputframe, text="Начальное условие для u1", font=("Arial", 11))
u02Label = ttk.Label(inputframe, text="Начальное условие для u2", font=("Arial", 11))
hLabel = ttk.Label(inputframe, text="Начальный шаг h", font=("Arial", 11))
HgrLabel = ttk.Label(inputframe, text="Правая граница для x", font=("Arial", 11))
nMaxLabel = ttk.Label(inputframe, text="Макс. количество шагов", font=("Arial", 11))
EgrLabel = ttk.Label(inputframe, text="Контроль выхода за гр.", font=("Arial", 11))
EpsLabel = ttk.Label(inputframe, text="Контроль локальной погр.", font=("Arial", 11))

#начальне условия
x0 = DoubleVar(value = 0.0)
u01 = DoubleVar(value = 7.0)
u02 = DoubleVar(value = 13.0)
h = DoubleVar(value = 0.01)
Hgr = DoubleVar(value = 750)
Nmax = IntVar(value = 30000)
Egr = DoubleVar(value = 0.1)
Eps = DoubleVar(value= 0.001)
typeOfMethod = IntVar()

#поле ввода начальных условий
xEntry = ttk.Entry(inputframe, textvariable=x0)
u01Entry = ttk.Entry(inputframe, textvariable=u01)
u02Entry= ttk.Entry(inputframe, textvariable=u02)
hEntry = ttk.Entry(inputframe, textvariable=h)
HgrEntry = ttk.Entry(inputframe, textvariable=Hgr)
NmaxEntry = ttk.Entry(inputframe, textvariable=Nmax)
EgrEntry = ttk.Entry(inputframe, textvariable=Egr)
EpsEntry = ttk.Entry(inputframe, textvariable=Eps)
typeButton = ttk.Checkbutton(inputframe, text="С контролем локальной погрешности?", variable=typeOfMethod, offvalue=0, onvalue=1)

#вывод кнопок
xLabel.grid(row=0, column=0, padx=5, pady=5)
xEntry.grid(row=0, column=1, padx=5, pady=5)
u01Label.grid(row=0, column=2, padx=5, pady=5)
u01Entry.grid(row=0, column=3, padx=5, pady=5)
u02Label.grid(row=0, column=4, padx=5, pady=5)
u02Entry.grid(row=0, column=5, padx=5, pady=5)
hLabel.grid(row=0, column=6, padx=5, pady=5)
hEntry.grid(row=0, column=7, padx=5, pady=5)
HgrLabel.grid(row=1, column=0, padx=5, pady=5)
HgrEntry.grid(row=1, column=1, padx=5, pady=5)
nMaxLabel.grid(row=1, column=2, padx=5, pady=5)
NmaxEntry.grid(row=1, column=3, padx=5, pady=5)
EgrLabel.grid(row=1,column=4, padx=5, pady=5)
EgrEntry.grid(row=1,column=5, padx=5, pady=5)
EpsLabel.grid(row=1,column=6, padx=5, pady=5)
EpsEntry.grid(row=1, column=7, padx=5, pady=5)
typeButton.grid(row=2,column=0, padx=5, pady=5)

#вывод таблицы
frameTable = ttk.Frame(tab1)
frameTable.pack(expand=True, fill='both')

#колонки для таблицы
column = ("№","x","h", "v1", "v2", "E1", "E2", "ОЛП")
table = ttk.Treeview(frameTable, columns=column, show="headings")

#определяем заголовки
table.heading("№", text="№")
table.heading("x", text="x")
table.heading("h", text="h")
table.heading("v1", text="v1")
table.heading("v2", text="v2")
table.heading("E1", text="E1")
table.heading("E2", text="E2")
table.heading("ОЛП", text="ОЛП")


table.column("№", width = 10)
table.column("x" ,width = 50)
table.column("h", width=50)
table.column("v1", width = 242)
table.column("v2", width = 242)
table.column("E1", width = 242)
table.column("E2", width = 242)
table.column("ОЛП", width = 242)

#добавление прокрутки
scrollbar = ttk.Scrollbar(frameTable,orient=VERTICAL, command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

table.pack(side=LEFT, expand=True, fill='both')
scrollbar.pack(side=RIGHT, fill='y')


#создание графиков
fig1 = plt.Figure(figsize=(5,5), dpi=100)
ax1 = fig1.add_subplot(111)

canvas1 = FigureCanvasTkAgg(fig1, master=tab2)
canvas1.draw()
canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

#E1 и E2
fig2 = plt.Figure(figsize=(5,5), dpi=100)
ax2 = fig2.add_subplot(111)

canvas2 = FigureCanvasTkAgg(fig2, master=tab3)
canvas2.draw()
canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

#v1 и u1
fig3 = plt.Figure(figsize=(5,5), dpi=100)
ax3 = fig3.add_subplot(111)

canvas3 = FigureCanvasTkAgg(fig3, master=tab4)
canvas3.draw()
canvas3.get_tk_widget().pack(fill=BOTH, expand=True)

#v2 и u2
fig4 = plt.Figure(figsize=(5,5), dpi=100)
ax4 = fig4.add_subplot(111)

canvas4 = FigureCanvasTkAgg(fig4, master=tab5)
canvas4.draw()
canvas4.get_tk_widget().pack(fill=BOTH, expand=True)

#справка
spravka = Text(tab6, wrap=WORD, height=50, width=100)
spravka.pack(pady=10)


#обработка нажатия кнопки
def button_click(event):
    #удаляем прошлые значения таблицы
    table.delete(*table.get_children())

    #вычисляем численную траекторию
    x, v1, v2, Olp, hList = (rk2.rk2WithoutControl if (typeOfMethod.get()==0) else rk2.rk2WithControl)(x0.get(), [u01.get(),u02.get()], h.get(), A, Hgr.get(), Nmax.get(),Egr.get(), Eps.get())

    u1, u2 = rk2.getTrueSolution(x, x0.get(), u01.get(), u02.get())

    e1 = u1 - v1
    e2 = u2 - v2

    #v1 и v2
    ax1.clear()
    ax1.set_title('v1 и v2')
  
    ax1.plot(x, v1, '-rh',label='u1')
    ax1.plot(x, v2, '-gv',label='u2')
    ax1.grid(color='b', linewidth=1.0)
    ax1.legend(fontsize=12)
    canvas1.draw()

    #E1 и E2
    ax2.clear()
    ax2.set_title('E1 и E2')
  
    ax2.plot(x, e1, '-rh',label='E1')
    ax2.plot(x, e2, '-gv',label='E2')
    ax2.grid(color='b', linewidth=1.0)
    ax2.legend(fontsize=12)
    canvas2.draw()

    #v1 и u1
    ax3.clear()
    ax3.set_title('v1 и u1')
  
    ax3.plot(x, v1, '-',label='v1',color='red')
    ax3.plot(x, u1, '--',label='u1', color='green' )
    ax3.grid(color='b', linewidth=1.0)
    ax3.legend(fontsize=12)
    canvas3.draw()

    #v2 и u2
    ax4.clear()
    ax4.set_title('v2 и u2')
  
    ax4.plot(x, v2, '-',label='v2',color='red')
    ax4.plot(x, u2, '--',label='u2', color='green' )
    ax4.grid(color='b', linewidth=1.0)
    ax4.legend(fontsize=12)
    canvas4.draw()

    #заполнение таблицы
    for i in range(x.shape[0]):
        table.insert("",END,values=(i,x[i], hList[i],v1[i],v2[i],e1[i],e2[i], Olp[i]))

    spravka.delete(1.0, END)
    maxElement1 = np.max(np.abs(e1))
    maxElement2 = np.max(np.abs(e2))
    indexE1 = np.where(np.abs(e1) == maxElement1)
    indexE2 = np.where(np.abs(e2) == maxElement2)
    spravka.insert(END,f"Количество шагов: {x.shape[0]}\n")
    spravka.insert(END,f"Численная траектория ушла из ({v1[0]},{v2[0]}) и пришла в ({v1[v1.shape[0]-1]},{v2[v2.shape[0]-1]})\n")
    spravka.insert(END, f"Максимальная гобальная погрешность E1: {maxElement1} , при x = {x[indexE1[0]]}\n")
    spravka.insert(END, f"Максимальная глобальная погрешность E2: {maxElement2} , при x = {x[indexE2[0]]}\n")






#установка кнопки
btn = ttk.Button(tab1,text="Начать вычисление")
btn.pack(ipady=8, fill=X)

#привязываем к кнопке
btn.bind("<ButtonPress>", button_click)



root.mainloop()



