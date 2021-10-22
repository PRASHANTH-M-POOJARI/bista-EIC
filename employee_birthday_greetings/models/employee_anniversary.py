# -*- coding: utf-8 -*-
import base64
import mimetypes

from odoo import api, models, fields
from datetime import date, datetime
from odoo.tools import misc, os, relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    confirmation_date = fields.Date(compute='_calculate_month', string='Confirmation Date')
    count_year = fields.Integer(compute='onchange_count_years', string='years count')
    email_sent = fields.Boolean("Email", default=False)

    @api.depends('confirmation_date')
    def onchange_count_years(self):
        for rec in self:
            current_date = date.today()
            anniversary_date = datetime.strptime(rec.confirmation_date, "%Y-%m-%d")
            year_date = relativedelta(anniversary_date, current_date).years
            rec.count_year = year_date

    @api.model
    def employee_anniversary_action(self):
        ctx = self._context.copy()
        print ('ctx', ctx)
        template_id = self.env.ref(
            "employee_birthday_greetings.email_template_employee_anniversary")
        for record in self.search([]):
            if record.confirmation_date:
                current_date = date.today()
                employee_anniversary = datetime.strptime(
                    record.confirmation_date, "%Y-%m-%d")
                one_full_year_passed = (current_date.month, current_date.day) == (
                    employee_anniversary.month, employee_anniversary.day)
                if one_full_year_passed:
                    ctx.update({'anniversary_email': self.env.user.company_id.anniversary_email})
                    template_id.with_context(ctx).send_mail(record.id)

                    # session_ids = self.env['hr.employee'].search([('email_sent', '=', False)])
                    # print('session_ ids', session_ids)
                    # for session in session_ids:
                    #     if session.email_sent is False:
                    #         session.send_email_with_attachment()
                            # session.email_sent = True

    # def send_email_with_attachment(self):
    #     template = self.env.ref("employee_birthday_greetings.email_template_employee_anniversary")
    #     report_template_id = self.env.ref(
    #         'employee_birthday_greetings.employee_anniversary_action_id').render_qweb_pdf(self.id)
    #     data_record = base64.b64encode(report_template_id[0])
    #     ir_values = {
    #         'name': "Employee Anniversary Report",
    #         'type': 'binary',
    #         'datas': data_record,
    #         'mimetype': 'application/x-pdf',
    #     }
    #     data_id = self.env['ir.attachment'].create(ir_values)
    #     template.attachment_ids = [(6, 0, [data_id.id])]
    #     template.send_mail(self.id, force_send=True)
    #     template.attachment_ids = [(3, data_id.id)]
    #     return True

