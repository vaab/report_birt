# -*- coding: utf-8 -*-

from openerp import netsvc

from openerp.osv import osv, fields
from birt_report import BirtProxyFactory
from openerp.report.report_sxw import rml_parse


def register_report(name, model, tmpl_path, parser=rml_parse):
    "Register the report into the services"
    name = 'report.%s' % name
    if netsvc.Service._services.get(name, False):
        service = netsvc.Service._services[name]
        if isinstance(service, BirtProxyFactory):
            #already instantiated properly, skip it
            return
        if hasattr(service, 'parser'):
            parser = service.parser
        del netsvc.Service._services[name]
    BirtProxyFactory(name, model, tmpl_path, parser=parser)


class ReportBIRT(osv.osv):

    def __init__(self, pool, cr):
        super(ReportBIRT, self).__init__(pool, cr)

    def register_all(self,cursor):
        value = super(ReportBIRT, self).register_all(cursor)
        cursor.execute("SELECT * FROM ir_act_report_xml WHERE report_type = 'birt'")
        records = cursor.dictfetchall()
        for record in records:
            register_report(record['report_name'], record['model'], record['report_rml'])
        return value

    def unlink(self, cursor, user, ids, context=None):
        """Delete report and unregister it"""
        trans_obj = self.pool.get('ir.translation')
        trans_ids = trans_obj.search(
            cursor,
            user,
            [('type', '=', 'report'), ('res_id', 'in', ids)]
        )
        trans_obj.unlink(cursor, user, trans_ids)

        # Warning: we cannot unregister the services at the moment
        # because they are shared across databases. Calling a deleted
        # report will fail so it's ok.

        res = super(ReportBIRT, self).unlink(
                                            cursor,
                                            user,
                                            ids,
                                            context
                                        )
        return res

    def create(self, cursor, user, vals, context=None):
        "Create report and register it"
        res = super(ReportBIRT, self).create(cursor, user, vals, context)
        if vals.get('report_type','') == 'birt':
            # I really look forward to virtual functions :S
            register_report(
                        vals['report_name'],
                        vals['model'],
                        vals.get('report_rml', False)
                        )
        return res

    def write(self, cr, uid, ids, vals, context=None):
        "Edit report and manage it registration"
        if isinstance(ids, (int, long)):
            ids = [ids,]
        for rep in self.browse(cr, uid, ids, context=context):
            if rep.report_type != 'birt':
                continue
            if vals.get('report_name', False) and \
                vals['report_name'] != rep.report_name:
                report_name = vals['report_name']
            else:
                report_name = rep.report_name

            register_report(
                        report_name,
                        vals.get('model', rep.model),
                        vals.get('report_rml', rep.report_rml)
                        )
        res = super(ReportBIRT, self).write(cr, uid, ids, vals, context)
        return res

    _name = 'ir.actions.report.xml'
    _inherit = 'ir.actions.report.xml'
    _columns = {
        'birt_url': fields.char('BIRT Viewer URL', size=256, required=False),
        'birt_report': fields.char('Report file', size=64,),
        'birt_format': fields.char('Output format', size=32),
        'birt_report_params' : fields.one2many('report_birt.parameter', 'parent_id', 'BIRT report params',
                                               help="BIRT report params"),
    }

    _defaults = {
    }

ReportBIRT()
