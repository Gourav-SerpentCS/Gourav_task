from odoo import _,api,fields, models

class CourseData(models.TransientModel):
    _name = 'course.data'
    _description= "Course data"

    room = fields.Char('Room details')
    session = fields.Char('Session')
    
    def course_details(self):
        print("::::::::")

          


    
