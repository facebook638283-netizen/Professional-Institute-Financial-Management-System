# Report Generator for various formats

from datetime import datetime, timedelta
from pathlib import Path
from decimal import Decimal
import csv
import json
from database.db_manager import DatabaseManager
from utils.formatters import Formatter
from config import INSTITUTE_NAME, REPORTS_DIR

class ReportGenerator:
    """Generate reports in various formats (PDF, Excel, TXT, JSON)"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.institute_name = INSTITUTE_NAME
    
    def generate_daily_report(self, date, format='txt'):
        """Generate daily financial report"""
        try:
            summary = self.db.get_daily_summary(date)
            
            if format == 'txt':
                return self._generate_daily_txt_report(summary)
            elif format == 'csv':
                return self._generate_daily_csv_report(summary)
            elif format == 'json':
                return self._generate_daily_json_report(summary)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Error generating daily report: {str(e)}")
    
    def generate_monthly_report(self, month, format='txt'):
        """Generate monthly financial report"""
        try:
            summary = self.db.get_monthly_summary(month)
            students = self.db.get_all_students()
            fees_collected = self.db.get_expenses_by_month(month)
            
            if format == 'txt':
                return self._generate_monthly_txt_report(summary, students, fees_collected)
            elif format == 'csv':
                return self._generate_monthly_csv_report(summary)
            elif format == 'json':
                return self._generate_monthly_json_report(summary)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Error generating monthly report: {str(e)}")
    
    def generate_student_report(self, filters=None, format='txt'):
        """Generate student report"""
        try:
            students = self.db.get_all_students()
            
            # Apply filters
            if filters:
                if 'class_name' in filters:
                    students = [s for s in students if s.class_name == filters['class_name']]
                if 'fee_status' in filters:
                    if filters['fee_status'] == 'pending':
                        current_month = datetime.now().strftime("%Y-%m")
                        student_ids_paid = [p.student_id for p in self.db.db.query(
                            self.db.db.SessionLocal().query(
                                from database.models import FeePayment
                                where FeePayment.payment_month == current_month
                            )
                        )]
                        students = [s for s in students if s.student_id not in student_ids_paid]
            
            if format == 'txt':
                return self._generate_student_txt_report(students)
            elif format == 'csv':
                return self._generate_student_csv_report(students)
            elif format == 'json':
                return self._generate_student_json_report(students)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Error generating student report: {str(e)}")
    
    def generate_teacher_report(self, format='txt'):
        """Generate teacher report"""
        try:
            teachers = self.db.get_all_teachers()
            
            if format == 'txt':
                return self._generate_teacher_txt_report(teachers)
            elif format == 'csv':
                return self._generate_teacher_csv_report(teachers)
            elif format == 'json':
                return self._generate_teacher_json_report(teachers)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Error generating teacher report: {str(e)}")
    
    def generate_financial_report(self, start_date, end_date, format='txt'):
        """Generate financial manager report"""
        try:
            # Calculate totals for the period
            total_income = Decimal('0')
            total_expenses = Decimal('0')
            
            current_date = start_date
            while current_date <= end_date:
                summary = self.db.get_daily_summary(current_date)
                total_income += Decimal(str(summary['total_income']))
                total_expenses += Decimal(str(summary['total_expenses']))
                current_date += timedelta(days=1)
            
            report_data = {
                'start_date': str(start_date),
                'end_date': str(end_date),
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'total_profit': float(total_income - total_expenses)
            }
            
            if format == 'txt':
                return self._generate_financial_txt_report(report_data)
            elif format == 'csv':
                return self._generate_financial_csv_report(report_data)
            elif format == 'json':
                return self._generate_financial_json_report(report_data)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Error generating financial report: {str(e)}")
    
    # ==================== TXT REPORT GENERATORS ====================
    
    def _generate_daily_txt_report(self, summary):
        """Generate daily report in TXT format"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"{self.institute_name} - DAILY REPORT".center(60))
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"Date: {Formatter.format_date(summary['date'])}")
        lines.append(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("INCOME SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Fee Collections:        {Formatter.format_currency(summary['fee_collection'])}")
        lines.append(f"Stock Sales:            {Formatter.format_currency(summary['stock_sales'])}")
        lines.append(f"Total Income:           {Formatter.format_currency(summary['total_income'])}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("EXPENSE SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Salary Payments:        {Formatter.format_currency(summary['salary_payments'])}")
        lines.append(f"Other Expenses:         {Formatter.format_currency(summary['expenses'])}")
        lines.append(f"Total Expenses:         {Formatter.format_currency(summary['total_expenses'])}")
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"PROFIT/LOSS:            {Formatter.format_currency(summary['profit'])}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _generate_monthly_txt_report(self, summary, students, expenses):
        """Generate monthly report in TXT format"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"{self.institute_name} - MONTHLY REPORT".center(60))
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"Month: {Formatter.format_month_name(summary['month'])}")
        lines.append(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("FINANCIAL SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Total Income:           {Formatter.format_currency(summary['total_income'])}")
        lines.append(f"Total Expenses:         {Formatter.format_currency(summary['total_expenses'])}")
        lines.append(f"Total Profit:           {Formatter.format_currency(summary['profit'])}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("BREAKDOWN")
        lines.append("-" * 60)
        lines.append(f"Fee Collections:        {Formatter.format_currency(summary['fee_collection'])}")
        lines.append(f"Stock Sales:            {Formatter.format_currency(summary['stock_sales'])}")
        lines.append(f"Salary Payments:        {Formatter.format_currency(summary['salary_payments'])}")
        lines.append(f"Other Expenses:         {Formatter.format_currency(summary['expenses'])}")
        lines.append("")
        lines.append("-" * 60)
        lines.append(f"Total Active Students:  {len([s for s in students if s.is_active])}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _generate_student_txt_report(self, students):
        """Generate student report in TXT format"""
        lines = []
        lines.append("=" * 100)
        lines.append(f"{self.institute_name} - STUDENT REPORT".center(100))
        lines.append("=" * 100)
        lines.append("")
        
        lines.append(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        lines.append("")
        lines.append("-" * 100)
        
        header = f"{'STD ID':<12} {'Name':<20} {'Father':<20} {'Class':<15} {'Balance':<15} {'Status':<10}"
        lines.append(header)
        lines.append("-" * 100)
        
        for student in students:
            balance = self.db.get_student_balance(student.student_id)
            status = "Paid" if balance <= 0 else "Pending"
            
            line = f"{student.student_id:<12} {Formatter.truncate_text(student.full_name, 19):<20} "
            line += f"{Formatter.truncate_text(student.father_name, 19):<20} "
            line += f"{student.class_name:<15} {Formatter.format_currency(balance):<15} {status:<10}"
            lines.append(line)
        
        lines.append("-" * 100)
        lines.append(f"Total Students: {len(students)}")
        lines.append("=" * 100)
        
        return "\n".join(lines)
    
    def _generate_teacher_txt_report(self, teachers):
        """Generate teacher report in TXT format"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"{self.institute_name} - TEACHER REPORT".center(80))
        lines.append("=" * 80)
        lines.append("")
        
        lines.append(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        lines.append("")
        lines.append("-" * 80)
        
        header = f"{'TCH ID':<12} {'Name':<20} {'Subject':<15} {'Salary':<15} {'Status':<10}"
        lines.append(header)
        lines.append("-" * 80)
        
        for teacher in teachers:
            line = f"{teacher.teacher_id:<12} {Formatter.truncate_text(teacher.full_name, 19):<20} "
            line += f"{teacher.subject:<15} {Formatter.format_currency(teacher.monthly_salary):<15} Active"
            lines.append(line)
        
        lines.append("-" * 80)
        lines.append(f"Total Teachers: {len(teachers)}")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _generate_financial_txt_report(self, report_data):
        """Generate financial report in TXT format"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"{self.institute_name} - FINANCIAL REPORT".center(60))
        lines.append("=" * 60)
        lines.append("")
        
        lines.append(f"Period: {report_data['start_date']} to {report_data['end_date']}")
        lines.append(f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("FINANCIAL SUMMARY")
        lines.append("-" * 60)
        lines.append(f"Total Income:           {Formatter.format_currency(report_data['total_income'])}")
        lines.append(f"Total Expenses:         {Formatter.format_currency(report_data['total_expenses'])}")
        lines.append(f"Net Profit:             {Formatter.format_currency(report_data['total_profit'])}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # ==================== CSV REPORT GENERATORS ====================
    
    def _generate_daily_csv_report(self, summary):
        """Generate daily report in CSV format"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([self.institute_name, "DAILY REPORT"])
        writer.writerow(["Date", Formatter.format_date(summary['date'])])
        writer.writerow([])
        writer.writerow(["Income Category", "Amount"])
        writer.writerow(["Fee Collections", summary['fee_collection']])
        writer.writerow(["Stock Sales", summary['stock_sales']])
        writer.writerow(["Total Income", summary['total_income']])
        writer.writerow([])
        writer.writerow(["Expense Category", "Amount"])
        writer.writerow(["Salary Payments", summary['salary_payments']])
        writer.writerow(["Other Expenses", summary['expenses']])
        writer.writerow(["Total Expenses", summary['total_expenses']])
        writer.writerow([])
        writer.writerow(["Profit/Loss", summary['profit']])
        
        return output.getvalue()
    
    def _generate_monthly_csv_report(self, summary):
        """Generate monthly report in CSV format"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([self.institute_name, "MONTHLY REPORT"])
        writer.writerow(["Month", Formatter.format_month_name(summary['month'])])
        writer.writerow([])
        writer.writerow(["Category", "Amount"])
        writer.writerow(["Total Income", summary['total_income']])
        writer.writerow(["Total Expenses", summary['total_expenses']])
        writer.writerow(["Total Profit", summary['profit']])
        
        return output.getvalue()
    
    def _generate_student_csv_report(self, students):
        """Generate student report in CSV format"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([self.institute_name, "STUDENT REPORT"])
        writer.writerow(["Generated", datetime.now().strftime('%d-%b-%Y %H:%M:%S')])
        writer.writerow([])
        writer.writerow(["Student ID", "Name", "Father's Name", "Class", "Phone", "Balance", "Status"])
        
        for student in students:
            balance = self.db.get_student_balance(student.student_id)
            status = "Paid" if balance <= 0 else "Pending"
            writer.writerow([
                student.student_id,
                student.full_name,
                student.father_name,
                student.class_name,
                student.phone_number or "N/A",
                balance,
                status
            ])
        
        return output.getvalue()
    
    def _generate_teacher_csv_report(self, teachers):
        """Generate teacher report in CSV format"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([self.institute_name, "TEACHER REPORT"])
        writer.writerow(["Generated", datetime.now().strftime('%d-%b-%Y %H:%M:%S')])
        writer.writerow([])
        writer.writerow(["Teacher ID", "Name", "Subject", "Monthly Salary", "Status"])
        
        for teacher in teachers:
            writer.writerow([
                teacher.teacher_id,
                teacher.full_name,
                teacher.subject,
                teacher.monthly_salary,
                "Active" if teacher.is_active else "Inactive"
            ])
        
        return output.getvalue()
    
    def _generate_financial_csv_report(self, report_data):
        """Generate financial report in CSV format"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([self.institute_name, "FINANCIAL REPORT"])
        writer.writerow(["Period", f"{report_data['start_date']} to {report_data['end_date']}"])
        writer.writerow([])
        writer.writerow(["Category", "Amount"])
        writer.writerow(["Total Income", report_data['total_income']])
        writer.writerow(["Total Expenses", report_data['total_expenses']])
        writer.writerow(["Net Profit", report_data['total_profit']])
        
        return output.getvalue()
    
    # ==================== JSON REPORT GENERATORS ====================
    
    def _generate_daily_json_report(self, summary):
        """Generate daily report in JSON format"""
        return json.dumps({
            'report_type': 'daily',
            'institute': self.institute_name,
            'date': str(summary['date']),
            'generated': datetime.now().isoformat(),
            'summary': {k: float(v) if isinstance(v, Decimal) else v for k, v in summary.items()}
        }, indent=2)
    
    def _generate_monthly_json_report(self, summary):
        """Generate monthly report in JSON format"""
        return json.dumps({
            'report_type': 'monthly',
            'institute': self.institute_name,
            'month': summary['month'],
            'generated': datetime.now().isoformat(),
            'summary': {k: float(v) if isinstance(v, Decimal) else v for k, v in summary.items()}
        }, indent=2)
    
    def _generate_student_json_report(self, students):
        """Generate student report in JSON format"""
        students_data = []
        for student in students:
            balance = self.db.get_student_balance(student.student_id)
            students_data.append({
                'student_id': student.student_id,
                'full_name': student.full_name,
                'father_name': student.father_name,
                'class': student.class_name,
                'phone': student.phone_number,
                'balance': float(balance),
                'status': 'Paid' if balance <= 0 else 'Pending'
            })
        
        return json.dumps({
            'report_type': 'students',
            'institute': self.institute_name,
            'generated': datetime.now().isoformat(),
            'total_students': len(students_data),
            'students': students_data
        }, indent=2)
    
    def _generate_teacher_json_report(self, teachers):
        """Generate teacher report in JSON format"""
        teachers_data = []
        for teacher in teachers:
            teachers_data.append({
                'teacher_id': teacher.teacher_id,
                'full_name': teacher.full_name,
                'subject': teacher.subject,
                'monthly_salary': float(teacher.monthly_salary),
                'status': 'Active' if teacher.is_active else 'Inactive'
            })
        
        return json.dumps({
            'report_type': 'teachers',
            'institute': self.institute_name,
            'generated': datetime.now().isoformat(),
            'total_teachers': len(teachers_data),
            'teachers': teachers_data
        }, indent=2)
    
    def _generate_financial_json_report(self, report_data):
        """Generate financial report in JSON format"""
        return json.dumps({
            'report_type': 'financial',
            'institute': self.institute_name,
            'period': {
                'start': report_data['start_date'],
                'end': report_data['end_date']
            },
            'generated': datetime.now().isoformat(),
            'summary': {k: float(v) if isinstance(v, Decimal) else v for k, v in report_data.items() if k not in ['start_date', 'end_date']}
        }, indent=2)
