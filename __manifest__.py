{
    'name': 'Client Retainer & SLA Tracker',
    'summary': 'Client Retainer & SLA Tracker',
    'description': """
        Internal tool for a consulting agency to track retainer clients, 
        recurring monthly engagements with a fixed hour allowance, a tier, and renewal dates.
    """,
    'author': 'Chike Chiagbaizu',
    'maintainer': 'Chike Chiagbaizu',
    'version': '19.0.1.0.1',
    'license': 'LGPL-3',
    'category': 'Operations',
    'sequence': 1,
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'contacts'
        ],
    'data': [
        'security/retainer_security_groups.xml',
        'security/ir.model.access.csv',
        'security/retainer_rule.xml',
        'views/client_retainer_kanban_view.xml',
        'views/client_retainer_form_view.xml',
        'views/client_retainer_list_view.xml',
        'views/client_retainer_actions.xml',
        'views/res_partner_views.xml',
        'views/client_retainer_menus.xml',
    ],
}
