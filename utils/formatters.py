# Formatters for displaying data

from datetime import datetime
from decimal import Decimal
from config import DATE_FORMAT, DATETIME_FORMAT, CURRENCY_SYMBOL, DECIMAL_PLACES

class Formatter:
    """Data formatting utility"""
    
    @staticmethod
    def format_currency(amount) -> str:
        """Format amount as currency"""
        try:
            amount = Decimal(str(amount))
            return f"{CURRENCY_SYMBOL} {amount:,.{DECIMAL_PLACES}f}"
        except:
            return f"{CURRENCY_SYMBOL} 0.00"
    
    @staticmethod
    def format_date(date_obj) -> str:
        """Format date object"""
        if isinstance(date_obj, str):
            return date_obj
        try:
            return date_obj.strftime(DATE_FORMAT)
        except:
            return str(date_obj)
    
    @staticmethod
    def format_datetime(datetime_obj) -> str:
        """Format datetime object"""
        if isinstance(datetime_obj, str):
            return datetime_obj
        try:
            return datetime_obj.strftime(DATETIME_FORMAT)
        except:
            return str(datetime_obj)
    
    @staticmethod
    def format_percentage(value, total) -> str:
        """Format as percentage"""
        if total == 0:
            return "0%"
        try:
            percentage = (value / total) * 100
            return f"{percentage:.2f}%"
        except:
            return "0%"
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """Format phone number"""
        phone = str(phone).replace(" ", "").replace("-", "")
        if len(phone) >= 10:
            return f"+{phone}" if not phone.startswith("+") else phone
        return phone
    
    @staticmethod
    def format_student_id(student_number: int) -> str:
        """Format student ID"""
        return f"STD-{student_number:04d}"
    
    @staticmethod
    def format_teacher_id(teacher_number: int) -> str:
        """Format teacher ID"""
        return f"TCH-{teacher_number:04d}"
    
    @staticmethod
    def format_receipt_number(date: datetime, receipt_number: int) -> str:
        """Format receipt number"""
        date_str = date.strftime("%Y%m%d")
        return f"RCP-{date_str}-{receipt_number:04d}"
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    @staticmethod
    def format_number(number, decimals=2) -> str:
        """Format number with decimal places"""
        try:
            return f"{float(number):,.{decimals}f}"
        except:
            return "0.00"
    
    @staticmethod
    def format_month_name(month_str: str) -> str:
        """Format month string (YYYY-MM to readable format)"""
        try:
            date_obj = datetime.strptime(month_str, "%Y-%m")
            return date_obj.strftime("%B %Y")
        except:
            return month_str
    
    @staticmethod
    def format_name(name: str) -> str:
        """Format name (Title case)"""
        return ' '.join(word.capitalize() for word in name.split())
    
    @staticmethod
    def truncate_text(text: str, length: int = 50) -> str:
        """Truncate text to specified length"""
        if len(text) > length:
            return text[:length-3] + "..."
        return text
    
    @staticmethod
    def format_balance_status(balance: Decimal) -> str:
        """Format balance status"""
        if balance <= 0:
            return "Paid"
        else:
            return f"Pending: {Formatter.format_currency(balance)}"
    
    @staticmethod
    def format_payment_status(status: str) -> str:
        """Format payment status"""
        status_map = {
            'completed': '✓ Completed',
            'pending': 'Pending',
            'failed': '✗ Failed',
            'cancelled': 'Cancelled'
        }
        return status_map.get(status.lower(), status)
