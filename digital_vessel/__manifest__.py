    # -*- coding: utf-8 -*-
{
    'name': "JPPI - Digital Vessel",

    'summary': """ Modul Digital Vessel """,
    'description': """ Modul Digital Vessel """,
    'author': "PT JPPI - Geger Gemilank",
    'website': "http://www.jppi.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','uom','hr'],

    'data': [
         'security/ir.model.access.csv',
         'views/config.xml',
         'views/pm.xml',
         'views/repair.xml',
         'views/sequence.xml',
         'views/ins_harian.xml',
         'reports/pm_report.xml',
         'reports/report_pdf.xml',
         'reports/repair_report.xml',
         'reports/lk_report.xml',
         'reports/lp_report.xml',
         'reports/docking_report.xml',
         'reports/wi_report.xml',
         'reports/ops_report.xml',
         # 'views/stage.xml',


    ],
    
    'demo': [],
}