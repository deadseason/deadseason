import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import colorchooser
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Mouse Paint")
        self.master.geometry("800x600")

        # create canvas
        self.fig = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        # self.ax.set_title("Mouse Paint")#绘图标题，而不是窗口标题
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)

        # create toolbar
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # create color menu
        self.color_var = tk.StringVar()
        self.color_var.set("black")
        self.color_menu = ttk.OptionMenu(self.toolbar, self.color_var, "black", "black", "red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "white")
        self.color_menu.pack(side=tk.LEFT, padx=5)

        # create line width menu
        self.width_var = tk.StringVar()
        self.width_var.set("1")
        self.width_menu = ttk.OptionMenu(self.toolbar, self.width_var, "1", "2", "3", "4", "5")
        self.width_menu.pack(side=tk.LEFT, padx=5)

        # create range input
        self.range_frame = ttk.Frame(self.toolbar)
        self.range_frame.pack(side=tk.LEFT, padx=5)
        self.x_range_label = ttk.Label(self.range_frame, text="X-axis range:")
        self.x_range_label.pack(side=tk.LEFT)
        self.x_range_entry = ttk.Entry(self.range_frame, width=10)
        self.x_range_entry.pack(side=tk.LEFT)
        self.y_range_label = ttk.Label(self.range_frame, text="Y-axis range:")
        self.y_range_label.pack(side=tk.LEFT)
        self.y_range_entry = ttk.Entry(self.range_frame, width=10)
        self.y_range_entry.pack(side=tk.LEFT)
        self.apply_button = ttk.Button(self.range_frame, text="Apply Axis-Range", command=self.apply_range)
        self.apply_button.pack(side=tk.LEFT, padx=5)

        # create clear button
        self.clear_button = ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # create save button
        self.save_button = ttk.Button(self.toolbar, text="Save", command=self.save_canvas_dialog)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # create settings button
        self.settings_button = ttk.Button(self.toolbar, text="Settings", command=self.show_settings_dialog)
        self.settings_button.pack(side=tk.LEFT, padx=5)

        # create help button
        self.help_button = ttk.Button(self.toolbar, text="?", command=self.show_help_dialog)
        self.help_button.pack(side=tk.LEFT, padx=5)
        
        # bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # initialize variables
        self.is_drawing = False
        self.line_color = "black"
        self.line_width = 1
        self.x_range = (0, 100)
        self.y_range = (0, 100)
        self.lines = []
        self.show_grid = True
        # self.title_text = "Mouse Paint"
        self.xlabel_text = "X-axis"
        self.ylabel_text = "Y-axis"

    def on_press(self, event):
        if event.button == 1:
            self.is_drawing = True
            self.line_color = self.color_var.get()
            self.line_width = int(self.width_var.get())
            self.lines.append((self.line_color, [(event.xdata, event.ydata)]))

    def on_motion(self, event):
        if self.is_drawing:
            self.lines[-1][1].append((event.xdata, event.ydata))
            self.draw_lines()

    def draw_lines(self, xlabel_font_size, ylabel_font_size ):
        self.ax.clear()
        self.ax.set_xlim(*self.x_range)
        self.ax.set_ylim(*self.y_range)
        if self.show_grid:
            self.ax.grid(True)
        else:
            self.ax.grid(False)
        for color, line in self.lines:
            xs, ys = zip(*line)
            self.ax.plot(xs, ys, color=color, linewidth=self.line_width)
        # self.ax.set_title(self.title_text)
        self.ax.set_xlabel(self.xlabel_text, fontsize=int(xlabel_font_size))
        self.ax.set_ylabel(self.ylabel_text, fontsize=int(ylabel_font_size)) 
        self.canvas.draw()

    def on_release(self, event):
        if event.button == 1:
            self.is_drawing = False

    def apply_range(self):
        try:
            x_min, x_max = map(float, self.x_range_entry.get().split(","))
            y_min, y_max = map(float, self.y_range_entry.get().split(","))
            self.x_range = (x_min, x_max)
            self.y_range = (y_min, y_max)
            self.clear_canvas()
        except ValueError:
            pass

    def clear_canvas(self):
        self.lines = []
        self.ax.clear()
        self.ax.set_xlim(*self.x_range)
        self.ax.set_ylim(*self.y_range)
        if self.show_grid:
            self.ax.grid(True)
        else:
            self.ax.grid(False)
        self.canvas.draw()

    def get_line_labels(self):
        labels = []
        for i, (color, line) in enumerate(self.lines):
            label = simpledialog.askstring("Line Label", f"Enter label for Line {i+1}:")
            if label:
                labels.append(label)
            else:
                labels.append(f"Line {i+1}")
        return labels

    def show_help_dialog(self):
        # create a dialog to display help information
        help_dialog = tk.Toplevel(self.master)
        help_dialog.title("Help")

        # add help information
        help_text = """
        Mouse Paint - Help

        - Left-click and drag on the canvas to draw lines.
        - Use the color and width menus to customize your drawing.
        - Set X and Y axis ranges using the entry boxes and apply button, e.g. X RANGE: 0,1000.
        - Click "Clear" to erase all drawings on the canvas.
        - Click "Save" to save the canvas as an image.When the save button is pressed, a legend will be added based on the number of lines you have drawn.(当按下保存按钮时，会根据你所绘制的线条个数来添加图例。)
        - Click "Settings" to modify the plot title, axis labels, and grid display.
        - Click "?" for help.
        - Please name title and axis with English
        """
        ttk.Label(help_dialog, text=help_text, wraplength=400, justify=tk.LEFT).pack(padx=10, pady=10)
    
    def save_canvas(self, xlabel="", ylabel="", xunit="", yunit=""):
        # get line labels
        self.labels = self.get_line_labels()

        # ask for filename to save
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            # set axis labels and title
            xlabel_with_unit = f"{xlabel} ({xunit})" if xunit else xlabel
            ylabel_with_unit = f"{ylabel} ({yunit})" if yunit else ylabel
            self.ax.set_xlabel(xlabel_with_unit, fontsize=16)
            self.ax.set_ylabel(ylabel_with_unit, fontsize=16)
            self.ax.set_title(self.title_text, fontsize=20)

            # plot lines with labels
            if self.labels:
                for i, (color, line) in enumerate(self.lines):
                    self.ax.plot([], [], color=color, linewidth=self.line_width, label=self.labels[i])
                self.ax.legend(fontsize=16)

            # save figure
            self.fig.savefig(filename)

    def save_canvas_dialog(self):
        self.save_canvas()

    def show_settings_dialog(self):
        # create a dialog to modify settings
        settings_dialog = tk.Toplevel(self.master)
        settings_dialog.title("Settings")
        settings_dialog.geometry("480x320")  # set initial size
        window_width = settings_dialog.winfo_reqwidth()
        window_height = settings_dialog.winfo_reqheight()
        position_right = int(settings_dialog.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(settings_dialog.winfo_screenheight() / 2 - window_height / 2)
        settings_dialog.geometry("+{}+{}".format(position_right, position_down))  # center window

        # create and pack widgets for settings
        ttk.Label(settings_dialog, text="X-axis Label:").pack()
        xlabel_entry = ttk.Entry(settings_dialog)
        xlabel_entry.insert(0, self.xlabel_text)
        xlabel_entry.pack()

        ttk.Label(settings_dialog, text="X-axis Label Font Size:").pack()
        xlabel_font_size_entry = ttk.Entry(settings_dialog)
        xlabel_font_size_entry.insert(0, "12")  # default font size
        xlabel_font_size_entry.pack()

        ttk.Label(settings_dialog, text="Y-axis Label:").pack()
        ylabel_entry = ttk.Entry(settings_dialog)
        ylabel_entry.insert(0, self.ylabel_text)
        ylabel_entry.pack()

        ttk.Label(settings_dialog, text="Y-axis Label Font Size:").pack()
        ylabel_font_size_entry = ttk.Entry(settings_dialog)
        ylabel_font_size_entry.insert(0, "12")  # default font size
        ylabel_font_size_entry.pack()

        ttk.Label(settings_dialog, text="Show Grid:").pack()
        show_grid_var = tk.BooleanVar()
        show_grid_var.set(self.show_grid)
        show_grid_checkbox = ttk.Checkbutton(settings_dialog, variable=show_grid_var)
        show_grid_checkbox.pack()

        # button to apply settings
        apply_settings_button = ttk.Button(settings_dialog, text="Apply Settings", command=lambda: self.apply_settings(xlabel_entry.get(), ylabel_entry.get(), xlabel_font_size_entry.get(), ylabel_font_size_entry.get(), show_grid_var.get()))
        apply_settings_button.pack()


    def apply_settings(self, xlabel, ylabel, xlabel_font_size, ylabel_font_size, show_grid):
        # apply settings to the plot
        self.xlabel_text = xlabel
        self.ylabel_text = ylabel
        self.ax.set_xlabel(self.xlabel_text, fontsize=int(xlabel_font_size))
        self.ax.set_ylabel(self.ylabel_text, fontsize=int(ylabel_font_size))
        self.show_grid = show_grid
        self.draw_lines( xlabel_font_size, ylabel_font_size, )


root = tk.Tk()
app = PaintApp(root)
root.mainloop()