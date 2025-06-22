{
    'name': 'HMS3',
    'version': '0.3',
    'author': 'Ahmed',
    'category': 'Healthcare',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/dept_views.xml',
        'views/doctor_views.xml',
        'views/res_partner_views.xml',
        'views/patient_views.xml',
    ],
    'application': True,
    'installable': True
}