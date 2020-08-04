# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (C) Solvate Informationstechnologie GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'SIT Contact Customisation',
    'summary': '''SIT Contact Customisation''',
    'description': '''SIT Contact Customisation''',
    'author': 'Solvate IT',
    'support': 'Service@Solvate.at',
    'website': 'http://www.Solvate.at',
    'version': '13.0.1.0.0',
    'category': 'Contact',
    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_view.xml',
        'views/res_partner_category_view.xml',
    ],
    'qweb': '',
    'external_dependencies': {
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
