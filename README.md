# ddns
将用户的动态IP地址映射到一个固定的域名解析服务上，用户每次连接网络的时候客户端程序就会通过信息传递把该主机的动态IP地址传送给位于服务商主机上的服务器程序，服务器程序负责提供DNS服务并实现动态域名解析。

#config.yaml例子
```
DNSPOD:
  ID: 110110
  Token: 5as5d5as4d4assa22sas5a5a2za5a
  domain: qq.com
  sub_domain: home
  myipAPI: https://api.py3c.net/myip
```
