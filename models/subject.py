from odoo import api,fields, models,_
from odoo.exceptions import ValidationError

class FacultySubject(models.Model):
    _name="faculty.subject"
    _description="subject info"
    
    
    subject_name=fields.Char("subject name", required=True,tracking=True)
    ref=fields.Char(string="Subject_reference",default=lambda self:_('New subject'))
    department_id=fields.Many2one('faculty.department' ,string="Depatrment")
    year=fields.Selection([('first year','First year'),('second year','Second year'),('third year','Third year'),('forth year','Forth year')],string="Year")
    semester=fields.Selection([('first_semester','First semester'),('second_semester','Second semester')],string="Semester")
    
        # initiate reference sequense for subject
    @api.model_create_multi      
    def create(self,value_list):
        for val in value_list:
            val['ref'] = self.env['ir.sequence'].next_by_code('faculty.subject')
        return super(FacultySubject,self).create(value_list)
    
    