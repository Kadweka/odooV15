# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class OoDataUploads(http.Controller):
    @http.route('/user/mass/upload', auth='none', type='json', methods=['GET', 'POST'], cors='*', csrf=False)
    def invoice_controller(self, **kw):
        payload = kw.get('payload')
        departments_cache = {}
        roles_cache = {}

        departments = set([line['department'] for line in payload])
        roles = set([line['role'] for line in payload])

        for role in roles:
            res = request.env['hr.job'].with_user(2).create({'name': role, 'state': 'open'})
            roles_cache[role] = res.id

        for department in departments:
            res = request.env['hr.department'].with_user(2).create({'name': department})
            departments_cache[department] = res.id

        for line in payload:
            res = request.env['res.users'].with_user(2).create({
                'name': line['name'],
                'login': line['login']
            })
            request.env['hr.employee'].with_user(2).create({
                'name': line['name'],
                'user_id': res.id,
                'work_phone': False,
                'work_phone': line['login'],
                'department_id': departments_cache.get(line['department']),
                'job_title': line['role'],
                'job_id': roles_cache.get(line['role'])
            })
        return json.dumps({'message': 'Users created successfully'})
