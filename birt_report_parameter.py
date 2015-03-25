# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class Parameter(osv.osv):

    _name = 'report_birt.parameter'

    _columns = {
        'name': fields.char(
            'Name',
            size=64,
            help="Param Label",
            required=True),
        'value': fields.char(
            'Value',
            size=256,
            help="Value",
            required=True),
        'eval': fields.boolean(
            'Eval',
            help="should the value be evaled as python string ?"),
        'parent_id': fields.many2one(
            'ir.actions.report.xml',
            'parent object'),
    }

    _defaults = {
        "eval": True
    }

## Compatibility with 6.0.3
Parameter()

