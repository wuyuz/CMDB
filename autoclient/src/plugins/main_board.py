#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from .base import BasePlugin
from libs.utils.response import BaseResponse


class MainBoard(BasePlugin):
    def win(self, handler, hostname=None):
        raise NotImplementedError('win must be implemented ')
    
    def linux(self, handler, hostname=None):
        response = BaseResponse()
        try:
            if self.debug:
                
                output = open(os.path.join(self.base_dir, 'files', 'board.out'), 'r').read()
            else:
                shell_command = "sudo dmidecode -t1"
                output = handler.cmd(shell_command, hostname)
            response.data = self.parse(output)
        except Exception as e:
            msg = traceback.format_exc()
            response.status = False
            response.error = msg

        return response.dict
    
    def parse(self, content):
        
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }
        
        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip()
        
        return result
