import yaml
import requests
import time
import logging, sys
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    datefmt='%y/%m/%d %H:%M:%S')

# 封装的api请求
# def dnsPOST(url, data):
#     params = dict({
#         "login_token": login_token,
#         "format": "json",
#         "lang": "cn",
#     }, **data)
#     headers = {
#         "user-agent": "MJJ DDNS Python/1.0.0 (apiapi@foxmail.com)"
#     }
#     resp = requests.post(url, headers=headers, data=params)
#     if resp.status_code == 200:
#         return resp.json()


class DDNS:
    def __init__(self):
        """
        config里面包含的数据
        ID和Token dnspod认证的必须, 格式 iD,Token用逗号隔开
        domain 域名
        sub_domain 域名前缀
        myipAPI 获取公网IP接口
        """
        self.config = self.loadConfig()
        self.login_token = str(self.config.get("ID")) + "," + self.config.get("Token")
        self.format = "json"
        self.lang = "cn"
        self.headers = {"User-Agent": "MJJ DDNS Python/1.0.0 (apiapi@foxmail.com)"}
        self.myipApi = self.config.get("myipAPI")
        self.data = {
            "login_token": self.login_token,
            "format": self.format,
            "lang": self.lang,
        }
        self.record_id, self.record_value = self.getRecordInfo()
    #读取本地配置文件
    def loadConfig(self):
        with open("config.yaml", "r", encoding="utf8") as file:
            dnspod = yaml.safe_load(file).get("DNSPOD")
        logging.info("读取配置文件成功")
        return dnspod

    # 获取公网IP
    def getMyIP(self):
        ip = requests.get(self.myipApi).text
        logging.info("你的公网IP是:%s", ip)
        return ip

    # 获取更新记录所需要的
    def getRecordInfo(self):
        recordList = self.getRecordList()
        for record in recordList["records"]:
            if record.get("name") == self.config.get("sub_domain"):
                record_id, record_value = (record.get("id"), record.get("value"))
                logging.info("获取record信息成功,id:%s value:%s",record_id, record_value)
                return (record_id, record_value)


    # 更新记录
    def updateRecord(self, myip):
        url = "https://dnsapi.cn/Record.Modify"
        data = self.data.copy()
        data.update({
                "domain": self.config.get("cionfig"),
                "record_id": self.record_id,
                "sub_domain": self.config.get("sub_domain"),
                "record_type": "A",
                "record_line": "默认",
                "value": myip,
            })
        try:
            resp = requests.post(url, headers=self.headers, data=data).json()
            if resp["status"]["code"] == "1":
                logging.info("ddns的ip地址修改为:%s", myip)
        except:
            logging.warning("由于网络问题, 更新ddns的ip地址失败")

    # 获取域名的记录列表
    def getRecordList(self):
        url = "https://dnsapi.cn/Record.List"
        data = self.data.copy()
        data.update({
            "domain": self.config.get("domain"),
            # "sub_domain": self.config.get("sub_domain"),
        })
        try:
            dataJson = requests.post(url, headers=self.headers, data=data).json()
            logging.info("dns域名列表记录获取成功")
        except:
            logging.info("dns接口获取失败")
            return None
        return dataJson

    # 循环检测IP是否变更, 如果变更就更新
    def testingIP(self):
        myip = self.getMyIP()
        if myip not in self.record_value:
            self.updateRecord(myip)
            self.record_value = myip
        else:
            logging.info("ip:%s没有变动, 无需更改", myip)


if __name__ == '__main__':
    ddns = DDNS()
    while True:
        ddns.testingIP()
        time.sleep(300)
