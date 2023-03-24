# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import re

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'telegraf_checksum': self.checksum,
            'telegraf_input_value': self.input_value,
            'telegraf_clean_list': self.telegraf_clean_list,
        }

    def checksum(self, data, os, arch):
        """
        """
        # display.v(f"checksum(self, data, {os}, {arch})")

        checksum = None

        if isinstance(data, list):
            # filter OS and ARCH
            checksum = [x for x in data if re.search(fr".*telegraf-.*.{os}-{arch}.tar.gz", x)][0]

        if isinstance(checksum, str):
            checksum = checksum.split(" ")[0]

        # display.v(f"= checksum: {checksum}")

        return checksum

    def input_value(self, var):
        """
        """
        # display.v(f"input_value(self, {var} ({type(var)}))")

        result = False
        result_value = var

        if isinstance(var, int) and int(var) > 0:
            result = True
        if isinstance(var, bool):
            result = True
            if var:
                result_value = "true"
            else:
                result_value = "false"
        if (isinstance(var, str) or type(var).__name__ == "AnsibleUnsafeText"):
            if var.lower() == "true" or var.lower() == "false":
                result_value = var.lower()
            else:
                result_value = '"{}"'.format(str(var))
            if len(var) > 0:
                result = True
        if isinstance(var, list) and len(var) > 0:
            _list = '","'.join(var)
            result_value = f'["{_list}"]'
            result = True

        # display.v(f"= result: {result}, {result_value}")

        return result, result_value

    def telegraf_clean_list(self, data):
        """
        """
        result = []

        if isinstance(data, list) and len(data) > 0:
            for e in data:
                # _type = e.get('type')
                _config = e.get('config', None)

                if not _config:
                    # display.v(f"{_type} has no config .. skip")
                    continue
                else:
                    result.append(e)

        # display.v(f"= result: {result}")

        return result
