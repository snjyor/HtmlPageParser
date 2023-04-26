import sys
import json


class Json2Markdown(object):
    def __init__(self):
        self.markdown = ""  # markdown文本
        self.tab = "  "  # 缩进
        self.list_tag = '* '  # 列表标签
        self.htag = '#'  # 标题标签
        self.tabletag = "|"  # 表格分隔符
        self.linktag = "[]"  # 链接标签
        self.imgtag = "!"  # 图片标签
        self.use_url = "origin_url"  # 使用的url字段

    def _json2markdown(self, json_data):
        """
        json转markdown
        :param json_data:
        :return:
        """
        for item_dict in json_data:
            if item_dict.get("type") == "p":
                self._p2markdown(item_dict)
            elif item_dict.get("type").startswith("h"):
                self._h2markdown(item_dict)
            elif item_dict.get("type") == "ul":
                self._ul2markdown(item_dict)
            elif item_dict.get("type") == "table":
                self._table2markdown(item_dict)
            elif item_dict.get("type") == "img":
                self._img2markdown(item_dict)
            else:
                # todo
                self._p2markdown(item_dict)

    def _str2markdown(self, item:dict):
        """
        字符串转markdown
        :param item:
        :return:
        """
        link_list = item.get("link")
        context = item.get("context")
        new_context = context
        if link_list:
            for link_dict in link_list:
                if link_dict.get("start") is None:
                    continue
                part_context = context[link_dict.get('start'):link_dict.get('end')]
                link_context = f"[{part_context}]({link_dict.get(self.use_url, '')})"
                new_context = new_context.replace(part_context, link_context)
        return new_context

    def _p2markdown(self, item: dict):
        """
        段落转markdown
        :param item:
        :return:
        """
        context = self._str2markdown(item)
        self.markdown += context + "\n\n"

    def _h2markdown(self, item: dict):
        """
        标题转markdown
        :param item:
        :return:
        """
        context = self._str2markdown(item)
        self.markdown += self.htag * int(item.get("type")[-1]) + context + "\n\n"

    def _ul2markdown(self, item: dict):
        """
        列表转markdown
        :param item:
        :return:
        """
        context_list = item.get("context")
        for li_dict in context_list:
            self.markdown += self.tab + self.list_tag + self._str2markdown(li_dict) + "\n"
        self.markdown += "\n"

    def _table2markdown(self, item: dict):
        """
        表格转markdown
        :param item:
        :return:
        """
        context_list = item.get("context")
        for tr_dict in context_list:
            one_row = ""
            for td_dict in tr_dict.get("context"):
                row = self.tabletag + self._str2markdown(td_dict)
                one_row += row
            one_row += self.tabletag + "\n"
            self.markdown += one_row
        self.markdown += "\n"

    def _img2markdown(self, item: dict):
        """
        图片转markdown
        :param item:
        :return:
        """
        link_list = item.get("link")
        if link_list:
            self.markdown += f"{self.imgtag}[{item.get('context')}]({link_list[0].get(self.use_url,'')})\n\n"

    def json2markdown(self, json_data):
        """
        json转markdown
        :param json_data: json数据
        :return: markdown文本
        """
        self._json2markdown(json_data)
        return self.markdown


