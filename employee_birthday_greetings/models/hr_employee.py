# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import date, datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def birthday_mail_method(self):
        ctx = self._context.copy()
        template_id = self.env.ref(
            "employee_birthday_greetings.email_template_employee_birthday_notification")
        for employee in self.search([]):
            if employee.birthday:
                current_date = date.today()
                employee_birthday = datetime.strptime(
                    employee.birthday, "%Y-%m-%d")
                full_year_passed = (current_date.month, current_date.day) == (
                    employee_birthday.month, employee_birthday.day)
                if full_year_passed:
                    ctx.update({'body_action':
                                self.env.user.company_id.body_action,
                                'report_header': employee.user_id.report_header or
                                self.env.user.company_id.report_header,
                                'report_footer': employee.user_id.report_footer or
                                self.env.user.company_id.report_footer})
                    template_id.with_context(ctx).send_mail(employee.id)
