# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools import misc, os, relativedelta
import datetime
from datetime import date, datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date('Joining Date')
    hr_id = fields.Many2one('hr.employee', string='Hr')

    @api.depends('joining_date')
    def _calculate_month(self):
        for rec in self:
            if rec.joining_date:
                Date_Start = datetime.strptime(rec.joining_date, "%Y-%m-%d")
                print("Start Date", Date_Start)
                six_months_after = Date_Start + relativedelta(months=6)
                print("After six month", six_months_after)
                rec.confirmation_date = six_months_after
                print ("end month:", rec.confirmation_date)

    @api.model
    def employee_probation_period_action(self):
        template_id = self.env.ref(
            "employee_birthday_greetings.email_template_probation_period")
        for record in self.search([]):
            if record.confirmation_date:
                Date_Start = datetime.strptime(record.joining_date, "%Y-%m-%d")
                employee_confirmation_date = datetime.strptime(
                    record.confirmation_date, "%Y-%m-%d")
                six_months_after = Date_Start + relativedelta(months=6)
                one_half_year_passed = six_months_after == employee_confirmation_date
                print ('one half', one_half_year_passed)
                if one_half_year_passed:
                    # modified_date = datetime.datetime.strptime(self.employee_confirmation_date, "%Y-%m-%d").date().strftime("%d-%m-%Y %a")
                    # template_id.with_context(
                    #     {
                    #         'date_scheduled': modified_date
                    #     })
                    template_id.send_mail(record.id, force_send=True)
