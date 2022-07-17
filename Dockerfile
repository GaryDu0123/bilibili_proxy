FROM python:3.9-buster

LABEL maintainer="zhangshuyang@outlook.com"

ENV PYTHONIOENCODING=utf-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /bilibili_proxy

COPY requirements.txt /bilibili_proxy
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && \
    rm -rf /tmp/*

COPY ./app /bilibili_proxy/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080", "--timeout-keep-alive=30"]