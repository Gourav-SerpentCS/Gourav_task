# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
  'name':'Course',
  'version':'3.0',
  'category':"Course management",
  'sequence': 360,
  'summary':'Track course data',
  'author': 'Gourav yadav',
  'description':"""Helps to track course data , instructor data, details of room in which event will happen,""",
  'depends':['base','web'],
  'data':["security/ir.model.access.csv",
          "wizard/wizard_view_course_detail.xml",
          "wizard/wizard_library_view.xml",
          "views/course_detail_view.xml",
          "views/rooms_detail_view.xml",
          "views/books_library_view.xml",
          "report/course_detail.xml",
          "report/course_detail_template.xml"
          ],
  'installable': True,
  'auto_install': False,
  'application': True,
}