===========
Report Birt
===========

This is a BIRT Report module for OpenERP. It's a very early alpha.

Fairly simple and small, It covers:

  - connection to birt-viewer web server to request reports

  - configurable URL parameters

So you can easily use BIRT as report engine in OpenERP.


Acknowledgements
----------------

Many thanks to `CARIF-OREF La Réunion`_ which has funded the near entirety of
the developpement of this code.

.. _CARIF-OREF La Réunion: http://www.cariforef-reunion.net/


Requirements
------------

Was tested successfully with:

 - OpenERP 6.0.3
 - OpenERP 6.1
 - OpenERP 7.0

``report_birt`` needs the python ``requests`` module (`Requests: HTTP for Humans`_)
to be installed. You could install it with::

  pip install requests

.. _requests\: http for humans: http://docs.python-requests.org/en/latest/index.html

Then, you'll need a running instance of ``birt-viewer`` of course.

You can download it here:

  http://download.eclipse.org/birt/downloads/

You are looking for the ``birt-runtime`` which contains a ``birt-viewer.war``
that you can install on a running tomcat server as a webapp.

Then you'll need a report from BIRT. This report should use some URL
parameters, these will be fed by OpenERP.


Installation
------------

Don't forget to run the ``./autogen.sh`` to set the module version and compute
the Changelog.

Install as any OpenERP module.


Usage
-----

1. Ensure that you are are an OpenERP administrator with Extended Interface.
2. Then go to the "Settings" Tab,
3. And in the left menu, follow Customization / Low Level Objects / Actions / Reports
4. You can create a new report, in the ``Report Type`` input write the string ``birt``,
   then quit this field. A new tab named ``Birt`` should appear.

   A common configuration could be::

     Birt Url: http://127.0.0.1:8080/birt-viewer
     Report file: myreport.rptdesign
     Output format: pdf

   Then in the parameters, you could send parameters which would be evaled by
   OpenERP python.

