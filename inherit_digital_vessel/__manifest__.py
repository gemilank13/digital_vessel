    # -*- coding: utf-8 -*-
{
    'name': "JPPI - Inherit Digital Vessel",

    'summary': """ Modul Inherit Digital Vessel """,
    'description': """ Modul Digital Vessel """,
    'author': "PT JPPI - Adelia",
    'website': "http://www.jppi.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','uom','hr', 'digital_vessel', 'board'],

    'data': [
         'security/security.xml',
         'security/ir.model.access.csv',
         'views/view.xml',
         'views/docking.xml',
         'views/weekly.xml',
         'views/daily.xml',
         'views/sequence.xml',
        #  'reports/pm_report.xml',
        #  'reports/report_pdf.xml',
         'views/dashboard.xml',


    ],
    
    'demo': [],
}