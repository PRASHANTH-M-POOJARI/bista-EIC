# -*- coding: utf-8 -*-
{
    'name': 'Employee Birthday Greetings',
    'category': 'Generic Modules/Human Resources',
    'version': '11.0.1.0.0',
    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'license': 'AGPL-3',
    'description': 'Automated system for sending greetings to employee on their birthday.',
    'summary': """
        User can set the Customised email format for there employees.And when 
        the Bigday for employee arrived he/she will receive the Greetings.""",

    'license': "AGPL-3",

    'depends': ['base', 'mail', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'data/employee_birthday_email_template.xml',
        'data/birthday_mail_scheduler.xml',
        'data/employee_anniversary_email_template.xml',
        'data/employee_anniversary_mail_scheduler.xml',
        'views/res_company_view.xml',
        'views/res_users_view.xml',
        'views/employee_anniversary_views.xml',
        'views/employee_probation_period.xml',
        'data/employee_probation_period_scheduler.xml',
        'data/employee_probation_period_template.xml',
    ],

    'images': [
        'static/description/banner.jpg',
    ],

    'auto_install': False,
    'installable': True,
    'application': False

}
