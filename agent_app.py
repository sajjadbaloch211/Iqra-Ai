import sys
import os
import threading
import time
import speech_recognition as sr
import pyttsx3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QFrame, QScrollArea, QStackedWidget,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon, QPainter, QBrush, QPen, QRadialGradient
from chatbot import ChatBot

class Communicate(QObject):
    response_received = pyqtSignal(str)
    speech_detected = pyqtSignal(str)

class ChatBubble(QFrame):
    def __init__(self, text, sender="bot", parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 5, 0, 5)
        
        self.bubble = QFrame()
        self.bubble_layout = QVBoxLayout(self.bubble)
        self.bubble_layout.setContentsMargins(15, 12, 15, 12)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-family: 'Segoe UI'; border: none; background: transparent;")
        
        self.bubble_layout.addWidget(self.label)
        
        if sender == "user":
            self.bubble.setStyleSheet("""
                QFrame {
                    background-color: #4ecdc4;
                    color: white;
                    border-radius: 18px;
                    border-bottom-right-radius: 2px;
                }
            """)
            self.label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600;")
            self.main_layout.addStretch()
            self.main_layout.addWidget(self.bubble)
            self.bubble.setMaximumWidth(320)
        else:
            self.bubble.setStyleSheet("""
                QFrame {
                    background-color: #f1f5f9;
                    color: #1e293b;
                    border: 1px solid #e2e8f0;
                    border-radius: 18px;
                    border-bottom-left-radius: 2px;
                }
            """)
            self.label.setStyleSheet("color: #1e293b; font-size: 14px;")
            self.main_layout.addWidget(self.bubble)
            self.main_layout.addStretch()
            self.bubble.setMaximumWidth(320)

class AiSpeechBubble(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Hi! I'm Curio! 👋\nHere to help you")
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: #1e293b; font-size: 15px; font-weight: 500; font-family: 'Segoe UI';")
        self.layout.addWidget(self.label)
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border-bottom-left-radius: 2px;
                padding: 5px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

class ModernVoiceOrb(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pulse = 0
        self.active = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(40)

    def animate(self):
        if self.active:
            self.pulse = (self.pulse + 1) % 50
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Blue Glow / Rings
        if self.active:
            for i in range(1, 4):
                alpha = int(80 / i) - (self.pulse * 1)
                if alpha < 0: alpha = 0
                p.setBrush(QBrush(QColor(56, 189, 248, alpha)))
                p.setPen(Qt.PenStyle.NoPen)
                rad = 40 + (i * 15) + (self.pulse * 0.5)
                p.drawEllipse(int(60 - rad), int(60 - rad), int(rad * 2), int(rad * 2))

        # Main White Circle
        p.setBrush(QBrush(Qt.GlobalColor.white))
        p.setPen(QPen(QColor(56, 189, 248, 100), 2))
        p.drawEllipse(30, 30, 60, 60)
        
        # Mic Icon
        p.setPen(QPen(QColor(30, 41, 59), 2))
        p.drawEllipse(54, 48, 12, 18)
        p.drawLine(60, 66, 60, 72)

class CurioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bot = ChatBot()
        self.comm = Communicate()
        self.comm.response_received.connect(self.display_res)
        self.comm.speech_detected.connect(self.handle_speech)
        
        self.init_engines()
        self.active_engine = None
        self.initUI()

    def init_engines(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            for v in voices:
                if "male" in v.name.lower() or "david" in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
            self.speech_enabled = True
        except: self.speech_enabled = False
        # STT Engine Optimization
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300  # More sensitive
            self.recognizer.pause_threshold = 0.5    # Faster detection of end-of-speech
            self.mic = sr.Microphone()
            self.mic_enabled = True
        except: self.mic_enabled = False
        self.is_listening = False

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(450, 850)

        # Main Stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # --- VOICE SCREEN (The "Curio" Look) ---
        self.voice_page = QFrame()
        self.voice_page.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e0f2fe);
            border-radius: 45px;
        """)
        v_lay = QVBoxLayout(self.voice_page)
        v_lay.setContentsMargins(0, 0, 0, 0)

        # Status Bar
        sb = QWidget()
        sb.setFixedHeight(40)
        sb_lay = QHBoxLayout(sb)
        sb_lay.setContentsMargins(35, 15, 35, 0)
        sb_lay.addWidget(QLabel("9:41"), alignment=Qt.AlignmentFlag.AlignLeft)
        sb_lay.addStretch()
        sb_lay.addWidget(QLabel("📶 🔋"), alignment=Qt.AlignmentFlag.AlignRight)
        v_lay.addWidget(sb)

        v_lay.addSpacing(60)

        # Large Header
        self.big_text = QLabel("Your ✨ Smart\nAssistant for\nIqra University\nInformation")
        self.big_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.big_text.setStyleSheet("color: #1e293b; font-size: 28px; font-weight: 800; font-family: 'Segoe UI';")
        v_lay.addWidget(self.big_text)

        v_lay.addStretch()

        # Robot & Single Bubble
        robot_box = QWidget()
        robot_box.setFixedHeight(400)
        rb_lay = QVBoxLayout(robot_box)
        
        self.ai_bubble = AiSpeechBubble(robot_box)
        rb_lay.addWidget(self.ai_bubble, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.robot_img = QLabel()
        pix = QPixmap("curio_robot.png")
        if not pix.isNull():
            self.robot_img.setPixmap(pix.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.robot_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rb_lay.addWidget(self.robot_img)
        v_lay.addWidget(robot_box)

        v_lay.addStretch()

        # Voice Orb & Controls
        v_ctrls = QHBoxLayout()
        v_ctrls.setContentsMargins(40, 0, 40, 50)
        
        kb_btn = QPushButton("⌨️")
        kb_btn.setFixedSize(50, 50)
        kb_btn.setStyleSheet("background: transparent; font-size: 24px; color: #64748b;")
        kb_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        v_ctrls.addWidget(kb_btn)
        
        v_ctrls.addStretch()
        self.voice_orb = ModernVoiceOrb()
        self.voice_orb.clicked.connect(self.toggle_mic)
        v_ctrls.addWidget(self.voice_orb)
        v_ctrls.addStretch()
        
        v_ctrls.addStretch()
        
        stop_btn = QPushButton("🛑")
        stop_btn.setFixedSize(50, 50)
        stop_btn.setToolTip("Stop AI Voice")
        stop_btn.setStyleSheet("background: transparent; font-size: 28px; color: #ef4444;")
        stop_btn.clicked.connect(self.stop_speech)
        v_ctrls.addWidget(stop_btn)
        
        v_lay.addLayout(v_ctrls)

        # --- CHAT SCREEN (Light Theme) ---
        self.chat_page = QFrame()
        self.chat_page.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e0f2fe);
            border-radius: 45px;
        """)
        t_lay = QVBoxLayout(self.chat_page)
        t_lay.setContentsMargins(0, 0, 0, 0)
        
        t_head = QHBoxLayout()
        t_head.setContentsMargins(30, 20, 30, 10)
        t_back = QPushButton("←")
        t_back.setStyleSheet("color: #1e293b; font-size: 22px; background: transparent;")
        t_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        t_head.addWidget(t_back)
        t_head.addStretch()
        title_lbl = QLabel("Chat with NEURA")
        title_lbl.setStyleSheet("color: #1e293b; font-size: 16px; font-weight: 700;")
        t_head.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        t_head.addStretch()
        t_dots = QPushButton("•••")
        t_dots.setStyleSheet("color: #1e293b; font-size: 22px; background: transparent;")
        t_head.addLayout(t_head) # Note: t_head is already added, this is for alignment
        t_lay.addLayout(t_head)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.msg_cont = QWidget()
        self.msg_cont.setStyleSheet("background: transparent;")
        self.msg_lay = QVBoxLayout(self.msg_cont)
        self.msg_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.msg_lay.setContentsMargins(25, 20, 25, 20)
        self.msg_lay.setSpacing(15)
        self.scroll.setWidget(self.msg_cont)
        t_lay.addWidget(self.scroll)

        t_in_frame = QFrame()
        t_in_frame.setFixedHeight(110)
        t_in_lay = QHBoxLayout(t_in_frame)
        t_in_lay.setContentsMargins(25, 10, 25, 45)
        
        in_box = QFrame()
        in_box.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 25px;")
        in_box_lay = QHBoxLayout(in_box)
        in_box_lay.setContentsMargins(15, 5, 15, 5)
        
        self.text_in = QLineEdit()
        self.text_in.setPlaceholderText("Type your message...")
        self.text_in.setStyleSheet("background: transparent; border: none; color: #1e293b; height: 40px; font-size: 15px;")
        self.text_in.returnPressed.connect(self.send_t)
        in_box_lay.addWidget(self.text_in)
        
        t_mic = QPushButton("🎙️")
        t_mic.setStyleSheet("background: transparent; color: #64748b; font-size: 20px;")
        t_mic.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        in_box_lay.addWidget(t_mic)
        t_in_lay.addWidget(in_box)
        t_lay.addWidget(t_in_frame)

        self.stack.addWidget(self.voice_page)
        self.stack.addWidget(self.chat_page)
        self.oldPos = self.pos()

    def mousePressEvent(self, e):
        self.oldPos = e.globalPosition().toPoint()
    def mouseMoveEvent(self, e):
        delta = QPoint(e.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPosition().toPoint()

    def toggle_mic(self):
        if not self.mic_enabled: return
        self.is_listening = not self.is_listening
        self.voice_orb.active = self.is_listening
        if self.is_listening:
            self.ai_bubble.label.setText("I'm listening... 👂")
            threading.Thread(target=self.listen_t, daemon=True).start()
        else:
            self.ai_bubble.label.setText("Hi! I'm Curio! 👋")

    def listen_t(self):
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self.recognizer.listen(source, timeout=4, phrase_time_limit=10)
            text = self.recognizer.recognize_google(audio)
            self.comm.speech_detected.emit(text)
        except: pass
        finally:
            self.is_listening = False
            QTimer.singleShot(0, lambda: setattr(self.voice_orb, 'active', False))

    def handle_speech(self, t):
        self.ai_bubble.label.setText("Analyzing voice... 🧠")
        self.add_b(t, "user")
        threading.Thread(target=self.call_ai, args=(t,), daemon=True).start()

    def send_t(self):
        t = self.text_in.text().strip()
        if not t: return
        self.text_in.clear()
        self.add_b(t, "user")
        threading.Thread(target=self.call_ai, args=(t,), daemon=True).start()

    def call_ai(self, t):
        try:
            r = self.bot.get_response(t)
            c = r.replace("[WIDGET:FEE]", "").replace("[WIDGET:GRADE]", "").replace("[WIDGET:MAP]", "").replace("[WIDGET:TEAM]", "").replace("[WIDGET:AURA]", "").replace("**", "").strip()
            self.comm.response_received.emit(c)
        except Exception as e:
            self.comm.response_received.emit(f"Error: {e}")

    def display_res(self, t):
        # Stop any previous speech before starting new one
        self.stop_speech()
        
        # On voice screen, don't show the long text, just the status
        self.ai_bubble.label.setText("🔊 I'm speaking...")
        self.add_b(t, "bot")
        if self.speech_enabled:
            threading.Thread(target=self.say, args=(t,), daemon=True).start()

    def add_b(self, t, s):
        bub = ChatBubble(t, s)
        self.msg_lay.addWidget(bub)
        QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def say(self, t):
        try:
            # Initialize a fresh engine instance inside the thread to avoid COM/threading issues on Windows
            import pyttsx3
            self.active_engine = pyttsx3.init()
            
            # Search for a Male voice (e.g., Microsoft David)
            voices = self.active_engine.getProperty('voices')
            for v in voices:
                if "male" in v.name.lower() or "david" in v.name.lower():
                    self.active_engine.setProperty('voice', v.id)
                    break
            
            self.active_engine.setProperty('rate', 170)
            
            clean_text = t.encode('ascii','ignore').decode('ascii')
            time.sleep(0.1) # Small delay
            self.active_engine.say(clean_text)
            self.active_engine.runAndWait()
        except Exception as e:
            print(f"TTS Thread Error: {e}")
        finally:
            self.active_engine = None
            # Reset UI bubble if it was showing 'speaking'
            if self.ai_bubble.label.text() == "🔊 I'm speaking...":
                QTimer.singleShot(0, lambda: self.ai_bubble.label.setText("Hi! I'm Curio! 👋"))

    def stop_speech(self):
        if self.active_engine:
            try:
                self.active_engine.stop()
                self.active_engine = None
                self.ai_bubble.label.setText("Hi! I'm Curio! 👋")
            except:
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CurioApp()
    win.show()
    sys.exit(app.exec())
