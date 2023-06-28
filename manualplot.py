import matplotlib.pyplot as plt

class SimpleDrawingApp:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.lines = []
        self.current_line = None

        # 添加鼠标事件处理函数
        self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion_notify)
        self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)

        # 创建工具栏
        self.toolbar = self.fig.canvas.toolbar
        self.toolbar.pan()
        self.toolbar.zoom()

    def on_button_press(self, event):
        # 创建一个新的线条
        self.current_line, = self.ax.plot([], [])
        self.lines.append(self.current_line)
        self.current_line.set_data([event.xdata], [event.ydata])  # 设置初始的空数据点
        self.current_line.set_color('blue')  # 默认颜色为蓝色

    def on_motion_notify(self, event):
        # 实时更新线条的终点坐标
        if self.current_line:
            xdata = self.current_line.get_xdata() + [event.xdata]
            ydata = self.current_line.get_ydata() + [event.ydata]
            self.current_line.set_data(xdata, ydata)
            self.fig.canvas.draw()

    def on_button_release(self, event):
        self.current_line = None

    def set_line_color(self, color):
        if self.current_line:
            self.current_line.set_color(color)
            self.fig.canvas.draw()

    def set_line_width(self, width):
        if self.current_line:
            self.current_line.set_linewidth(width)
            self.fig.canvas.draw()

    def clear_canvas(self):
        for line in self.lines:
            line.set_data([], [])
        self.lines.clear()
        self.fig.canvas.draw()

    def set_axis_range(self, xlim, ylim):
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.fig.canvas.draw()

    def save_image(self, filename):
        self.fig.savefig(filename)

if __name__ == '__main__':
    app = SimpleDrawingApp()

    # 设置X和Y轴的范围
    xlim = [0, 10]
    ylim = [0, 10]
    app.set_axis_range(xlim, ylim)

    # 显示程序界面
    plt.show()