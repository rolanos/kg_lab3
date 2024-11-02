import numpy as np
from math import factorial

class BezierSurface:
    def __init__(self, control_points):
        self.control_points = [[np.array(point, dtype=np.float32) for point in row] for row in control_points]

    #Расчет и генерация точек для построения поверхности Безье
    #resultion задает точность графика
    def generate_surface(self, resolution=25):
        u_vals = np.linspace(0, 1, resolution)
        v_vals = np.linspace(0, 1, resolution)
        surface = np.array([[self.bezier_surface_point(u, v) for v in v_vals] for u in u_vals])
        return surface

    #Вычисление тензорного произведения поверхности Безье точки в параметрических направлениях (u, w)
    def bezier_surface_point(self, u, v):
        p = np.zeros(3)
        n, m = len(self.control_points) - 1, len(self.control_points[0]) - 1

        for i in range(n + 1):
            for j in range(m + 1):
                bernstein_u = self.bernstein(n, i, u)
                bernstein_v = self.bernstein(m, j, v)
                p += bernstein_u * bernstein_v * self.control_points[i][j]
        return p

    #Полином Берштейна
    def bernstein(self, n, i, t):
        return self.binomial_coeff(n, i) * (t ** i) * ((1 - t) ** (n - i))

    #Расчет биномиального коэффициент
    def binomial_coeff(self, n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
