{
    'name': "Novobi Sales B2B",
    'summary': "Addons feature for B2B Sales",
    'description': """
Manage Sales
==============
Description related to Sales.
    """,
    'author': "Alan Pham",
    'website': "http://www.example.com",
    'category': 'Sales',
    'version': '14.0.1',
    'depends': ['base', 'sale', 'website'],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/salesperson_security.xml',
        # data
        'data/mail_template.xml',
        'data/delivery_order_sent_email.xml',
        # wizard
        'wizard/sale_request_wizard_view.xml',
        # view
        'views/sale_request.xml',
        'views/request_portal.xml',
        'views/create_sale_request_portal.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'novobi_sales_b2b/static/src/js/app.js',
            'novobi_sales_b2b/static/src/js/create_order.js',
            'novobi_sales_b2b/static/src/css/page.css',
            'novobi_sales_b2b/static/src/scss/page.scss'
        ],
    }
}
