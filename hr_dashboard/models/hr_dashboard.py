from datetime import datetime, timedelta
from odoo import fields, models, api


class HrEmployee(models.Model):
    """Inherit Hr employee """
    _inherit = 'hr.employee'

    emp_dob = fields.Date(string="DOB")
    str_emp_dob = fields.Char(string="DOB STR", compute='_compute_emp_dob', store=True)

    @api.depends('emp_dob')
    def _compute_emp_dob(self):
        """Convert the emp_dob to a string and store it in str_emp_dob."""
        for rec in self:
            if rec.emp_dob:
                # Convert the date to string format (you can change the format as needed)
                rec.str_emp_dob = rec.emp_dob.strftime(
                    '%d-%m')
            else:
                rec.str_emp_dob = ""

    @api.model
    def get_leave_days_by_state(self, employee_id, leave_state='validate'):
        """Calculate total leave days for an employee within the current month based on the specified state."""
        today = datetime.today()
        # Get the first day of the current month
        first_day_of_month = today.replace(day=1)
        # Get the last day of the current month (first day of the next month minus 1 day)
        # This will get us to the next month
        next_month = today.replace(day=28) + timedelta(days=4)
        last_day_of_month = next_month.replace(day=1) - timedelta(days=1)
        # Filter for leaves within the current month and the given state
        leaves = self.env['hr.leave'].search([
            ('employee_id', '=', employee_id),
            ('state', '=', leave_state),
            ('date_from', '<=', last_day_of_month),
            ('date_to', '>=', first_day_of_month),
        ])
        total_leave_days = 0
        # Calculate the number of days for each leave record
        for leave in leaves:
            # Ensure date_from and date_to are within the current month
            # Max to ensure it's within the current month
            date_from = max(leave.date_from, first_day_of_month)
            # Min to ensure it's within the current month
            date_to = min(leave.date_to, last_day_of_month)
            # Calculate the number of days (including both start and end dates)
            # +1 to include the start date as a full day
            leave_days = (date_to - date_from).days + 1
            total_leave_days += leave_days

        return total_leave_days

    @api.model
    def fetch_emp_data(self):
        """Fetch employee data directly from models."""
        # Fetch all employees and validated leaves in a single query
        hr_emp_rec = self.env['hr.employee'].search([])  # Fetch all employees
        leave_rec = self.env['hr.leave'].search(
            [('state', '=', 'validate')])  # Fetch validated leaves

        # Create a dictionary to map employee_id to leave counts
        leave_count_dict = {}
        for leave in leave_rec:
            employee_id = leave.employee_id.id
            leave_count_dict[employee_id] = leave_count_dict.get(
                employee_id, 0) + 1

        result = []
        for rec in hr_emp_rec:
            # Get leave counts for the current employee (validated, draft, cancel, pending)
            approved_leave_days = self.get_leave_days_by_state(
                rec.id, leave_state='validate')
            draft_leave_days = self.get_leave_days_by_state(
                rec.id, leave_state='draft')
            cancel_leave_days = self.get_leave_days_by_state(
                rec.id, leave_state='cancel')
            pending_leave_days = self.get_leave_days_by_state(
                rec.id, leave_state='confirm')
            emp_data = {
                "id": rec.id,
                "name": rec.name,
                "department": rec.department_id.name if rec.department_id.name else '',
                "work_email": rec.work_email,
                "work_phone": rec.work_phone,
                "designation": rec.job_title,
                'dob': rec.emp_dob,
                "draft_leave_count": draft_leave_days,
                "pending_leave_count": pending_leave_days,
                "validate_leave_count": approved_leave_days,
                "cancel_leave_count": cancel_leave_days,
                "today_birthday": [
                    {'name': rec.name if rec.str_emp_dob == datetime.today().strftime('%d-%m') else 'No Birthday today',
                     'dob_string': datetime.today().strftime('%d-%m-%Y') if rec.str_emp_dob == datetime.today().strftime('%d-%m') else ''}

                ]  # If today_birthday exists, include it, otherwise set as emp string
            }
            result.append(emp_data)

        return result
