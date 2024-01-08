from tkinter import *
import pandas as ps
import numpy as np
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

filepath = False
read = False
colnames = [False]
res = False
count = 0
left = False
right = False
entry1 = False
entry2 = False
onentry = False

# To read the file on the system
def readFile():
    global filepath, read, colnames, res, count
    try:
        filepath = filedialog.askopenfilename() 
        read = ps.read_csv(filepath)
        colnames = list(read.columns)
        res = True
        start()
    except ValueError:
        print("Please reselect the file")

# To take input of URL of the online CSV file and then calls insertOnline()
def readOnline():
    global onentry
    frame = Frame(window)
    frame.pack()
    onentry = Entry(frame,
                width = 100,
                font = ("JetBrains Mono", 16))
    onentry.grid(row = 0, column = 1, pady = 2)
    
    onBtn = Button(frame,
                    text = "Load Variable",
                    font = ("JetBrains Mono", 16),
                    command = insertOnline)
    onBtn.grid(row = 1, column = 1, pady = 5)

# Goes to the url and reads the CSV file
def insertOnline():
    global entry1, entry2, res, filepath, read
    win = Toplevel()
    frame = Frame(win)
    frame.pack()
    try:
        filepath = onentry.get()
        read = ps.read_csv(filepath)
        res = True
        colnames = list(read.columns)
        rownum = 0 
        for names in colnames: # Creating the label
            Label(frame,
                    text = names,
                    font = ("JetBrains Mono", 16)).grid(row = rownum, column = 0, pady = 2)
            rownum += 1
        entry1 = Entry(frame,
                       font = ("JetBrains Mono", 16))
        entry1.grid(row = rownum + 1, column = 0, pady = 2)
        entry2 = Entry(frame,
                       font = ("JetBrains Mono", 16))
        entry2.grid(row = rownum + 2, column = 0, pady = 2)
        loadBtn = Button(frame,
                         text = "Load Variable",
                         font = ("JetBrains Mono", 16),
                         command = load)
        loadBtn.grid(row = rownum + 3, column = 0, pady = 10)
    except:
        print("Some Error Occurred!")

# Initialises the window, frame and plotting area
def initializer():
    window = Toplevel() # Creates a toplevel window
    frame = Frame(window) # Creates a frame
    fig = Figure(figsize = (25, 12), # Creates a Figure type object to store the figure.
                 dpi = 100)
    plot = fig.add_subplot(111) # Adds axes to the figure
    return window,frame,fig,plot # Returning everything created

# Loads the function load to load the file on the system
def start():
    global entry1, entry2
    win = Toplevel()
    frame = Frame(win)
    frame.pack()
    rownum = 0
    for names in colnames: # Creating the label
        Label(frame,
                text = names,
                font = ("JetBrains Mono", 16)).grid(row = rownum, column = 0, pady = 2)
        rownum += 1
    entry1 = Entry(frame,
                       font = ("JetBrains Mono", 16))
    entry1.grid(row = rownum + 1, column = 0, pady = 2)
    entry2 = Entry(frame,
                       font = ("JetBrains Mono", 16))
    entry2.grid(row = rownum + 2, column = 0, pady = 2)
    loadBtn = Button(frame,
                         text = "Load Variable",
                         font = ("JetBrains Mono", 16),
                         command = load)
    loadBtn.grid(row = rownum + 3, column = 0, pady = 10)

# Loads the variable in the left and right
def load():
    global left, right
    left = entry1.get()
    right = entry2.get()
    print(left , right)


# Bar Plot
def barPlot():
    try:
        if res:
            bar_window ,bar_frame ,bar_fig, bar_plot = initializer()
            bar_frame.pack() # Packing the returned frame
            Label(bar_frame, text = "Bar Plot").pack()
            first = read[left]
            second = read[right]
            bar_plot.bar(first, second) # Actual plotting
            chart = FigureCanvasTkAgg(bar_fig, bar_frame) # Merging the fig and frame as one
            chart.get_tk_widget().pack() # Placing the above merged object on the window.
        else:
            readFile()
            barPlot()
    except Exception as e:
            print(e)

# Pie Plot
def piePlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Pie Plot").pack()
            read_1 = read.dropna().reset_index(drop = True) # Dropped all the NaN's from the read dataframe and assingned to read_1
            first = read_1[left]
            second = read_1[right] #np.floor(ps.to_numeric(read[right], errors='coerce')).astype('Int64')
            plot.pie(second, radius = 1.4, labels = first, autopct = '%1.01f%%')
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else:             
            readFile()
            piePlot() 
    except Exception as e:
            print(e)

# Line Plot
def linePlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Line Plot").pack()
            agg_data = read.groupby(left)[right].mean()
            plot.plot(agg_data.index, agg_data.values, marker = "o", linestyle = "-")
            plot.grid(True)
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else: 
            readFile()
            linePlot()
    except Exception as e:
            print(e)

# Histogram Plot
def histogramPlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Histogram Plot").pack()        
            plot.hist(read[left], bins = 15, edgecolor = "black")
            plot.grid(True)
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else: 
            readFile()
            histogramPlot()
    except Exception as e:
            print(e)

# Scatter Plot
def scatterPlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Scatter Plot").pack()
            plot.scatter(read[left], read[right])
            plot.grid(True)
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else: 
            readFile()
            scatterPlot()
    except Exception as e:
            print(e)
        
# Box Plot
def boxPlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Box Plot").pack()
            plot.boxplot(read[right])
            plot.grid(True)
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else: 
            readFile()
            boxPlot()
    except Exception as e:
            print(e)

# Stair plot
def stairPlot():
    try:
        if res:
            window, frame, fig, plot = initializer()
            frame.pack()
            Label(frame, text = "Stair Plot").pack()
            plot.stairs(read[right], linewidth = 2)
            plot.grid(True)
            chart = FigureCanvasTkAgg(fig, frame)
            chart.get_tk_widget().pack()
        else: 
            readFile()
            stairPlot()
    except Exception as e:
            print(e)

# Main ----

# Creating the window
window = Tk()

# Photo frame and photo
photoFrame = Frame(window)
icon = PhotoImage(file = "images/archcraft.png")
intro_label = Label(photoFrame,
                   text = "DWM Project",
                   font = ("JetBrains Mono Nerd Font", 16),  
                   compound = BOTTOM)
motto_label = Label(photoFrame,                   
                   text =  "VIT",
                   font = ("JetBrains Mono Nerd Font", 16),
                   pady = 5,
                   compound = BOTTOM)
icon_label  = Label(window,                   
                   text =  "The Plotter",
                   font = ("JetBrains Mono Nerd Font", 16),
                   pady = 15,
                   image = icon,
                   compound = BOTTOM)
intro_label.pack()
motto_label.pack()
icon_label.pack()
photoFrame.pack(pady = 20)


# Frame to put the buttons
btnFrame = Frame(window)
btnFrame.pack(pady = 20)
# Frame to put the file button
fileFrame = Frame(window)
fileFrame.pack()
# Label Frame
labelFrame = Frame(window)
labelFrame.pack()


# Buttons
barBtn =  Button(btnFrame,
                 text = "Bar",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = barPlot)
pieBtn =  Button(btnFrame,
                 text = "Pie",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = piePlot)
lineBtn = Button(btnFrame,
                 text = "Line",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = linePlot)
histBtn = Button(btnFrame,
                 text = "Hist",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = histogramPlot)
scatBtn = Button(btnFrame,
                 text = "Scatter",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = scatterPlot)
boxBtn = Button(btnFrame,
                 text = "Box",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = boxPlot)
stairBtn = Button(btnFrame,
                 text = "Stair",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = stairPlot)

readBtn = Button(fileFrame,
                 text = "open file",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = readFile)

onlineBtn = Button(fileFrame,
                 text = "read online",
                 font = ("JetBrains Mono Nerd Font", 18),
                 width = 10,
                 command = readOnline)
                 

# Placing the buttons on the window
barBtn.grid(row = 0, column = 0, padx = 2)
pieBtn.grid(row = 0, column = 1, padx = 2)
lineBtn.grid(row = 0, column = 2, padx = 2)
histBtn.grid(row = 0, column = 3, padx = 2)
scatBtn.grid(row = 0, column = 4, padx = 2)
boxBtn.grid(row = 0, column = 5, padx = 2)
stairBtn.grid(row = 0, column = 6, padx = 2)
readBtn.grid(row = 0, column = 2, padx = 4, pady = 4)
onlineBtn.grid(row = 0, column = 3, padx = 4, pady = 4)

window.mainloop()
