# -*- coding: utf-8 -*-

{
    "name": "BIRT Report Engine",
    "description" : """This module adds a new Report Engine which uses BIRT to create report
The module structure and some code is inspired by the report_webkit module.
""",
    "version": "%%short-version%%",
    "depends": [
        "base",
        "report_webkit",
    ],
    "author": "Valentin LAB",
    "category": "Reports/Xml",
    "url": "http://github.com/simplee/report_birt",
    "data": [ "security/ir.model.access.csv",
              "birt_report_parameter.xml",
              "ir_report_view.xml",
    ],
    "installable": True,
    "active": False,
}
