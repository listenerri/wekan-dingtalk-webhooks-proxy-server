FROM python:3.10

WORKDIR /opt/wekan-dingtalk-webhooks-proxy-server

COPY . .

#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -r requirements.txt

CMD ["./scripts/start-uwsgi-server.sh"]
