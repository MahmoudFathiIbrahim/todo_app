from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Record'

    state_selections = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]

    name = fields.Char(required=True)
    assign_to = fields.Many2one('res.partner')
    description = fields.Text()
    due_date = fields.Date()
    state = fields.Selection(state_selections, default='new')

    timesheet_line_ids = fields.One2many('timesheet.line', 'todo_task_id')
    estimated_time = fields.Float()
    active = fields.Boolean(default=True)
    is_late = fields.Boolean()

    @api.constrains('timesheet_line_ids')
    def _check_estimated_time(self):
        for rec in self:
            total_time = 0
            for line in rec.timesheet_line_ids:
                total_time += line.time
            if total_time > rec.estimated_time:
                raise ValidationError("Estimated Time is Over")

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_todo_task_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.state != 'completed' and rec.state != 'closed':
                if rec.due_date and rec.due_date < fields.date.today():
                    rec.is_late = True
                else:
                    rec.is_late = False
            

class TimesheetLine(models.Model):
    _name = 'timesheet.line'
    _description = 'TimesheetLines'

    description = fields.Text()
    date = fields.Date()
    time = fields.Float()

    todo_task_id = fields.Many2one('todo.task')


