# Validators for input data

import re
from datetime import datetime
from decimal import Decimal

class Validator:
    """Input validation utility"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        # Accept digits, spaces, hyphens, and + sign
        pattern = r'^[\d\s\-\+]+$'
        return re.match(pattern, phone) is not None and len(phone) >= 7
    
    @staticmethod
    def validate_amount(amount) -> bool:
        """Validate monetary amount"""
        try:
            amount_decimal = Decimal(str(amount))
            return amount_decimal > 0
        except:
            return False
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """Validate date format"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """Validate student ID format"""
        pattern = r'^STD-\d{4}$'
        return re.match(pattern, student_id) is not None
    
    @staticmethod
    def validate_teacher_id(teacher_id: str) -> bool:
        """Validate teacher ID format"""
        pattern = r'^TCH-\d{4}$'
        return re.match(pattern, teacher_id) is not None
    
    @staticmethod
    def validate_receipt_number(receipt_number: str) -> bool:
        """Validate receipt number format"""
        pattern = r'^RCP-\d{8}-\d{4}$'
        return re.match(pattern, receipt_number) is not None
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username"""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength"""
        if len(password) < 6:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_lower and has_digit
    
    @staticmethod
    def validate_full_name(name: str) -> bool:
        """Validate full name"""
        pattern = r'^[a-zA-Z\s]{2,100}$'
        return re.match(pattern, name) is not None
    
    @staticmethod
    def validate_class_name(class_name: str) -> bool:
        """Validate class name"""
        return 1 <= len(class_name) <= 50
    
    @staticmethod
    def validate_subject(subject: str) -> bool:
        """Validate subject name"""
        return 1 <= len(subject) <= 50
    
    @staticmethod
    def validate_item_name(item_name: str) -> bool:
        """Validate item name"""
        return 1 <= len(item_name) <= 100
    
    @staticmethod
    def validate_category(category: str) -> bool:
        """Validate category"""
        return 1 <= len(category) <= 50
    
    @staticmethod
    def validate_quantity(quantity) -> bool:
        """Validate quantity"""
        try:
            qty = int(quantity)
            return qty > 0
        except:
            return False
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: list) -> tuple:
        """Validate required fields"""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        return True, "All required fields present"
