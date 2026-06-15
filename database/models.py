# Data Models for Professional Institute & Financial Management System

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Time, Boolean, ForeignKey, Text, Numeric, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    father_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    class_name = Column(String(50), nullable=False)
    admission_date = Column(Date, nullable=False)
    class_start_date = Column(Date, nullable=False)
    monthly_fee = Column(Numeric(10, 2), nullable=False)
    address = Column(String(255))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    fee_payments = relationship("FeePayment", back_populates="student")
    receipts = relationship("Receipt", back_populates="student")

class FeePayment(Base):
    __tablename__ = 'fee_payments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    payment_month = Column(String(20), nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0)
    remaining_balance = Column(Numeric(10, 2))
    payment_date = Column(Date, nullable=False)
    payment_time = Column(Time)
    payment_status = Column(String(20), default='completed')
    receipt_number = Column(String(50), unique=True)
    cashier_id = Column(Integer, ForeignKey('users.id'))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    student = relationship("Student", back_populates="fee_payments")
    cashier = relationship("User")
    receipts = relationship("Receipt", back_populates="payment")

class Receipt(Base):
    __tablename__ = 'receipts'
    
    id = Column(Integer, primary_key=True)
    receipt_number = Column(String(50), unique=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    payment_id = Column(Integer, ForeignKey('fee_payments.id'), nullable=False)
    receipt_type = Column(String(20), default='thermal58')
    issued_date = Column(TIMESTAMP, default=datetime.now)
    issued_by = Column(Integer, ForeignKey('users.id'))
    is_printed = Column(Boolean, default=False)
    print_count = Column(Integer, default=0)
    pdf_saved_path = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    student = relationship("Student", back_populates="receipts")
    payment = relationship("FeePayment", back_populates="receipts")
    issued_user = relationship("User")

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    father_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    subject = Column(String(50), nullable=False)
    monthly_salary = Column(Numeric(10, 2), nullable=False)
    joining_date = Column(Date, nullable=False)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    salary_payments = relationship("SalaryPayment", back_populates="teacher")
    advance_salaries = relationship("AdvanceSalary", back_populates="teacher")

class SalaryPayment(Base):
    __tablename__ = 'salary_payments'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    salary_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False)
    advance_deducted = Column(Numeric(10, 2), default=0)
    remaining_amount = Column(Numeric(10, 2))
    payment_date = Column(Date, nullable=False)
    payment_month = Column(String(20), nullable=False)
    payment_status = Column(String(20), default='completed')
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    teacher = relationship("Teacher", back_populates="salary_payments")

class AdvanceSalary(Base):
    __tablename__ = 'advance_salaries'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    advance_amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(String(255))
    request_date = Column(Date, nullable=False)
    approval_status = Column(String(20), default='approved')
    is_deducted = Column(Boolean, default=False)
    deduction_month = Column(String(20))
    deduction_date = Column(Date)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    teacher = relationship("Teacher", back_populates="advance_salaries")

class StockItem(Base):
    __tablename__ = 'stock_items'
    
    id = Column(Integer, primary_key=True)
    item_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    total_quantity = Column(Integer, nullable=False)
    sold_quantity = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    sales = relationship("StockSale", back_populates="stock_item")

class StockSale(Base):
    __tablename__ = 'stock_sales'
    
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock_items.id'), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2))
    profit_amount = Column(Numeric(10, 2))
    sale_date = Column(Date, nullable=False)
    sale_time = Column(Time)
    buyer_name = Column(String(100))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    stock_item = relationship("StockItem", back_populates="sales")

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    expense_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    description = Column(Text)
    paid_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User")

class FinancialSummary(Base):
    __tablename__ = 'financial_summary'
    
    id = Column(Integer, primary_key=True)
    summary_date = Column(Date, nullable=False)
    summary_type = Column(String(20), nullable=False)
    total_income = Column(Numeric(10, 2), default=0)
    total_expenses = Column(Numeric(10, 2), default=0)
    total_profit = Column(Numeric(10, 2), default=0)
    fee_collection = Column(Numeric(10, 2), default=0)
    salary_payment = Column(Numeric(10, 2), default=0)
    stock_sales = Column(Numeric(10, 2), default=0)
    other_income = Column(Numeric(10, 2), default=0)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(Text)
    new_values = Column(Text)
    ip_address = Column(String(50))
    action_date = Column(TIMESTAMP, default=datetime.now)
    
    user = relationship("User")

class BackupHistory(Base):
    __tablename__ = 'backup_history'
    
    id = Column(Integer, primary_key=True)
    backup_file = Column(String(255), nullable=False)
    backup_date = Column(TIMESTAMP, default=datetime.now)
    backup_size = Column(Integer)
    status = Column(String(20), default='success')
    notes = Column(Text)

class Setting(Base):
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
