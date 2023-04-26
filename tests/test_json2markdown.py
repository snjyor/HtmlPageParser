import json

from src.json2markdown import Json2Markdown

def test_json2markdown():
    """
    使用json2markdown.json文件测试json2markdown脚本的流程正确性与输出结果以供参考
    :return:
    """
    with open("json_data.json", 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    J2M = Json2Markdown()
    markdown_data = J2M.json2markdown(json_data)
    print(markdown_data)


if __name__ == '__main__':
    test_json2markdown()
