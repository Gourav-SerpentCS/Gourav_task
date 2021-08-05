from odoo import _, api, models, fields
from odoo.osv import expression
from odoo.exceptions import UserError

class RoomDetail(models.Model):
    _name = 'room.detail'
    _description = 'Room details'
    _rec_name= 'location'


    location = fields.Char('Room')
    capacity = fields.Integer('Capacity', default=1)
    session = fields.Char('Session')
    room= fields.Boolean('Room Available', compute="_compute_room", readonly=False)  #to make a compute field editablegive attr redonly= False
    room_name= fields.Char('Room Name', compute="_compute_room_name",readonly= False,store=True) 
    

    
    @api.depends('location','session')
    def _compute_room(self):
        for rec in self:
            if rec.session and rec.location:
                rec.room = True
            else:
                rec.room = False

    @api.depends('location','capacity','session')
    def _compute_room_name(self):
        for rec in self:
            if rec.session and rec.location and rec.capacity:
                rec.room_name = 'Compute'
            else:
                rec.room_name = ' '


    # @api.model
    # def create(self, vals):
    #     print("::::::::::vals", vals)
    #     print(":::::::::::::SELf", self)
    #     rec = super(RoomDetail, self).create(vals)
    #     if vals.get("room_name") != rec.room_name:
    #         rec.write({'room_name':vals.get("room_name")})
    #     return rec

    # @api.model
    # def create(self, vals):
    #     print(":::::::vals", vals)
    #     rec= super(RoomDetail, self).create(vals)
    #     value= vals.get("room")
    #     if value != rec.room:
    #         rec.update({"room" :value })
    #     return rec

    # def write(self,vals):
    #     print("::::::::::vals", vals)
    #     rec= super(RoomDetail, self).write(vals)
    #     value= vals.get('room')
    #     if value != rec.room:
    #         rec.write({'room':value})
    #     return rec

    
   