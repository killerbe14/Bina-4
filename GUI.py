from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, filedialog, PhotoImage
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Kmeans import Kmeans
from PreProcess import PreProcess


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("GUI")
        master.geometry('1024x700')

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        #######################################################################################################

        self.btn = Button(master, text="Browse file", command=lambda: self.browse(self.entry))
        self.entry = Entry(master, width=50)
        vcmd = master.register(self.validate)  # we have to wrap the command
        self.cluster_label = Label(master, text="Number of clusters k")
        self.entry2 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.number_runs = Label(master, text="Number of runs")
        self.entry3 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.pre_process_btn = Button(master, text="Pre-process", command=lambda: self.preprocess(self.entry.get()))
        self.cluster = Button(master, text="Cluster", command=lambda: self.kmeans(self.processing.countriesDataFrame, self.entry2.get(), self.entry3.get()))

        # LAYOUT
        self.entry.grid(row=0, column=0, columnspan=6, sticky=W + E)
        self.btn.grid(row=0, column=7, columnspan=2, sticky=W + E)
        self.cluster_label.grid(row=1, column=0)
        self.entry2.grid(row=1, column=2, sticky=W + E)
        self.number_runs.grid(row=2, column=0)
        self.entry3.grid(row=2, column=2, sticky=W + E)
        self.pre_process_btn.grid(row=4, column=0)
        self.cluster.grid(row=4, column=2)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

    def browse(self, entry):
        Tk().withdraw()
        file_path = filedialog.askopenfilename()
        entry.insert(0, file_path)
        return

    def preprocess(self, path):
        try:
            self.processing = PreProcess(path)
            messagebox.showinfo(title='Done', message='PreProcessing Finished')
        except:
            messagebox.showerror(title='Error', message='There was an error with the path\'s file')

    def kmeans(self, dataframe, numOfClusters, numOfInit):
        try:
            numOfInit = int(numOfInit)
            numOfClusters = int(numOfClusters)
            model = Kmeans(dataframe, numOfClusters, numOfInit)
            model.draw()
            scatter_canvas = FigureCanvasTkAgg(model.scatter, master=self.master)
            #scatter_canvas.draw()
            scatter_canvas.get_tk_widget().grid(row=7, column=0, sticky=W)
            saved_map = PhotoImage(file="choropleth-map.png")
            map_as_image = Label(self.master, image=saved_map)
            map_as_image.image = saved_map
            map_as_image.grid(row=7, column=1, sticky=W)
        except:
            messagebox.showerror(title='Error', message='There was an error with the variables')



root = Tk()
my_gui = GUI(root)
root.mainloop()
