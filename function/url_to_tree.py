# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/4/3 19:22'


class UrlTree():
    def __init__(self):
        self.root = {}
    def url_to_tree(self, url_str):
        url_list = url_str.strip('/').split("/")
        temp = self.root
        for i in url_list:
            if i not in temp.keys():
                temp[i] = {}
            temp = temp[i]
        temp[url_list[-1]] = "code:"+"200"

    def get_json(self):
        import json
        return json.dumps(self.root)


if __name__=="__main__":
    test = UrlTree()
    test.url_to_tree("/www/html/abc.php")
    test.url_to_tree("/www/html/test.php")
    test.url_to_tree("/abc/html/abc.php")
    test.url_to_tree("/ccc/html/abc.php")
    with open("1.json", 'w') as f:
        f.write(test.get_json())
    pass