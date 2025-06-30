requests建立在python原生库urllib、第三方库urllib3的基础上，提供了方便易用的HTTP功能

# 请求与响应

```python
import requests

# 简单请求
response = requests.get(
    'example.com',
    params={'page', '1'},                     # GET参数
    headers={'User-Agent': 'Mozilla/5.0'}     # 请求头
    cookies={'SESSIONID':'8A25432CEC745A1C'}  # Cookie
)

# 响应
r = get_response
r.status_code   # 状态码 
r.headers       # 响应头, dict
r.text          # 文本格式的响应体
r.content       # 二进制格式的响应体
r.json()        # 用json解码的响应体
```

# 会话

https://requests.readthedocs.io/en/latest/user/advanced/

Session对象可进行会话管理，在多个请求之间复用请求头、自动管理Cookie、复用TCP连接

```python
s =  requests.Session()

# 设置会话参数。这些参数在后续请求都会使用；若服务器Set-Cookie也会在会话中自动使用
sess.headers.update({'User-Agent': 'Mozilla/5.0'})   # 请求头
sess.cookies.set('_SESSID', '1CvdAc0VkE13nc')        # Cookie
sess.proxies = {'http': '192.168.0.1:8080'}          # Proxy

# 请求资源
domain = 'https://example.com'
try:
    # GET请求，并用BeautifulSoup分析响应
    response = sess.get(f'{domain}/thread', params={'file': 'a.png'})
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': '_token'})['value']
    # POST请求。注意：post方法添加的header只在此次请求生效
    sess.post(f'{domain}/thread', header={'X-TOKEN': token}, data={'text':'example'})
except Exception as e:
    print(str(traceback.format_exc()))
```

需要对请求进行额外处理，比如修改自动生成的`Content-Length`头以实现HTTP请求走私，可以用prepared request

```python
sess = requests.Session()
req = Request('GET', 'example.com')
# 生成prepared request并做特殊处理
prep = req.prepare()
prep.body = 'GET /secret HTTP/1.1\r\nHost: example.com\r\n\r\n'
# 发出请求
sess.send(prep)
```

# 其他

忽略SSL

```python
requests.packages.urllib3.disable_warnings()
requests.get('https://example.com', verify=False)
```
