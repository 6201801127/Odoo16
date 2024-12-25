{
    'name': 'Custom Dashboard',
    "description": """This is hd dashboard there we can overview employe record and leave count""",
    'version': '16.0.0.0',
    'category': 'Dashboard',
    'author': 'Ajay Kumar Ravidas',
    'summary': 'HR dashboard module',
    'website': 'https://www.ask-tech.com/',
    'depends': ['base', 'hr', 'hr_holidays'],
    'data': [
        'security/security.xml',
        'views/custom_dashboard_view.xml',
        'views/hr_employee_inherit_view.xml'
    ],
    'demo': [
        # Include demo data here, if any
    ],
    'installable': True,
    'application': True,
    'sequence': '1',
    'qweb': [
        # include qweb report
    ],
    'assets': {
        'web.assets_backend': [
            '/custom_dashboard/static/src/js/custom_dashboard.js',
            '/custom_dashboard/static/src/xml/custom_dashboard.xml']
    },
    'license': 'LGPL-3',
    'images':['static/description/icon.png']
}
