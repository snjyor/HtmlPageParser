import logging
import re
import unicodedata

from bs4 import BeautifulSoup, NavigableString
from lxml import etree


class HtmlLabels:
    def __init__(self, base_url, a_attr="href", img_attr="src", video_attr="src"):
        self.base_url = base_url
        self.a_attr = a_attr
        self.img_attr = img_attr
        self.video_attr = video_attr

    def exist_img_label(self, group_str):
        """
        判断group_str中是否有image标签, 有则将image上传至blob
        group_str:      html节点数据
        return:         image信息字典
        """
        logging.info(f"Here if exist img label function")
        img_selector = etree.HTML(group_str)
        img_srcs = img_selector.xpath(f".//img/@{self.img_attr}")
        link_data = {}
        for src in img_srcs:
            src = src if src.startswith("http") else self.base_url + src
            link_data['origin_url'] = src
        return link_data

    def exist_video_label(self, group_str):
        """
        判断group_str中是否有video标签, 有则将video上传至blob
        group_str: html节点数据
        return:  video信息字典
        """
        video_selector = etree.HTML(group_str)
        video_srcs = video_selector.xpath(f".//video/source/@{self.video_attr}")
        link_data = {}
        for src in video_srcs:
            src = src if src.startswith("http") else self.base_url + src
            link_data['origin_url'] = src
        return link_data

    def exist_ul_label(self, group_str):
        logging.info(f"Here if exist ul label function")
        selector = BeautifulSoup(group_str, "lxml")
        li_children = selector.find_all("li")
        li_data = []
        for group in li_children:
            li_dict = {}
            str_list = []
            for string in group.stripped_strings:
                str_list.append(string)
            li_dict['type'] = "li"
            li_dict['context'] = ' '.join(str_list)
            link_data = self.exist_a_label(str(group), li_dict['context'])
            li_dict['link'] = link_data
            li_data.append(li_dict)
        return li_data

    def exist_a_label(self, group_str, content_str):
        """
        : 路径和链接的映射
        group_str: 单行的标签数据
        content_str: 该标签下面的文本数据
        """
        logging.info(f"Here if exist a label function")
        content_str = self.replace_everything(content_str)
        a_re = re.compile("<a [\s|\S]*?\/a>")
        a_tags = a_re.findall(group_str)
        text_list, hrefs = [], []
        for a_tag in a_tags:
            a_selector = etree.HTML(a_tag)
            href = a_selector.xpath(f"body/a/@{self.a_attr}")
            if href and href[0].startswith("#"):
                href = []
            text = a_selector.xpath("body/a//text()")
            text = self.replace_everything("".join(text))
            hrefs.extend(href)
            text_list.append(text)
        link_list = []
        if hrefs:
            for index, each_text in enumerate(text_list):
                url_start = content_str.find(''.join(each_text).replace("\n", "").strip())
                if url_start == -1:
                    url_start = 0
                url_end = url_start + len(''.join(each_text))
                try:
                    email_re = re.compile("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
                    email_str = email_re.findall(hrefs[index])
                    detail_href = hrefs[index]
                    if email_str:
                        sas_path = detail_href if detail_href.startswith("mailto:") else "mailto:" + detail_href
                        href = sas_path
                    else:
                        href = self.base_url + detail_href if not detail_href.startswith("http") else detail_href
                        print(href)
                except Exception as err:
                    logging.info(f"href not enough! detail: {err}")
                    sas_path = ''
                    href = ''
                link_data = {}
                link_data['start'] = url_start
                link_data['end'] = url_end
                link_data['origin_url'] = href.split(";")[0]
                link_list.append(link_data)
                logging.info(f"current link data: {link_data}")
        return link_list

    def exist_table_label(self, group_str):
        """
        : 路径和链接的映射
        group_str: 单行的标签数据
        """
        selector = BeautifulSoup(group_str, "lxml")
        table_list = selector.select("body>table")
        element_dict = {}
        for table_element in table_list:
            element_dict = {
                "type": table_element.name,
                "link": []
            }
            tr_element_list = table_element.find_all("tr")
            tr_list = []
            for tr_element in tr_element_list:
                tr_dict = {
                    "type": tr_element.name,
                    "link": []
                }
                child_list = []
                for child_element in tr_element.contents:
                    if isinstance(child_element, NavigableString):
                        continue
                    # colspan,rowspan
                    td_res = {"attribution": {}}
                    if 'colspan' in child_element.attrs.keys():
                        td_res["attribution"]["colspan"] = "".join(child_element.attrs['colspan'])
                    if 'rowspan' in child_element.attrs.keys():
                        td_res["attribution"]["rowspan"] = "".join(child_element.attrs['rowspan'])

                    # 正常数据
                    content_str = ''.join(child_element.strings)
                    temp = {
                        "type": child_element.name,
                        "context": content_str,
                        "link": []
                    }
                    if child_element.find_all("a"):
                        temp.update({"link": self.exist_a_label(group_str=str(child_element), content_str=content_str)})

                    if td_res["attribution"]:
                        td_res.update(temp)
                    else:
                        td_res = temp
                    child_list.append(td_res)
                tr_dict["context"] = child_list
                tr_list.append(tr_dict)
            element_dict["context"] = tr_list
        return element_dict

    def get_tag_type(self, tag_str):
        flag_list = []
        img_re = re.compile("<img.*?>")
        hasimg = re.findall(img_re, tag_str)
        if hasimg:
            flag_list.append("tag_img")
        table_re = re.compile("<table ")
        hastable = re.findall(table_re, tag_str)
        if hastable:
            flag_list.append("tag_table")
        ul_re = re.compile("<ul>[\s|\S]*?<\/ul>")
        hasul = re.findall(ul_re, tag_str)
        if hasul:
            flag_list.append("tag_ul")
        a_re = re.compile("<a [\s|\S]*?\/a>")
        hasa = re.findall(a_re, tag_str)
        if hasa:
            flag_list.append("tag_a")
        video_re = re.compile("<video [\s|\S]*?\/video>")
        hasvideo = re.findall(video_re, tag_str)
        if hasvideo:
            flag_list.append("tag_video")
        return flag_list

    def parse_context(self, context, dict_key="context"):
        for con in context:
            text = con.get(dict_key)
            if isinstance(text, list):
                self.parse_context(text)
            else:
                if text:
                    con[dict_key] = self.replace_everything(text)

    def complete_url(self, url, base_url=""):
        """
        url: 爬取到的部分url地址
        base_url: 当前网站的域名
        当拿到的href是邮箱的时候加上mailto: 正常网址链接时加上域名
        """
        email_re = re.compile("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
        email_str = email_re.findall(url)
        if email_str:
            url = url if url.startswith("mailto:") else "mailto:" + url
        else:
            url = url if url.startswith("http") else base_url + url
        return url
    
    def replace_everything(self, content):
        content = unicodedata.normalize("NFKC", content)
        to_blank = ['""', '\r', '\t', ' ', '\\n']
        for replace in to_blank:
            content = content.replace(replace, "")
        to_dollar = ["'", "`", "’", '”', '“', '"', "\'"]
        for replace in to_dollar:
            content = content.replace(replace, "^")
        to_space = ["\\xa0", " ", '\n', r'\xa0', " "]
        for replace in to_space:
            content = content.replace(replace, " ")

        return content.strip()

