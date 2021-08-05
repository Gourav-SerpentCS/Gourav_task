from odoo import _, api,fields,models
from odoo.osv import expression
from odoo.exceptions import UserError
from lxml import etree
import re

class AttendesName(models.Model):
    _name = 'attendees.data'
    _description = 'Attendees Details'
    _rec_name='partner_id'

    partner_id = fields.Many2one('res.partner',string='Attendee name ')


    def course_detail(self):
        context = dict(self._context)
        if context.get('open_action') == "course":
            return {
            "type": "ir.actions.act_window",
            "res_model": "courses.detail",
            "views": [[False, "form"]],
            "target": "new",
            }
        elif context.get('open_action') == "room":
            return{
            "type": "ir.actions.act_window",
            "res_model": "room.detail",
            "views": [[False, "tree"], [False, "form"]],
            "target": "new",
            }



        elif context.get('print_report') == "print":
            
            course = self.env['courses.detail'].search([])
            print(":::::::course", course)
            partner= course.mapped('attendees_ids')
            print(":::::partner", partner)
            partners= partner.mapped("partner_id")
            print(":::::::::partners",partners)
            # courses= self.env['courses.detail'].search([("attendees_ids.partner_id",'=',self.partner_id.id)])
            # print(":::::::::::courses", courses)

            attendee=[]
            for rec in course:
                if rec.mapped('attendees_ids').partner_id == self.id:
                    attendee.append(rec.attendees_ids.partner_id)

                   
            return self.env.ref('task_26_july.action_report_course_details').report_action(attendee)
           
            # self.ensure_one()
            # [data] = self.read()
            # data['course'] = self.env.context.get('active_ids', [])
            # course = self.env['courses.detail'].search([])
            # datas = {
            #     'ids': [],
            #     'model': 'course.data',
            #     'form': data
            # }
            # return self.env.ref('task_26_july.action_report_course_details').report_action(attendee)

            


class CourseData(models.Model):
    _name = 'courses.detail'
    _description = 'Course details'
    _rec_name = 'course'

    course= fields.Char(string='Course name')
    instructor_ids = fields.Many2many('res.partner','course_instructor_details_1','courses_ids1','instructor_ids1',string='Instructor')
    room_id = fields.Many2one('room.detail', string='Room')
    attendees_ids = fields.Many2many("attendees.data", string='Attendees Name')
    state = fields.Selection([('new','New'),('confirm','Confirm'),('cancel','Cancel')],default='new')
    
    def action_confirm(self):
        self.write({'state':'confirm'})

    def action_cancel(self):
        self.write({'state':'cancel'})

    

    @api.model
    def create(self, vals):
        res = super(CourseData, self).create(vals)
        # print(':::::::::Res', res)
        course_ids = res.instructor_ids.course_ids.ids or []
        course_ids.append(res.id)
        # print(':::::::::::course_ids', course_ids)
        res.instructor_ids.write({'course_ids' : course_ids})
        res.instructor_ids.write({'instructor': True})
        return res


    # def write(self,vals): 
    #     if vals.get('course') != self.course:
    #         for instructor in self.instructor_ids:
    #             self.instructor_ids.instructor = False
    #         rec= super(CourseData, self).write(vals)
    #         if self.instructor_ids.instructor:
    #             raise UserError("Already checked")
    #         else:
    #             self.instructor_ids.instructor = True
    #         return rec


    
    # def write(self,vals):
    #     value= vals.get('course')
    #     if value != self.course:
    #         self.instructor_ids.write({"instructor": False})
    #     rec = super(CourseData, self).write(vals)
    #     if self.instructor_ids.instructor:
    #         raise UserError('Already checked')
    #     else:
    #         print(":::::::::::::self.instructor_id.instructor", self.instructor_ids.instructor)
    #         # self.instructor_id.write({'instructor': True})
    #         self.instructor_ids.instructor = True
    #         return rec


    # def write(self,vals):
    #     self.instructor_id.write({"instructor":False})
    #     vals
    #     print(':::::::::::::vals', vals)
    #     rec = self.env['res.partner'].browse([vals.get('instructor_id')])
    #     if rec.instructor:
    #         raise UserError('Already checked')
    #     else:
    #         rec.write({'instructor': True})
    #         return rec


    def unlink(self):
        if self.state == "confirm":
            raise UserError("Cannot delete the record")
        return super(CourseData, self).unlink()


    @api.constrains("room_id",'attendees_ids')
    def _check_room_id(self):
        if self.room_id.capacity < len(self.attendees_ids):
            raise UserError("out of capacity")


    
    # @api.constrains("instructor_ids",'attendees_ids')
    # def _check_instructor_id(self):
    #     for rec in self.instructor_ids:
    #         for res in self.attendees_ids:
    #             if rec == res.partner_id:
    #                 raise UserError("instructor and attendees cannot be same")

    # @api.constrains("instructor_ids",'attendees_ids')
    # def _check_instructor_id(self):
    #     instructor = self.instructor_ids.ids
    #     attendees = self.attendees_ids.partner_id.ids
    #     instructor.extend(attendees)
    #     if len(instructor) > len(set(instructor)):
    #         raise UserError("instructor and attendees cannot be same")

    @api.constrains("instructor_ids",'attendees_ids')
    def _check_instructor_id(self):
        instructor = self.instructor_ids.ids
        attendees = self.attendees_ids.partner_id.ids
        common = set(instructor).intersection(attendees)
        print(":::::::::::common",set(instructor),set(instructor).intersection(attendees) )
        if common:
            raise UserError("instructor and attendees cannot be same")
                


    # def write(self,vals):
    #     print(":::::::::self.instructor_ids", self.instructor_ids,self.instructor_ids.ids, type(self.instructor_ids.ids))
    #     print('::::::::::;;attendees ids',self.attendees_ids.partner_id, self.attendees_ids.partner_id.ids, type(self.attendees_ids.partner_id.ids))
    #     return super(CourseData, self).write(vals)



class ResPartner(models.Model):
    _inherit = "res.partner"
    _rec_name= 'course_ids'

    instructor = fields.Boolean('Instructor')
    course_ids= fields.Many2many('courses.detail','course_instructor_details_1','instructor_ids1','courses_ids1', readonly= True, string='Courses')

    # def write(self,vals):
    #     rec= self.env['courses.detail'].search([('instructor_id','=',self.id)])
    #     print(':::::::::::rec', rec)
    #     vals.update({'course_ids':rec})
    #     return super(ResPartner, self).write(vals)
