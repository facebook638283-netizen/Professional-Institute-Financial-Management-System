# Receipt Generator for thermal printers

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from config import INSTITUTE_NAME, INSTITUTE_ADDRESS, INSTITUTE_PHONE, INSTITUTE_EMAIL, CURRENCY_SYMBOL
from utils.formatters import Formatter

class ReceiptGenerator:
    """Generate receipts in various formats"""
    
    def __init__(self, institute_name=INSTITUTE_NAME, institute_address=INSTITUTE_ADDRESS, 
                 institute_phone=INSTITUTE_PHONE, institute_email=INSTITUTE_EMAIL):
        self.institute_name = institute_name
        self.institute_address = institute_address
        self.institute_phone = institute_phone
        self.institute_email = institute_email
    
    def generate_thermal_receipt(self, receipt_data, width_mm=58):
        """Generate receipt for thermal printer"""
        receipt_text = self._generate_receipt_text(receipt_data, width_mm)
        return receipt_text
    
    def _generate_receipt_text(self, receipt_data, width_mm):
        """Generate plain text receipt"""
        char_width = 32 if width_mm == 58 else 42
        
        lines = []
        lines.append("=" * char_width)
        lines.append(self._center_text(self.institute_name, char_width))
        lines.append(self._center_text(self.institute_address, char_width))
        lines.append(self._center_text(self.institute_phone, char_width))
        lines.append(self._center_text(self.institute_email, char_width))
        lines.append("=" * char_width)
        lines.append("")
        
        lines.append(self._left_right_text("RECEIPT", receipt_data['receipt_number'], char_width))
        lines.append(self._center_text(datetime.now().strftime("%d-%b-%Y %H:%M:%S"), char_width))
        lines.append("-" * char_width)
        lines.append("")
        
        lines.append("STUDENT INFORMATION:")
        lines.append(self._left_right_text("ID:", receipt_data['student_id'], char_width))
        lines.append(self._wrap_text(f"Name: {receipt_data['student_name']}", char_width))
        lines.append(self._wrap_text(f"Father: {receipt_data['father_name']}", char_width))
        lines.append(self._wrap_text(f"Class: {receipt_data['class_name']}", char_width))
        lines.append("")
        
        lines.append("PAYMENT DETAILS:")
        lines.append(self._left_right_text("Month:", receipt_data['payment_month'], char_width))
        lines.append(self._left_right_text("Monthly Fee:", 
                                          Formatter.format_currency(receipt_data['monthly_fee']), 
                                          char_width))
        lines.append(self._left_right_text("Paid Amount:", 
                                          Formatter.format_currency(receipt_data['paid_amount']), 
                                          char_width))
        lines.append(self._left_right_text("Discount:", 
                                          Formatter.format_currency(receipt_data['discount']), 
                                          char_width))
        lines.append(self._left_right_text("Remaining:", 
                                          Formatter.format_currency(receipt_data['remaining_balance']), 
                                          char_width))
        lines.append("-" * char_width)
        lines.append("")
        
        lines.append(self._center_text("Thank You!", char_width))
        lines.append(self._center_text("For Your Payment", char_width))
        lines.append("=" * char_width)
        lines.append(self._center_text(f"Cashier: {receipt_data.get('cashier_name', 'N/A')}", char_width))
        lines.append(self._center_text(datetime.now().strftime("%d-%b-%Y"), char_width))
        lines.append("=" * char_width)
        
        return "\n".join(lines)
    
    def generate_pdf_receipt(self, receipt_data, output_path=None):
        """Generate PDF receipt"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        
        if output_path is None:
            output_path = f"receipts/receipt_{receipt_data['receipt_number']}.pdf"
        
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        
        y = height - 50
        
        # Header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, self.institute_name)
        y -= 20
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, self.institute_address)
        y -= 15
        c.drawString(50, y, f"Phone: {self.institute_phone}")
        y -= 15
        c.drawString(50, y, f"Email: {self.institute_email}")
        y -= 30
        
        # Receipt header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "RECEIPT")
        c.drawRightString(width - 50, y, receipt_data['receipt_number'])
        y -= 20
        
        c.setFont("Helvetica", 10)
        c.drawString(50, y, datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
        y -= 30
        
        # Student Information
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "STUDENT INFORMATION")
        y -= 15
        
        c.setFont("Helvetica", 10)
        c.drawString(70, y, f"Student ID: {receipt_data['student_id']}")
        y -= 15
        c.drawString(70, y, f"Name: {receipt_data['student_name']}")
        y -= 15
        c.drawString(70, y, f"Father's Name: {receipt_data['father_name']}")
        y -= 15
        c.drawString(70, y, f"Class: {receipt_data['class_name']}")
        y -= 30
        
        # Payment Details
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "PAYMENT DETAILS")
        y -= 15
        
        c.setFont("Helvetica", 10)
        payment_details = [
            ("Payment Month:", receipt_data['payment_month']),
            ("Monthly Fee:", Formatter.format_currency(receipt_data['monthly_fee'])),
            ("Paid Amount:", Formatter.format_currency(receipt_data['paid_amount'])),
            ("Discount:", Formatter.format_currency(receipt_data['discount'])),
            ("Remaining Balance:", Formatter.format_currency(receipt_data['remaining_balance'])),
        ]
        
        for label, value in payment_details:
            c.drawString(70, y, label)
            c.drawRightString(width - 70, y, value)
            y -= 15
        
        y -= 20
        
        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Cashier: {receipt_data.get('cashier_name', 'N/A')}")
        y -= 15
        c.drawString(50, y, f"Print Date: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        y -= 30
        
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, y, "Thank You!")
        
        c.save()
        return output_path
    
    @staticmethod
    def _center_text(text, width):
        """Center align text"""
        padding = (width - len(str(text))) // 2
        return " " * max(0, padding) + str(text)
    
    @staticmethod
    def _left_right_text(left, right, width):
        """Create left-right aligned text"""
        left_str = str(left)
        right_str = str(right)
        middle_padding = width - len(left_str) - len(right_str)
        return left_str + " " * max(1, middle_padding) + right_str
    
    @staticmethod
    def _wrap_text(text, width):
        """Wrap text to width"""
        if len(text) <= width:
            return text
        
        wrapped = []
        current_line = ""
        words = text.split()
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += word + " "
            else:
                if current_line:
                    wrapped.append(current_line.rstrip())
                current_line = word + " "
        
        if current_line:
            wrapped.append(current_line.rstrip())
        
        return "\n".join(wrapped)
