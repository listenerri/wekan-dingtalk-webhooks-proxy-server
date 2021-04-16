# wekan-dingtalk-webhooks-proxy-server

A Webhook proxy service between Wekan and DingTalk.

Note: I suggest you use the docker-compose project directly: [wekan-docker-compose](https://github.com/listenerri/wekan-docker-compose)

## Usage

Copy a configuration file from the template and edit it:

```
cp -i config/config-server-example.json config/config-server.json
cp -i config/config-account-example.json config/config-account.json
```

After editing the configuration files, execute the following command to start the service:

```
./scripts/start-aspath-uwsgi-server.sh
```

Or start the service in docker:

```
docker build -t wekan-dingtalk-webhooks-proxy-server .

docker run --name wekan-dingtalk-webhooks-proxy-server \
    --restart always \
    -p 8080:8080 \
    -v `pwd`/config:/opt/wekan-dingtalk-webhooks-proxy-server/config \
    -d \
    wekan-dingtalk-webhooks-proxy-server:latest
```

And then setup a webhook in wekan, let's say our wekan-dingtalk-webhooks-proxy-server is running on `192.168.1.77`,
the webhook address should be `http://192.168.1.77:8080/api/wekan/webhook/`,
that is it, the proxy server will receive, process, and forward webhook requests from wekan.
