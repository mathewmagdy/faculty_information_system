from odoo import api,fields, models,_
from odoo.exceptions import ValidationError
from datetime import date


class FacultyStudent(models.Model):
    _name="faculty.student"
    _description="student info"
    _inherit="mail.thread"
    
    id_student=fields.Char(string="National_ID",required=True,tracking=True)
    name=fields.Char(string="Name",required=True,tracking=True)
    date_of_birth=fields.Date(string="Date_Of_Birth")
    age=fields.Integer(string="Age",compute="Calculate_Age",store=True)
    year=fields.Selection([('first year','First year'),('second year','Second year'),('third year','Third year'),('forth year','Forth year')],string="Year")
    semester=fields.Selection([('first_semester','First semester'),('second_semester','Second semester')],string="Semester")
    gpa=fields.Float(string="GPA",required=True,tracking=True)
    semester_fees=fields.Float(string="Semester_Fees",compute="Calculate_fee",store=True)
    ref=fields.Char(string="Reference",default=lambda self:_('New Student'))
    department_id=fields.Many2one('faculty.department' ,string="Depatrment")
    subject_id=fields.Many2many('faculty.subject',string="Subject")
    state = fields.Selection([
        ('draft', 'Not Confirmed'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')], string='Status', readonly=True, default='draft', track_visibility='onchange')
    
    @api.onchange('state')
    def action_confirm(self):
        for student in self:
            self.write({'state': 'confirm'})
            
    @api.onchange('state')
    def action_cancel(self):
        for student in self:
            self.write({'state': 'cancel'})
            
    @api.onchange('state')
    def action_done(self):
        for student in self:
            self.write({'state': 'done'})
            
    @api.onchange('state')
    def action_reset(self):
        for student in self:
            self.write({'state': 'draft'})
    
    @api.depends('date_of_birth')
    def Calculate_Age(self):
        for rec in self:
            if rec.date_of_birth:
                today = fields.Date.today()
                age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                rec.age = age
            else:
                rec.age = 0
                
    @api.model_create_multi      
    def create(self,value_list):
        for val in value_list:
            val['ref'] = self.env['ir.sequence'].next_by_code('faculty.student')
        return super(FacultyStudent,self).create(value_list)
    
    @api.depends('gpa','semester')
    def Calculate_fee(self):
        h_cost=800
        for rec in self:
            if rec.semester=='first_semester' and rec.gpa>3:
                rec.semester_fees=(h_cost*20)-((h_cost*20)*(30/100))
            elif rec.semester=='first_semester' and rec.gpa<3:
                rec.semester_fees=h_cost*20
            elif rec.semester=='second_semester' and rec.gpa>3:
                rec.semester_fees=(h_cost*18)-((h_cost*18)*(30/100))
            elif rec.semester=='second_semester' and rec.gpa<3:
                rec.semester_fees=h_cost*18
    
    
    @api.onchange('year')
    def onchange_year(self):
        if self.year == 'first year':
            return {'domain': {'department_id': [('department_name', '=', 'General')]}}
        else:
            return {'domain': {'department_id': [('department_name', '!=', 'General')]}}
        

    @api.onchange('year', 'semester', 'department_id')
    def onchange_year_semester_department(self):
        if self.year and self.semester and self.department_id:
            try:
                domain = [
                    ('department_id', '=', self.department_id.id),  
                    ('semester', '=', self.semester),
                    ('year', '=', self.year)
                ]
                return {'domain': {'subject_id': domain}}
            except AttributeError as e:
                
                return {
                    'warning': {
                        'title': 'Error',
                        'message': f"AttributeError: {e}. Please check if 'department_id' is correctly set." 
                    },
                    'domain': {'subject_id': []} 
                }
        else:
            return {'domain': {'subject_id': []}}
          