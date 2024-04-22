from qfluentwidgets import CaptionLabel, CardWidget, LineEdit, PrimaryPushButton, SubtitleLabel, TableWidget, TitleLabel
from main_ui_ui import Ui_Form
from PyQt5 import QtWidgets
from sympy import symbols, sympify, lambdify
import numpy as np
import matplotlib.pyplot as plt

class MainApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.calc_button.clicked.connect(self.calculate)

        # Setup the table columns
        self.TableWidget.setColumnCount(5)
        self.TableWidget.setHorizontalHeaderLabels(["a", "b", "X", "f(x)", "Error"])
        self.TableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def false_position(self, f, a, b, tol):
        if f(a) * f(b) >= 0:
            return None, "Function has the same sign at points a and b."

        data = []
        while True:
            X = ((a * f(b)) - (b * f(a))) / (f(b) - f(a))
            fx = f(X)
            error = abs(b - a)
            data.append((a, b, X, fx, error))

            if abs(fx) < tol:
                break

            if f(a) * fx < 0:
                b = X
            else:
                a = X

        return data, None

    def calculate(self):
        user_function = self.equation_text.text()
        a = float(self.a_value.text())
        b = float(self.b_value.text())
        tolerance = float(self.tolarence_value.text())

        x = symbols('x')
        f_expr = sympify(user_function)
        f = lambdify(x, f_expr, 'numpy')

        result, message = self.false_position(f, a, b, tolerance)
#-------------------------------------------------------------------------------------------------------------------------------------
        if result:
            self.TableWidget.setRowCount(len(result))
            for row, (a, b, X, fx, error) in enumerate(result):
                self.TableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(a)))
                self.TableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(b)))
                self.TableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(X)))
                self.TableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(fx)))
                self.TableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(error)))

            # Prepare plots for each data
            plt.figure(figsize=(12, 15))
            iterations = list(range(len(result)))
            as_, bs_, xs_, fxs_, errors_ = zip(*[(row[0], row[1], row[2], row[3], row[4]) for row in result])

            # Plotting function
            plt.subplot(6, 1, 1)
            x_vals = np.linspace(min(as_), max(bs_), 400)
            y_vals = f(x_vals)
            plt.plot(x_vals, y_vals, 'k-')
            plt.title(f'Function Plot: {user_function}')
            plt.grid(True)

            # Subplot for a
            plt.subplot(6, 1, 2)
            plt.plot(iterations, as_, 'b-', label='a')
            plt.title('Value of a over iterations')
            plt.ylabel('a value')
            plt.grid(True)

            # Subplot for b
            plt.subplot(6, 1, 3)
            plt.plot(iterations, bs_, 'g-', label='b')
            plt.title('Value of b over iterations')
            plt.ylabel('b value')
            plt.grid(True)

            # Subplot for X
            plt.subplot(6, 1, 4)
            plt.plot(iterations, xs_, 'r-', label='X')
            plt.title('Value of X over iterations')
            plt.ylabel('X value')
            plt.grid(True)

            # Subplot for f(x)
            plt.subplot(6, 1, 5)
            plt.plot(iterations, fxs_, 'm-', label='f(x)', linestyle='dotted')
            plt.title('Value of f(x) over iterations')
            plt.ylabel('f(x)')
            plt.grid(True)

            # Subplot for Error
            plt.subplot(6, 1, 6)
            plt.plot(iterations, errors_, 'c-', label='Error')
            plt.title('Convergence (Error) over iterations')
            plt.xlabel('Iteration')
            plt.ylabel('Error')
            plt.grid(True)

            plt.tight_layout()
            plt.show()

        else:
            QtWidgets.QMessageBox.warning(self, "Calculation Error", message)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
