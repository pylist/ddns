#基于的基础镜像
FROM python:3.7
#创建工作空间
WORKDIR /ddns
COPY . /ddns

# 安装依赖
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt

CMD ["python", "ddns.py"]
