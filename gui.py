from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
import pandas as pd
import plotly.graph_objects as go
import io


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Veri Görselleştirme")

        # Ana widget ve layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # QWebEngineView
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Kullanıcı etkileşim bölümü
        input_layout = QHBoxLayout()

        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText("X koordinatları (virgülle ayrılmış)")
        input_layout.addWidget(self.input_x)

        self.input_y = QLineEdit()
        self.input_y.setPlaceholderText("Y koordinatları (virgülle ayrılmış)")
        input_layout.addWidget(self.input_y)

        self.input_z = QLineEdit()
        self.input_z.setPlaceholderText("Z koordinatları (virgülle ayrılmış)")
        input_layout.addWidget(self.input_z)

        add_button = QPushButton("Grafiğe Ekle")
        add_button.clicked.connect(self.add_data_to_plot)
        input_layout.addWidget(add_button)

        load_button = QPushButton("CSV'den Ekle")
        load_button.clicked.connect(self.load_from_csv)
        input_layout.addWidget(load_button)

        layout.addLayout(input_layout)

        # Grafik için veri depolama
        self.graph_data = {"x": [], "y": [], "z": []}

        # Varsayılan grafik
        self.init_plot()

    def init_plot(self):
        fig = go.Figure(data=[go.Scatter3d(
            x=self.graph_data["x"],
            y=self.graph_data["y"],
            z=self.graph_data["z"],
            mode='markers',
            marker=dict(size=10, color=self.graph_data["z"], colorscale='Viridis')
        )])

        fig.update_layout(
            scene=dict(
                xaxis_title="X Eksen",
                yaxis_title="Y Eksen",
                zaxis_title="Z Eksen"
            )
        )

        html_content = io.StringIO()
        fig.write_html(html_content, include_plotlyjs='cdn')
        self.web_view.setHtml(html_content.getvalue())

    def add_data_to_plot(self):
        try:
            # Kullanıcıdan girilen verileri al
            new_x = list(map(float, self.input_x.text().split(',')))
            new_y = list(map(float, self.input_y.text().split(',')))
            new_z = list(map(float, self.input_z.text().split(',')))

            if len(new_x) == len(new_y) == len(new_z):
                # Mevcut verilere ekle
                self.graph_data["x"].extend(new_x)
                self.graph_data["y"].extend(new_y)
                self.graph_data["z"].extend(new_z)

                # Grafiği güncelle
                self.init_plot()
            else:
                self.show_error("X, Y, Z koordinatlarının uzunlukları eşit olmalı!")
        except ValueError:
            self.show_error("Koordinatlar doğru formatta değil!")

    def load_from_csv(self):
        # Kullanıcıdan CSV dosyası seçmesini iste
        file_path, _ = QFileDialog.getOpenFileName(self, "CSV Dosyası Seç", "", "CSV Files (*.csv)")

        if file_path:
            try:
                # CSV dosyasını oku
                df = pd.read_csv(file_path)

                if all(col in df.columns for col in ['x', 'y', 'z']):
                    new_x = df['x'].tolist()
                    new_y = df['y'].tolist()
                    new_z = df['z'].tolist()

                    # Mevcut verilere ekle
                    self.graph_data["x"].extend(new_x)
                    self.graph_data["y"].extend(new_y)
                    self.graph_data["z"].extend(new_z)

                    # Grafiği güncelle
                    self.init_plot()
                else:
                    self.show_error("CSV dosyasında 'x', 'y', 'z' sütunları bulunmalı!")
            except Exception as e:
                self.show_error(f"Hata: {e}")

    def show_error(self, message):
        error_window = QMainWindow(self)
        error_window.setWindowTitle("Hata")
        error_label = QLabel(message, error_window)
        error_window.setCentralWidget(error_label)
        error_window.resize(300, 100)
        error_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())