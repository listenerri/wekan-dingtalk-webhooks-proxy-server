FROM python:3.5

WORKDIR /opt/ipwave-aspath-api

COPY . .

#RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -r requirements.txt

CMD ["./start-aspath-uwsgi-server.sh"]
