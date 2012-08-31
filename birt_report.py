# -*- coding: utf-8 -*-

import logging
import traceback

import netsvc
import pooler

import report_webkit

from report.report_sxw import *
from tools.translate import _
from osv.osv import except_osv
from osv.orm import except_orm

from tools.safe_eval import safe_eval as eval

from . import birt

##
##

## XXXvlab: Translation ?

def format_last_exception():
    """Format the last exception for display it in tests."""

    return '\n'.join(
        ["  | " + line for line in traceback.format_exc().strip().split('\n')]
    )


class BirtProxyFactory(report_webkit.webkit_report.WebKitParser):
    """Proxies the BIRT client viewer web service
       Code partially taken from report webkit. Thanks guys :)
    """

    def __init__(self, name, table, rml=False, parser=False,
                 header=True, store=False):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.parser_instance = False
        self.localcontext = {}
        super(BirtProxyFactory, self).__init__(name, table, rml,
                                        parser, header, store)

    def generate_pdf(self, comm_path, report_birt, header, footer, html_list):
        ## should return the raw data of a pdf
        return None

    def _create_birt_report(self, cr, uid, ids, data, report_birt, context=None):
        if len(ids) != 1:
            raise NotImplementedError("Report on multiple object not implemented")
        table_obj = pooler.get_pool(cr.dbname).get(self.table)

        objs = table_obj.browse(cr, uid, ids, list_class=None, context=context, fields_process=None)
        obj = objs[0]
        fields_def = obj._table.fields_get(cr, uid, None, context)

        report_file = report_birt.birt_report
        format = report_birt.birt_format

        local = dict((k, getattr(obj, k)) for k, v in fields_def.iteritems())

        params = dict((o['identifier'],
                       o['value'] if o['is_literal'] else
                         eval(o['value'], globals(), local))
                      for o in report_birt.birt_report_params)
 
        birt_factory = birt.BirtConnection(report_birt.birt_url)

        return birt_factory(report_file, format, params)

    # override needed to keep the attachments' storing procedure
    def create_single_pdf(self, cr, uid, ids, data, report_birt, context=None):
        """Override of inherited function to divert it and generate the BIRT output
        instead of PDF if report_type is 'birt'."""

        if context is None:
            context={}

        if report_birt.report_type != 'birt':
            return super(XmlParser,self).create_single_pdf(cr, uid, ids, data, report_birt, context=context)

        return self.create_single_birt(cr, uid, ids, data, report_birt, context)

    def create_single_birt(self, cr, uid, ids, data, report_birt, context=None):
        """generate the BIRT report"""

        if context is None:
            context={}

        if report_birt.report_type != 'birt':
            return super(BirtProxyFactory,self).create_single_pdf(
                cr, uid, ids, data, report_birt, context=context)

        return self._create_birt_report(cr, uid, ids, data, report_birt, context)

    def create(self, cr, uid, ids, data, context=None):
        """We override the create function in order to handle generator
           Code taken from report webkit. Thanks guys :) """

        pool = pooler.get_pool(cr.dbname)
        ir_obj = pool.get('ir.actions.report.xml')
        report_xml_ids = ir_obj.search(cr, uid,
                [('report_name', '=', self.name[7:])], context=context)

        if report_xml_ids:
            report_xml = ir_obj.browse(
                                        cr,
                                        uid,
                                        report_xml_ids[0],
                                        context=context
                                    )
            report_xml.report_rml = None
            report_xml.report_rml_content = None
            report_xml.report_sxw_content_data = None
            report_rml.report_sxw_content = None
            report_rml.report_sxw = None
        else:
            return super(BirtProxyFactory, self).create(cr, uid, ids, data, context)
        if report_xml.report_type != 'birt' :
            return super(BirtProxyFactory, self).create(cr, uid, ids, data, context)
        result = self.create_source_pdf(cr, uid, ids, data, report_xml, context)
        if not result:
            return (False,False)
        return result
