from tkinter import Tk, Label, Button, Entry, END, W, E, filedialog, PhotoImage
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Kmeans import Kmeans
from PreProcess import PreProcess

# The class of presenting the gui
class GUI:

    def __init__(self, master):
        self.master = master
        master.title("K Means Clustering")
        master.geometry('1300x700')

        self.btn = Button(master, text="Browse", command=lambda: self.browse(self.entry))
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

    # Check if the input is number or not
    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            return True

        try:
            int(new_text)
            return True
        except ValueError:
            return False

    # updating the entry of the path
    def browse(self, entry):
        Tk().withdraw()
        file_path = filedialog.askopenfilename()
        entry.insert(0, file_path)
        return

    # make instance of processed dataframe
    def preprocess(self, path):
        try:
            self.processing = PreProcess(path)
            messagebox.showinfo(title='K Means Clustering', message='Preprocessing completed successfully!')
        except:
            messagebox.showerror(title='K Means Clustering', message='There was an error with the path\'s file')

    # make instance of kmeans model and draw the prediction of groups
    def kmeans(self, dataframe, numOfClusters, numOfInit):
        try:
            # At start we try to make the input as int, and if we fail we exit
            numOfInit = int(numOfInit)
            numOfClusters = int(numOfClusters)
            if numOfClusters < 2:  # if clusters are less than 2 so there's a problem with the arguements
                raise Exception()
            # making a model and making the scatter and map
            model = Kmeans(dataframe, numOfClusters, numOfInit)
            model.draw()
            scatter_canvas = FigureCanvasTkAgg(model.scatter, master=self.master)
            scatter_canvas.get_tk_widget().grid(row=7, column=0, sticky=W)
            saved_map = PhotoImage(file="choropleth-map.png")
            map_as_image = Label(self.master, image=saved_map)
            map_as_image.image = saved_map
            map_as_image.grid(row=7, column=1, sticky=W)
            messagebox.showinfo(title="K Means Clustering", message="Finished clustering")
        except:
            messagebox.showerror(title='K Means Clustering', message='There was an error with the variables')

# main that we run that creates instance of gui


root = Tk()
my_gui = GUI(root)
root.mainloop()
