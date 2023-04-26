from bs4 import BeautifulSoup, NavigableString
import logging
from lxml import etree
from .htmllabel import HtmlLabels


class Parser(HtmlLabels):
    def __init__(self, base_url, a_attr="href", img_attr="src", video_attr="src"):
        super().__init__(base_url, a_attr=a_attr, img_attr=img_attr, video_attr=video_attr)
        self.data = []

    def deep_parser(self, xpath_css, group_str):
        for each_xpath, each_css in xpath_css[0].items():
            deeper_tag = etree.HTML(group_str)
            inner_tag = deeper_tag.xpath(each_xpath)
            if inner_tag:
                self.parser(group_str, each_css, xpath_css={})
                xpath_css.pop(0)
                break

    def parser(self, html, css_selector, xpath_css=None):
        if xpath_css is None:
            xpath_css = []
        tag_groups = self.generate_groups(html, css_selector)
        if not tag_groups:
            return []
        # 循环处理新闻详情页面的html节点数据
        for index, group in enumerate(tag_groups):
            content_dict = {}
            content = group.text
            content_dict['type'] = group.name
            if isinstance(content, list):
                content_dict['context'] = ', '.join(content)
            else:
                content_dict['context'] = content
            content_dict['link'] = []
            group_str = str(group)
            if xpath_css:
                self.deep_parser(xpath_css, group_str)

            logging.info(f"current content dict: {content_dict}")
            tag_type_list = self.get_tag_type(group_str)

            if "tag_img" in tag_type_list:
                link_data = self.exist_img_label(group_str)
                content_dict['link'].append(link_data)
            if "tag_video" in tag_type_list:
                link_data = self.exist_video_label(group_str)
                content_dict['link'].append(link_data)
            if "tag_table" in tag_type_list:
                table_data = self.exist_table_label(group_str)
                content_dict = table_data
            elif group.name == "ul" or "tag_ul" in tag_type_list:
                li_data = self.exist_ul_label(group_str)
                content_dict.update({"context": li_data})
            else:
                if "tag_a" in tag_type_list:
                    link_data = self.exist_a_label(group_str, content_dict['context'])
                    content_dict['link'].extend(link_data)
            if content_dict.get("type") == "p" and content_dict.get("context") == "" and content_dict.get("link"):
                continue
            self.data.append(content_dict)
        return self.data

    def generate_groups(self, html, css_selector):
        """
        获取新闻详情的文本信息，并通过beautifulsoup对html节点数据进行过滤
        url:            新闻详情url
        css_selector:   新闻详情页面要处理的文本数据的 路径
        return:         新闻详情请求对象、过滤完的新闻详情页面html数据
        """
        selector = BeautifulSoup(html, "lxml")
        children = selector.select(css_selector)
        groups = []
        if children:
            for each_children in children:
                for child in each_children.contents:
                    if isinstance(child, NavigableString):
                        continue
                    groups.append(child)
        return groups


