# Main Application Window

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QStackedWidget, QSideBar, QPushButton, QLabel, QMenu, 
                               QMessageBox, QStatusBar, QToolBar)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QAction
from datetime import datetime
from config import APP_NAME, APP_VERSION
from ui.login_window import LoginWindow
from ui.dashboards.dashboard import Dashboard
from ui.modules.student_module import StudentModule
from ui.modules.fee_collection_module import FeeCollectionModule
from ui.modules.teacher_module import TeacherModule
from ui.modules.salary_module import SalaryModule
from ui.modules.stock_module import StockModule
from ui.modules.expense_module import ExpenseModule
from ui.modules.reports_module import ReportsModule
from auth.roles import RoleManager

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.role_manager = RoleManager()
        
        # Show login window first
        self.show_login()
    
    def show_login(self):
        """Show login dialog"""
        login_window = LoginWindow()
        login_window.login_successful.connect(self.on_login_success)
        
        if login_window.exec() == QDialog.Rejected:
            exit(0)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.init_ui()
    
    def init_ui(self):
        """Initialize main UI after login"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1000, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar, 0)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
        central_widget.setLayout(main_layout)
        
        # Create all modules
        self.create_modules()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QSideBar {
                background-color: #1a237e;
                border-right: 1px solid #ddd;
            }
            QPushButton {
                padding: 10px;
                text-align: left;
                border: none;
                color: white;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #283593;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        
        # Show dashboard by default
        self.show_page("dashboard")
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        from PySide6.QtWidgets import QFrame
        
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a237e;
                border-right: 1px solid #ddd;
            }
        """)
        sidebar.setMaximumWidth(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)
        
        # User info
        user_label = QLabel(f"User: {self.current_user['full_name']}")
        user_label.setStyleSheet("color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(user_label)
        
        role_label = QLabel(f"Role: {self.role_manager.get_role_display_name(self.current_user['role'])}")
        role_label.setStyleSheet("color: #90caf9; padding: 0 10px;")
        layout.addWidget(role_label)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        nav_items = [
            ("Dashboard", "dashboard", True),
            ("Student Management", "students", True),
            ("Fee Collection", "fee_collection", self.role_manager.has_permission(self.current_user['role'], 'collect_fees')),
            ("Teacher Management", "teachers", self.role_manager.has_permission(self.current_user['role'], 'manage_teachers')),
            ("Salary Management", "salaries", self.role_manager.has_permission(self.current_user['role'], 'manage_salaries')),
            ("Stock Management", "stock", self.role_manager.has_permission(self.current_user['role'], 'manage_stock')),
            ("Expenses", "expenses", self.role_manager.has_permission(self.current_user['role'], 'manage_expenses')),
            ("Reports", "reports", self.role_manager.has_permission(self.current_user['role'], 'view_reports')),
        ]
        
        for label, page_id, visible in nav_items:
            if visible:
                btn = QPushButton(label)
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 12px 15px;
                        text-align: left;
                        border: none;
                        color: white;
                        font-size: 12px;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        background-color: #283593;
                    }
                    QPushButton:pressed {
                        background-color: #0d47a1;
                    }
                """)
                btn.clicked.connect(lambda checked, p=page_id: self.show_page(p))
                layout.addWidget(btn)
        
        layout.addStretch()
        
        # Bottom buttons
        backup_btn = QPushButton("Backup Database")
        backup_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #f57c00;
            }
            QPushButton:hover {
                background-color: #e64a19;
            }
        """)
        if self.role_manager.has_permission(self.current_user['role'], 'backup_database'):
            layout.addWidget(backup_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #d32f2f;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_modules(self):
        """Create all application modules"""
        # Dashboard
        self.dashboard = Dashboard()
        self.stacked_widget.addWidget(self.dashboard)
        self.modules_map = {"dashboard": self.dashboard}
        
        # Student Management
        self.student_module = StudentModule()
        self.stacked_widget.addWidget(self.student_module)
        self.modules_map["students"] = self.student_module
        
        # Fee Collection
        self.fee_module = FeeCollectionModule()
        self.stacked_widget.addWidget(self.fee_module)
        self.modules_map["fee_collection"] = self.fee_module
        
        # Teacher Management
        self.teacher_module = TeacherModule()
        self.stacked_widget.addWidget(self.teacher_module)
        self.modules_map["teachers"] = self.teacher_module
        
        # Salary Management
        self.salary_module = SalaryModule()
        self.stacked_widget.addWidget(self.salary_module)
        self.modules_map["salaries"] = self.salary_module
        
        # Stock Management
        self.stock_module = StockModule()
        self.stacked_widget.addWidget(self.stock_module)
        self.modules_map["stock"] = self.stock_module
        
        # Expense Management
        self.expense_module = ExpenseModule()
        self.stacked_widget.addWidget(self.expense_module)
        self.modules_map["expenses"] = self.expense_module
        
        # Reports
        self.reports_module = ReportsModule()
        self.stacked_widget.addWidget(self.reports_module)
        self.modules_map["reports"] = self.reports_module
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add toolbar items
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_current_module)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
    
    def create_status_bar(self):
        """Create status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Time display
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)
        
        # Update time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
    
    def update_time(self):
        """Update status bar time"""
        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.time_label.setText(current_time)
    
    def show_page(self, page_id):
        """Show specific page/module"""
        if page_id in self.modules_map:
            self.stacked_widget.setCurrentWidget(self.modules_map[page_id])
    
    def refresh_current_module(self):
        """Refresh current module"""
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'refresh'):
            current_widget.refresh()
    
    def show_help(self):
        """Show help dialog"""
        QMessageBox.information(self, "Help", 
            "Professional Institute & Financial Management System\n\n"
            "This system helps manage:\n"
            "- Student registration and fee collection\n"
            "- Teacher management and salary payments\n"
            "- Stock and inventory management\n"
            "- Financial reporting and analysis\n\n"
            "For more information, contact support.")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
            f"{APP_NAME}\nVersion {APP_VERSION}\n\n"
            "A comprehensive ERP system for educational institutes.\n\n"
            "© 2026 - All Rights Reserved")
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.timer.stop()
            self.close()
            self.show_login()
