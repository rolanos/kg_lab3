from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QSpinBox, QGroupBox
from PyQt5.QtCore import Qt
from bezier_surface import BezierSurface
from bezier_canvas import BezierCanvas
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поверхность Безье. Будило Зашляхтин Костенко")
        self.setGeometry(100, 100, 1000, 700)

        # Набор контрольных точек по умолчанию
        control_points = [
            [[-10, -10, 0], [-5, -10, 5], [5, -10, 5], [10, -10, 0]],
            [[-10, -5, -5], [-5, -5, 10], [5, -5, 10], [10, -5, -5]],
            [[-10, 5, -5], [-5, 5, 10], [5, 5, 10], [10, 5, -5]],
            [[-10, 10, 0], [-5, 10, 5], [5, 10, 5], [10, 10, 0]]
        ]
        # Инициализация поверхности Безье
        self.bezier_surface = BezierSurface(control_points)
        self.canvas = BezierCanvas(self.bezier_surface)
        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Основной макет
        layout = QHBoxLayout()
        main_widget.setLayout(layout)
        # Панель управления
        self.spinbox_dict = {}  # Словарь для хранения ссылок на QSpinBox для каждой точки
        control_panel = self.create_control_panel()
        # Добавляем виджеты к макету
        layout.addWidget(self.canvas, 3)
        layout.addWidget(control_panel, 1)

    #Создаёт панель управления с вращением и настройкой координат точек
    def create_control_panel(self):
        control_panel = QWidget()
        layout = QVBoxLayout()
        control_panel.setLayout(layout)

        # Группа для вращения осей графика
        rotation_group = QGroupBox("Поворот осей графика")
        rotation_layout = QVBoxLayout()
        for axis in ["X", "Y", "Z"]:
            button_layout = QHBoxLayout()
            label = QLabel(f"Поворот по {axis}:")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-180, 180)
            slider.valueChanged.connect(lambda value, ax=axis: self.set_rotation(ax, value))
            button_layout.addWidget(label)
            button_layout.addWidget(slider)
            rotation_layout.addLayout(button_layout)
        rotation_group.setLayout(rotation_layout)
        layout.addWidget(rotation_group)

        # Группа для вращения контрольных точек
        control_rotation_group = QGroupBox("Поворот точек вокруг осей")
        control_rotation_layout = QVBoxLayout()

        for axis in ["OX", "OY"]:
            button_layout = QHBoxLayout()
            label = QLabel(f"Поворот вокруг {axis}:")
            increase_button = QPushButton("-")
            decrease_button = QPushButton("+")
            increase_button.clicked.connect(lambda _, ax=axis: self.rotate_control_points(ax, 5))
            decrease_button.clicked.connect(lambda _, ax=axis: self.rotate_control_points(ax, -5))
            button_layout.addWidget(label)
            button_layout.addWidget(increase_button)
            button_layout.addWidget(decrease_button)
            control_rotation_layout.addLayout(button_layout)
        control_rotation_group.setLayout(control_rotation_layout)
        layout.addWidget(control_rotation_group)

        # Группа для управления координатами точек
        coords_group = QGroupBox("Контрольные точки")
        coords_layout = QVBoxLayout()
        for i, row in enumerate(self.bezier_surface.control_points):
            for j, point in enumerate(row):
                point_layout = QHBoxLayout()
                label = QLabel(f"Point [{i},{j}]:")
                spinboxes = []
                for k, coord in enumerate("XYZ"):
                    spinbox = QSpinBox()
                    spinbox.setRange(-10, 10)  # Увеличенный диапазон
                    spinbox.setValue(int(point[k]))
                    spinbox.valueChanged.connect(lambda value, i=i, j=j, k=k: self.update_control_point(i, j, k, value))
                    spinboxes.append(spinbox)
                # Сохраняем ссылку на QSpinBox для последующего обновления
                self.spinbox_dict[(i, j)] = spinboxes
                point_layout.addWidget(label)
                point_layout.addWidget(spinboxes[0])
                point_layout.addWidget(spinboxes[1])
                point_layout.addWidget(spinboxes[2])
                coords_layout.addLayout(point_layout)
        coords_group.setLayout(coords_layout)
        layout.addWidget(coords_group)

        return control_panel

    #Устанавливает угол вращения и обновляет график
    def set_rotation(self, axis, value):
        if axis == "X":
            self.canvas.ax.view_init(elev=value)
        elif axis == "Y":
            self.canvas.ax.view_init(azim=value)
        self.canvas.plot_surface()

    #Вращает контрольные точки вокруг оси OX или OY на заданный угол и обновляет график и панель
    def rotate_control_points(self, axis, angle):
        radians = np.radians(angle)
        cos_a, sin_a = np.cos(radians), np.sin(radians)

        for i in range(len(self.bezier_surface.control_points)):
            for j in range(len(self.bezier_surface.control_points[i])):
                x, y, z = self.bezier_surface.control_points[i][j]
                if axis == "OX":
                    y_new = y * cos_a - z * sin_a
                    z_new = y * sin_a + z * cos_a
                    self.bezier_surface.control_points[i][j] = np.array([x, y_new, z_new])
                elif axis == "OY":
                    x_new = x * cos_a + z * sin_a
                    z_new = -x * sin_a + z * cos_a
                    self.bezier_surface.control_points[i][j] = np.array([x_new, y, z_new])
                # Обновляем значения QSpinBox с новыми координатами точки
                self.update_spinbox(i, j)

        self.canvas.plot_surface()

    #Обновляет значения QSpinBox для заданной точки (i, j)
    def update_spinbox(self, i, j):
        x, y, z = self.bezier_surface.control_points[i][j]
        self.spinbox_dict[(i, j)][0].setValue(int(x))
        self.spinbox_dict[(i, j)][1].setValue(int(y))
        self.spinbox_dict[(i, j)][2].setValue(int(z))

    #Обновляет контрольную точку и график при изменении значения в QSpinBox
    def update_control_point(self, i, j, k, value):
        self.bezier_surface.control_points[i][j][k] = value
        self.canvas.plot_surface()
