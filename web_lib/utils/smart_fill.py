# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 10:38'


from utils.LogManager import log as logging
from settings import PARAMETER_NAME_KNOWLEDGE


def smart_fill(variable_name):

    variable_name = variable_name.lower()

    for filled_value, variable_name_list in PARAMETER_NAME_KNOWLEDGE.items():
        if variable_name in variable_name_list:
            return filled_value

    msg = '[smart_fill] Failed to find a value for parameter with name "' + variable_name + '".'
    logging.debug(msg)

    return 'UNKNOWN'


if __name__=="__main__":
    print(smart_fill("username"))
    print(smart_fill("password"))
    print(smart_fill("domain"))
    print(smart_fill("email"))
    print(smart_fill("content"))