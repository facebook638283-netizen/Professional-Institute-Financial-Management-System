# Login Window UI

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from auth.auth_manager import AuthManager

class LoginWindow(QDialog):
    """Login window for user authentication"""
    
    login_successful = Signal(dict)  # Signal to emit user data on successful login
    
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Professional Institute & Financial Management System - Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton {
                padding: 10px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Login")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Username
        main_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        main_layout.addWidget(self.username_input)
        
        # Password
        main_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.password_input)
        
        # Remember me
        self.remember_checkbox = QCheckBox("Remember me")
        main_layout.addWidget(self.remember_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(login_btn)
        
        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Connect Enter key to login
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter username and password")
            return
        
        result = self.auth_manager.login(username, password)
        
        if result['success']:
            self.login_successful.emit(result)
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", result['message'])
            self.password_input.clear()
            self.username_input.setFocus()
