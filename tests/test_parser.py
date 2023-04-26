from src.parser import Parser

def test_parser():
    """
    使用test.html文件测试parser脚本的流程正确性与输出结果以供参考
    :return:
    """
    with open("../tests/test.html", "r", encoding="utf-8") as f:
        html = f.read()
    client = Parser(base_url="https://www.163.com/")
    xpath_css = [
        {".//p[@id='video']": "#video"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"}
    ]
    data = client.parser(html, css_selector="#content > div.post_body", xpath_css=xpath_css)
    print(data)


if __name__ == '__main__':
    test_parser()
