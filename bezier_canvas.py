from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class BezierCanvas(FigureCanvas):
    def __init__(self, surface):
        self.surface = surface
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        super().__init__(self.fig)
        self.plot_surface()

    #Рисует поверхность безье и оси координат
    def plot_surface(self):
        self.ax.clear()

        # Генерация точек для поверхности Безье
        surface_points = self.surface.generate_surface()
        x = surface_points[:, :, 0]
        y = surface_points[:, :, 1]
        z = surface_points[:, :, 2]

        # Построение поверхности
        self.ax.plot_surface(x, y, z, color='cyan', edgecolor='k', alpha=0.7)

        # Отображение контрольных точек
        control_points = np.array(self.surface.control_points)
        self.ax.scatter(control_points[:, :, 0], control_points[:, :, 1], control_points[:, :, 2], color='red')

        # Установка новых границ для осей
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        # Отображение осей с подписями
        self.ax.quiver(0, 0, 0, 1, 0, 0, color='r', length=5)
        self.ax.quiver(0, 0, 0, 0, 1, 0, color='g', length=5)
        self.ax.quiver(0, 0, 0, 0, 0, 1, color='b', length=5)
        self.ax.text(10, 0, 0, "X", color='red')
        self.ax.text(0, 10, 0, "Y", color='green')
        self.ax.text(0, 0, 10, "Z", color='blue')

        self.draw()