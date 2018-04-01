# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/29 10:50'

from urllib.parse import parse_qs, urlencode


class Data(dict):
    # 传入一个http查询字符串，如a=1&b=2，返回一个字典
    def __init__(self,init_val=()):

        dict.__init__(self)
        if isinstance(init_val, Data):
            dict.update(self, init_val)
        elif isinstance(init_val, str):
            for k, v in parse_qs(init_val).items():
                self[k]=v[0]
        else:
            # [('id', 1), ('test', 2)]
            for item in init_val:
                try:
                    key, val = item
                except TypeError:
                    raise TypeError('key ,val= item')
                self[key] = val


class postData(Data):
    def __init__(self, init_val=()):

        Data.__init__(self, init_val)

        self._name = None
        self._method = None
        self._action = None
        self._files = None

    def get_action(self):
        return self._action

    def get_method(self):
        return self._method

    def set_method(self, method):
        self._method = method

    def set_name(self, name):
        self._name = name

    def set_action(self, action):
        self._action = action

    def set_file(self, files):
        self._files = files

    def set_data(self, key, value):
        self[key] = value

    def __str__(self):
        # 因为这个类继承的是一个字典，恰好urlencode传入的参数也是字典
        return urlencode(self)


if __name__ == "__main__":
    # a = Data("user=1&password=2")
    # b = Data([('id', 1), ('test', 2)])
    # print(a)
    # print(b)


    postdata = postData([('id', 1), ('test', "汉语")])
    postdata.h()