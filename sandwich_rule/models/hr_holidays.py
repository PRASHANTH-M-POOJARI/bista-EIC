# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import date, timedelta


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    sandwich_rule = fields.Boolean('Sandwich Rule')
    hr_consider_sandwich_rule = fields.Boolean('Apply Sandwich Rule', default=True)

    @api.onchange('number_of_days_temp', 'hr_consider_sandwich_rule')
    def check_leave_type(self, day=None):
        start_date = datetime.datetime.strptime(self.date_from.split(' ')[0], '%Y-%m-%d')
        till_leave_date = datetime.datetime.strptime(self.date_to.split(' ')[0], '%Y-%m-%d')
        number_date = start_date.weekday()
        applied_from_date = datetime.datetime.strptime(self.date_from.split(' ')[0], '%Y-%m-%d')
        print("APPLIED DATE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", applied_from_date)
        last_leave = self.env['hr.holidays'].search([('employee_id', '=', self.employee_id.id), ('type', '=', 'remove')],order="id desc", limit=1)
        if last_leave:
            last_leave_date = datetime.datetime.strptime(last_leave.date_from.split(' ')[0], '%Y-%m-%d')
            print("n/n/n/n/n8")
            print("LAST LEAVE DATE>>>>>>>>>>>>>>>>>>>>>>>>>>>>", last_leave_date)
            if applied_from_date > last_leave_date:
                d1 = applied_from_date
                d2 = last_leave_date
                gap_days = (d1 - d2).days
                print("gap days", gap_days)
                print("Last Leave-----------", last_leave)
                if gap_days <= 3 and number_date == 0 and number_date != 4 and number_date != 3 and number_date != 2:
                    print("last_friday_at_16 ")
                    if gap_days <= 3 and number_date == 0 and number_date != 4 and number_date != 3 and number_date != 2:
                        self.number_of_days_temp = 2 + self.number_of_days_temp
                        print(">>111", self.number_of_days_temp)

        if self.hr_consider_sandwich_rule and self.employee_id and self.number_of_days_temp:
            days = []
            for each in self.employee_id.resource_calendar_id.attendance_ids:
                if int(each.dayofweek) not in days:
                    days.append(int(each.dayofweek))
            if self.date_from:
                leave_ids = self.env['hr.holidays'].search([('employee_id', '=', self.employee_id.id)])
                start_date = datetime.datetime.strptime(self.date_from.split(' ')[0], '%Y-%m-%d')
                number_date = start_date.weekday()
                end_to = datetime.datetime.strptime(self.date_to.split(' ')[0], '%Y-%m-%d')
                end_number_date = end_to.weekday()
                date_list = []
                if number_date == 0:
                    date_list.append(start_date - datetime.timedelta(days=1))
                    date_list.append(start_date - datetime.timedelta(days=2))
                    if max(days) == 4:
                        date_list.append(start_date - datetime.timedelta(days=3))
                if end_number_date == 1:
                    date_list.append(start_date - datetime.timedelta(days=1))
                    date_list.append(start_date - datetime.timedelta(days=2))
                    if max(days) == 4:
                        date_list.append(start_date - datetime.timedelta(days=3))
                if number_date == 4:
                    if max(days) == 4:
                        date_list.append(start_date + datetime.timedelta(days=1))
                        date_list.append(start_date + datetime.timedelta(days=2))
                        date_list.append(start_date + datetime.timedelta(days=3))
                if number_date == 5:
                    if max(days) == 5:
                        date_list.append(start_date + datetime.timedelta(days=1))
                        date_list.append(start_date + datetime.timedelta(days=2))
                for each in leave_ids:
                    if each.date_from:
                        if datetime.datetime.strptime(each.date_from.split(' ')[0], '%Y-%m-%d') in date_list:
                            self.sandwich_rule = True

            if self.number_of_days_temp and self.date_from:
                start_date = self.date_from.split(' ')[0]
                end_date = self.date_to.split(' ')[0]
                number_of_leave = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.datetime.strptime(
                    start_date, '%Y-%m-%d').date()
                cnt = 0
                if number_of_leave:
                    rngs = 0
                    if 'days' in str(number_of_leave):
                        rngs = int(str(number_of_leave).split(' days,')[0])
                    else:
                        rngs = int(str(number_of_leave).split(' day,')[0])
                    live_list = []
                    for d_ord in range(rngs + 1):
                        day = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=cnt)
                        cnt = cnt + 1
                        if max(days) == 4:
                            if int(day.weekday()) == 5 or int(day.weekday()) == 6:
                                self.number_of_days_temp = rngs
                        if max(days) == 5:
                            if int(day.weekday()) == 6:
                                self.number_of_days_temp = rngs
                        live_list.append(day.weekday())
                    if max(days) == 4:
                        if 5 in live_list:
                            if 6 in live_list:
                                self.number_of_days_temp = 1 + rngs
                                print(self.number_of_days_temp)
                                self.sandwich_rule = True
                                print("self1", self.sandwich_rule)
                            else:
                                self.sandwich_rule = False
                    if max(days) == 4:
                        if self.sandwich_rule and number_date == 1 and 5 in live_list:
                            print("<<<")
                            if number_date == 1 and 6 in live_list:
                                self.number_of_days_temp = 0 + self.number_of_days_temp
                                print("LL", self.number_of_days_temp)
                        else:
                            last_leave_date1 = datetime.datetime.strptime(last_leave.date_from.split(' ')[0], '%Y-%m-%d')
                            d1 = till_leave_date
                            d2 = applied_from_date
                            d3 = applied_from_date
                            d4 = last_leave_date1
                            gap_days = (d3 - d4).days
                            gap_day = (d1 - d2).days
                            print("gggg", gap_day)
                            if gap_day > 4  and gap_days <= 3 and 5 in live_list and number_date != 4 and number_date != 3 and number_date != 2:
                                if gap_day > 4 and gap_days <= 3 and 6 in live_list and number_date != 4 and number_date != 3 and number_date != 2:
                                    self.number_of_days_temp = 2 + self.number_of_days_temp
                                    print("ee", self.number_of_days_temp)

                    if max(days) == 5:
                        if 6 in live_list:
                            self.sandwich_rule = True
                            print("self2", self.sandwich_rule)
        else:
            if self.employee_id and self.date_from and self.date_to:
                self.sandwich_rule = False
                self.number_of_days_temp = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)

    @api.onchange('date_from', 'date_to')
    def check_date_from_live(self):
        res = {}
        if self.employee_id:
            days = []
            for each in self.employee_id.resource_calendar_id.attendance_ids:
                if int(each.dayofweek) not in days:
                    days.append(int(each.dayofweek))
            if self.date_from:
                start_date = datetime.datetime.strptime(self.date_from.split(' ')[0], '%Y-%m-%d')
                date_number = start_date.weekday()
                if date_number not in days:
                    res.update(
                        {'value': {'date_to': '', 'date_from': '', 'number_of_days_temp': 0.00, 'sandwich_rule': False},
                         'warning': {
                             'title': 'Validation!', 'message': 'This day is already holiday.'}})
            if self.date_to:
                end_date = datetime.datetime.strptime(self.date_to.split(' ')[0], '%Y-%m-%d')
                date_number = end_date.weekday()
                if date_number not in days:
                    res.update(
                        {'value': {'date_to': '', 'number_of_days_temp': 0.00, 'sandwich_rule': False}, 'warning': {
                            'title': 'Validation!', 'message': 'This day is already holiday.'}})

        return res

    @api.onchange('date_from', 'date_to')
    def auto_time_for_date(self):
        start_line = fields.Datetime.from_string(self.date_from)
        deadline = fields.Datetime.from_string(self.date_to)
        date_from = start_line.replace(hour=5, minute=00, second=00)
        date_to = deadline.replace(hour=18, minute=00, second=00)
        self.date_from = date_from
        self.date_to = date_to

    @api.onchange('date_from', 'date_to')
    def auto_sandwitch_false(self):
        start_date = datetime.datetime.strptime(self.date_from.split(' ')[0], '%Y-%m-%d')
        number_date = start_date.weekday()
        end_to = datetime.datetime.strptime(self.date_to.split(' ')[0], '%Y-%m-%d')
        end_number_date = end_to.weekday()
        if number_date == 1 and end_number_date == 1:
            self.sandwich_rule = False
            print("self.sandwich_rule", self.sandwich_rule)
        if number_date == 4 and end_number_date == 4:
            self.sandwich_rule = False

