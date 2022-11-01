# -*- coding:utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class HrLeaveTypes(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.leave.type'
    _description = 'Employee Contract'

    leave_validation_type = fields.Selection(
        selection_add=[('multi', 'Multi Level Approval')])


class HrLeave(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.leave'
    _description = 'Employee Contract'

    state = fields.Selection(selection_add=[('first', 'First Approval'), ('draft',)], default='first')
    reason = fields.Char(string="Reason:")

    def notifyme(self):
        if not self.reason:
            self.action_refuse()
        else:
            raise UserError("Reasons For Rejecting can`t be Empty")

    @api.model
    def create(self, vals):
        if vals:
            vals['state'] = "first"
        result = super().create(vals)
        for res in result:
            res.notify_first_approver()
        return result

    def notify_first_approver(self):
        approver_group = self.env.ref('general_approvers.first_level_approver')
        users = approver_group.users
        for res in users:
            if res:
                mail_obj = self.env['mail.mail']
                state = dict(self._fields['state'].selection).get(self.state)
                subject = f"Time Off APproval Request for {self.employee_id.name}"
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
                email_to = res.login
                body_html = f"""
                    <html>
                    <body>
                    <div style="margin:0px;padding: 0px;">
                        <p style="padding: 0px; font-size: 13px;">
                            Dear {res.name},
                            <br/>
                            You Have Been Requested to accept the Time Off.
                            <br/>
                            .
                            </p>
                            <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web?#cids=1&menu_id=571&model=hr.leave&view_type=form&id={self.id}" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Accept Time Off
            </a>
                    <br/>
                    </div>
                    </body>
                    </html>
                """
                mail = mail_obj.sudo().create({
                    'body_html': body_html,
                    'subject': subject,
                    'email_to': email_to
                })
                mail.send()

    def need_second_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.notify_second_approver()
            return self.write({'state': "draft"})

    def notify_second_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        approver_group = self.env.ref('general_approvers.second_level_approver')
        users = approver_group.users
        for res in users:
            mail_obj = self.env['mail.mail']
            state = dict(self._fields['state'].selection).get(self.state)
            subject = f"Time Off Request For {self.employee_id.name}"
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
            email_to = res.login
            body_html = f"""
                <html>
                <body>
                <div style="margin:0px;padding: 0px;">
                    <p style="padding: 0px; font-size: 13px;">
                        Dear {res.name},
                        <br/>
                        You Have Been Requested to Confirm Time Off for {self.employee_id.name}.
                        <br/>
                        .
                        <br/>
                    </p>
                    <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web?#cids=1&menu_id=571&model=hr.leave&view_type=form&id={self.id}" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Confirm Time Off
            </a>
        </p>
                <br/>
                </div>
                </body>
                </html>
            """
            mail = mail_obj.sudo().create({
                'body_html': body_html,
                'subject': subject,
                'email_to': email_to
            })
            mail.send()
            return mail

    def need_third_approver(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.action_confirm()
            self.notify_third_approver()

    def notify_third_approver(self):
        approver_group = self.env.ref('general_approvers.third_level_approver')
        users = approver_group.users
        for res in users:
            mail_obj = self.env['mail.mail']
            state = dict(self._fields['state'].selection).get(self.state)
            subject = f"Time Off Request For {self.employee_id.name}"
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
            email_to = res.login
            body_html = f"""
                <html>
                <body>
                <div style="margin:0px;padding: 0px;">
                    <p style="padding: 0px; font-size: 13px;">
                        Dear {res.name},
                        <br/>
                        You Have Been Requested to Approve Time Off for {self.employee_id.name}.
                        <br/>
                        .
                        <br/>
                    </p>
                    <p style="margin:16px 0px 16px 0px;">
            <a href="{base_url}/web?#cids=1&menu_id=571&model=hr.leave&view_type=form&id={self.id}" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
            Approve Time Off
            </a>
        </p>
                <br/>
                </div>
                </body>
                </html>
            """
            mail = mail_obj.sudo().create({
                'body_html': body_html,
                'subject': subject,
                'email_to': email_to
            })
            mail.send()
            return mail

    def need_owner(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            self.action_approve()
            self.notify_owner()
        else:
            raise UserError("Your Dont Have Enough permissions")

    def notify_owner(self):
        mail_obj = self.env['mail.mail']
        subject = f"Time Off Accepted"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.private.url')
        email_to = self.employee_id.work_email
        body_html = f"""
            <html>
            <body>
            <div style="margin:0px;padding: 0px;">
                <p style="padding: 0px; font-size: 13px;">
                    Dear {self.employee_id.work_email},
                    <br/>
                    Your Time Of Has Been Approved!.
                    <br/>
                    .
                    <br/>
                </p>
                <p style="margin:16px 0px 16px 0px;">
        <a href="{base_url}/web?#cids=1&menu_id=571&model=hr.leave&view_type=form&id={self.id}" target="_blank" style="background-color:#875A7B;padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px;">
        View Time Off
        </a>
    </p>
            <br/>
            </div>
            </body>
            </html>
        """
        mail = mail_obj.sudo().create({
            'body_html': body_html,
            'subject': subject,
            'email_to': email_to
        })
        mail.send()
        return mail


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_leave_state = fields.Selection(selection_add=[('first', 'First Approval'), ('draft',)], default='first')
