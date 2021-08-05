from odoo import _,api,fields, models
from odoo.osv import expression
from odoo.exceptions import UserError
from lxml import etree

class LibraryData(models.TransientModel):
    _name = 'library.books.data'
    _description= "Library Books Data"

    book_id = fields.Many2one('books.detail', string='Book Name')
    partner_id= fields.Many2one("res.partner",string="Student Name")
    date = fields.Date('Date', default=fields.Date.today)

    def book_issue_detail(self):
        data = dict(self._context)
        print(":::::::::::::::data", data)
        print("::::::::::selfbook id",self.book_id)
        rec= self.env['books.detail'].search([('book',"=",self.book_id.book)])
        print(":::::::::::;rec", rec)
        if data.get('issue_button') == "issue date":
            rec.write({"book_history_ids":[(0, 0, {"book_id":self.book_id.id, "partner_id":self.partner_id.id, "issue_on":self.date })]})
        
        elif data.get("return_button") == 'return date':
            res= self.env['book.history'].search(['&',('book_id','=',self.book_id.id),('partner_id','=',self.partner_id.id)])
            print(":::::::::::res", res)
            res.write({"return_date":self.date})
            
            

# another method by new wizard 
    # def book_return_detail(self):
    #     res= self.env['books.detail'].search([('book',"=",self.book_id.book)])
    #     print(":::::::::::::res", res)
    #     rep= res.book_history_ids.search(['&',('partner_id','=',self.partner_id.id), ('book_id',"=",self.book_id.id)])
    #     print(":::::::::::rep", rep)
    #     res.write({'book_history_ids': [(1,rep.id, {"return_date":self.date})]})

    