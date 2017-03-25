import re
def decodeCorpDetails():
    decodeMethod = re.compile(r'<h1 class="mbt">[\u4e00-\u9fa5]+</h1>')
    data = '<h1 class="mbt">深圳亿森众合科技有限公司</h1>'
    decodeMethod.search(data)
    print(decodeMethod)
decodeCorpDetails()

