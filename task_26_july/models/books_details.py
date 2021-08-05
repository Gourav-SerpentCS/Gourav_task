from odoo import _, api,fields, models
from odoo.osv import expression

class BooksDetail(models.Model):
    _name = 'books.detail'
    _description = 'Book details'
    _rec_name= 'book'

    book = fields.Char('Book Name')
    library_id = fields.Many2one("library.data", string='Library detail')
    book_history_ids =fields.One2many("book.history",'book_id',string="Book history")



class LibraryData(models.Model):
    _name='library.data'
    _description= 'Books Data'
    _rec_name='library_name'

    library_name =fields.Char("Name")
    books_data_ids = fields.One2many('books.detail', 'library_id', string='Library data', store=True)



class BookHistory(models.Model):
    _name='book.history'
    _description='Book History'
    _rec_name='partner_id'

    partner_id= fields.Many2one("res.partner",string="Student Name")
    issue_on = fields.Date('Issue Date')
    return_date= fields.Date('Return Date')
    book_id = fields.Many2one('books.detail', string='Book')
