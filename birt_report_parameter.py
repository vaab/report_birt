# -*- coding: utf-8 -*-

from osv import osv, fields


class Parameter(osv.osv):

    _name = 'report_birt.parameter'

    _columns = {
        'identifier': fields.char(
            'Identifier',
            size=256,
            help="Identifier Label",
            required=True),
        'is_literal': fields.boolean(
            'Fixed String',
            help="should the identifier considered as a direct fixed string?"),
        'value': fields.char(
            'Value',
            size=256,
            help="As Label",
            required=True),
        'parent_id': fields.many2one(
            'ir.actions.report.xml',
            'parent object'),
    }

    _defaults = {}

