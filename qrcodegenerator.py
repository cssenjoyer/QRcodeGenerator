import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QWidget, QFileDialog,
                            QScrollArea, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtGui import (QPixmap, QImage, QFont, QColor, QPainter, 
                        QLinearGradient, QPen, QGuiApplication)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
import qrcode
from io import BytesIO

class GlitchEffect(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.text = text
        self.glitch_offset = 0
        self.glitch_alpha = 0
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self.update_glitch)
        self.glitch_timer.start(100)
        self.setStyleSheet("""
            QLabel {
                color: #00ff9f;
                font-family: 'Segoe UI';
                font-weight: 800;
                letter-spacing: 4px;
                text-transform: uppercase;
            }
        """)

    def update_glitch(self):
        if random.random() < 0.05:
            self.glitch_offset = random.randint(-1, 1)
            self.glitch_alpha = random.randint(50, 100)
        else:
            self.glitch_offset = 0
            self.glitch_alpha = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#00ff9f"))
        gradient.setColorAt(0.5, QColor("#00ffff"))
        gradient.setColorAt(1, QColor("#00ff9f"))
        
        painter.setPen(QPen(QColor(0, 255, 159, 30), 8))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        
        painter.setPen(QPen(QColor(0, 255, 159, 50), 4))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        
        painter.setPen(QColor(0, 255, 159))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

        if self.glitch_offset:
            painter.setPen(QColor(255, 50, 50, self.glitch_alpha))
            rect = self.rect()
            rect.translate(self.glitch_offset, 0)
            painter.drawText(rect, Qt.AlignCenter, self.text)
            painter.setPen(QColor(50, 50, 255, self.glitch_alpha))
            rect = self.rect()
            rect.translate(-self.glitch_offset, 0)
            painter.drawText(rect, Qt.AlignCenter, self.text)

class ModernButton(QPushButton):
    def __init__(self, text, color_start, color_end, parent=None):
        super().__init__(text, parent)
        self.color_start = color_start
        self.color_end = color_end
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {color_start}, stop:1 {color_end});
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {color_end}, stop:1 {color_start});
            }}
        """)

    def enterEvent(self, event):
        animation = QPropertyAnimation(self.shadow, b"blurRadius")
        animation.setDuration(200)
        animation.setStartValue(15)
        animation.setEndValue(25)
        animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        animation = QPropertyAnimation(self.shadow, b"blurRadius")
        animation.setDuration(200)
        animation.setStartValue(25)
        animation.setEndValue(15)
        animation.start()
        super().leaveEvent(event)

class QRGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_qr = None
        self.initUI()
        self.start_background_animation()

    def initUI(self):
        self.setWindowTitle("Генератор QR-кодов")
        self.setGeometry(100, 100, 800, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: #0a0a0a;
            }
            QWidget {
                color: #ffffff;
            }
            QScrollArea {
                background: transparent;
                border: 2px solid rgba(0, 255, 159, 0.1);
                border-radius: 15px;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollArea > QWidget {
                background: transparent;
            }
            QLineEdit {
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid rgba(0, 255, 159, 0.2);
                border-radius: 10px;
                padding: 15px;
                color: #e0e0e0;
                font-size: 14px;
                selection-background-color: #00ff9f;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 255, 159, 0.05);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff9f, stop:1 #00ffcc);
                min-height: 20px;
                border-radius: 5px;
            }
        """)

        # Главный виджет и layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setSpacing(30)
        self.layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок с эффектом глитча
        self.title_label = GlitchEffect("ГЕНЕРАТОР QR-КОДОВ")
        self.title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.title_label.setFixedHeight(100)
        self.layout.addWidget(self.title_label)

        # Поле ввода
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите текст или ссылку...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: rgba(20, 20, 20, 0.8);
                border: 1px solid rgba(0, 255, 159, 0.3);
                border-radius: 10px;
                padding: 15px;
                color: #e0e0e0;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.input_field)

        # Область для QR-кода
        self.qr_frame = QWidget()
        self.qr_frame.setStyleSheet("""
            QWidget {
                background: rgba(0, 255, 159, 0.05);
                border: 1px solid rgba(0, 255, 159, 0.1);
                border-radius: 15px;
            }
        """)
        self.qr_layout = QVBoxLayout(self.qr_frame)
        self.qr_label = QLabel("QR-код появится здесь")
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 16px;
            }
        """)
        self.qr_layout.addWidget(self.qr_label)
        self.layout.addWidget(self.qr_frame)

        # Кнопки
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setSpacing(20)
        
        buttons_data = [
            ("СГЕНЕРИРОВАТЬ", "#00ff9f", "#00ffcc", self.generate_qr),
            ("СОХРАНИТЬ", "#00ffcc", "#00ff9f", self.save_qr)
        ]
        
        for text, color_start, color_end, func in buttons_data:
            btn = ModernButton(text, color_start, color_end)
            btn.clicked.connect(func)
            self.button_layout.addWidget(btn)

        self.layout.addWidget(self.button_container)

    def start_background_animation(self):
        self.background_timer = QTimer(self)
        self.background_timer.timeout.connect(self.update_background)
        self.background_timer.start(50)
        self.background_offset = 0

    def update_background(self):
        self.background_offset = (self.background_offset + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(10, 12, 16))
        gradient.setColorAt(0.5, QColor(15, 18, 24))
        gradient.setColorAt(1, QColor(10, 12, 16))
        painter.fillRect(self.rect(), gradient)

        pen = QPen(QColor(0, 255, 159, 10))
        pen.setWidth(1)
        painter.setPen(pen)
        
        step = 30
        offset = self.background_offset
        for x in range(0, self.width() + step, step):
            painter.drawLine(x + offset, 0, x + offset - step*2, self.height())
        for y in range(0, self.height() + step, step):
            painter.drawLine(0, y + offset, self.width(), y + offset - step*2)

    def generate_qr(self):
        text = self.input_field.text()
        if not text:
            self.qr_label.setText("Введите текст для генерации QR-кода")
            self.qr_label.setStyleSheet("color: rgba(255, 100, 100, 0.8);")
            return
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="#00ff9f", back_color="transparent")
            
            # Сохранение в буфер
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            
            # Отображение
            qimage = QImage()
            qimage.loadFromData(buffered.getvalue())
            pixmap = QPixmap.fromImage(qimage)
            
            # Применяем эффект свечения
            effect = QGraphicsDropShadowEffect()
            effect.setColor(QColor(0, 255, 159, 150))
            effect.setBlurRadius(30)
            effect.setOffset(0, 0)
            
            self.qr_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.qr_label.setGraphicsEffect(effect)
            self.qr_label.setText("")
            
            # Сохраняем QR-код для возможного сохранения
            self.current_qr = img
            
        except Exception as e:
            self.qr_label.setText(f"Ошибка генерации: {str(e)}")
            self.qr_label.setStyleSheet("color: rgba(255, 100, 100, 0.8);")

    def save_qr(self):
        if not self.current_qr:
            return
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить QR-код",
            "",
            "PNG Files (*.png);;All Files (*)",
            options=options
        )
        
        if file_name:
            if not file_name.endswith('.png'):
                file_name += '.png'
            self.current_qr.save(file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRGenerator()
    window.show()
    sys.exit(app.exec_())