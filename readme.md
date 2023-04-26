# HtmlPageParser
通用HTML页面内容解析器

## example
```python
from HtmlParser.parser import Parser
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


| 参数           |参数说明|
|:-------------|:---|
| base_url     |爬取页面的域名，如爬取的页面是https://www.163.com/dy/article/I35SM5AN0514EGPO.html，那base_url就是https://www.163.com/|
| html         |该页面的html元素，即requests.get()返回的response.text|
| css_selector |需要爬取的元素的上一级标签的css_selector,右键检查选中复制selector即可|
| xpath_css    |xpath和css的映射字典，如果需要爬取的页面内部还有需要继续深入爬取的标签，则需要配置需要深入爬取标签上一级的xpath和css的映射字典，具体示例如下|
| a_attr       |需要抓取a标签中的属性，默认为herf|
| img_attr     |需要抓取img标签中的属性，默认为src|
| video_attr   |需要抓取video标签中的属性，默认为src|


## 配置示例
如下述元素块，
例如我想要抓取div[class='post_body']下面的所有标签，那css_selector就是```<div class="post_body">```这个标签位置的css_selector; 如果只配置了上面的css_selector，那只能抓到```<div class="post_body">```标签下一层的标签内容，不能抓到该标签下一层标签里面的标签内容， 这个时候需要配置xpath_css参数，即如下所示，如果我想继续深入抓取```<p class="f_center">```标签下面的img标签，那我需要写```<p class="f_center">```这层标签的xpath和css字典，下述元素中有两个```<p class="f_center">```标签，所以需要按顺序写两个映射字典，格式如下：
```python
xpath_css = [
    {".//p[@class='f_center']": ".f_center"},
    {".//p[@class='f_center']": ".f_center"}
]
```

```html
    <div class="post_top">
        <div class="post_body">
            <p id="1O5D2DRS">
                <video src="http://flv0.bn.netease.com/6ac0c4.mp4" data-video="http://flv0.bn.netease.com/6ac0c40c71faab9.jpg">
                当地时间4月24日，联合国秘书长古特雷斯与俄外交部长拉夫罗夫举行了会面，双方就乌克兰局势、阿富汗、叙利亚等方面的问题进行了讨论。
            </p>
            <p class="f_center">
                <img src="https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.00ne00esc.jpg">
                <br>
            </p>
            <p id="1O5G5ICJ">视频截图</p>
            <p id="1O556NEP">古特雷斯还向拉夫罗夫提交了一封致俄总统普京的信，概述了旨在改进、延长和扩大黑海粮食协议的方向。
            </p>
            <p id="1O556NEQ">报道称古特雷斯已向该协议的另外两个签署方乌克兰、土耳其，发送了类似函件。
            </p>
            <p id="1O556NER">此外，古特雷斯还向拉夫罗夫介绍了秘书处在解决俄罗斯官员签证问题上所做的最新努力。</p>
            <p class="f_center">
                <img src="https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.000hp00ajc.jpg">
                <br>
            </p>
        </div>
    </div>
```


# 解析结果格式
下述结果不是由上面的html元素解析而来，只是例举出多种标签的结构
```json
[
    {
        "type": "p",
        "context": "Imprimir",
        "link": [
            {
                "start": 0,
                "end": 8,
                "origin_url": "https://www.minsalud.gob.bo/1089-sorata-cumple-con-la-implementacion-de-la-politica-sanitaria-safci-encaminada-por-el-ministerio-de-salud?tmpl=component&print=1&layout=default",
                "url": "https://www.minsalud.gob.bo/1089-sorata-cumple-con-la-implementacion-de-la-politica-sanitaria-safci-encaminada-por-el-ministerio-de-salud?tmpl=component&print=1&layout=default"
            }
        ]
    },
    {
        "type": "img",
        "context": "",
        "link": [
            {
                "origin_url": "https://www.minsalud.gob.bo/images/noticias16/sorata2.gif",
                "url": "Bolivia_Regulation/Files//8b36d2ab18f5fed475dffa42b7e0bbe7."
            }
        ]
    },
    {
        "type": "h1",
        "context": "La Paz – Viernes 6 de Mayo de 2016 | Unidad de Comunicación",
        "link": []
    },
    {
        "type": "h2",
        "context": "Otras peticiones fundamentales fueron la compra de ambulancias",
        "link": []
    },
    {
        "type": "table",
        "link": [],
        "context": [
            {
                "type": "tr",
                "link": [],
                "context": [
                    {
                        "type": "th",
                        "context": "配信動画",
                        "link": []
                    },
                    {
                        "type": "th",
                        "context": "配信日",
                        "link": []
                    }
                ]
            },
            {
                "type": "tr",
                "link": [],
                "context": [
                    {
                        "type": "td",
                        "context": "これでわかる!適合性調査における再審査等申請から日程調整までの手続き -資料作成のポイント-",
                        "link": []
                    },
                    {
                        "type": "td",
                        "context": "2022年11月15日",
                        "link": []
                    }
                ]
            },
            {
                "type": "tr",
                "link": [],
                "context": [
                    {
                        "type": "td",
                        "context": "再審査適合性調査等における解析用データセットの活用について",
                        "link": []
                    },
                    {
                        "type": "td",
                        "context": "2022年11月15日",
                        "link": []
                    }
                ]
            }
        ]
    },
```
