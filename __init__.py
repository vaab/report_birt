# -*- coding: utf-8 -*-

import birt_report
import birt_report_parameter
import ir_report


## Monkey patching to add a new type of reports:

from openerp.addons.base.ir.ir_actions import ir_actions_report_xml

column = ir_actions_report_xml._columns['report_type']
if getattr(column, '_type', False) == 'selection':
    ## then it's a v8
    column.selection.append(('birt', 'BIRT report'))
