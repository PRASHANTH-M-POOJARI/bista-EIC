# -*- coding: utf-8 -*-

# © 2018-Today Aktiv Software (http://www.aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    body_action = fields.Html(string='Body Action')
    report_header = fields.Html(string='Report Header')
    report_footer = fields.Html(string='Report Footer')
    anniversary_email = fields.Html(string='Employee Anniversary')
