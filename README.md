# HtmlPageParser
A generic HTML page parser

```
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()
    client = Parser(base_url="https://www.163.com/")
    xpath_css = [
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"},
        {".//p[@class='f_center']": ".f_center"}
    ]
    data = client.parser(html, css_selector="#content > div.post_body", xpath_css=xpath_css)
    print(data) 
```
