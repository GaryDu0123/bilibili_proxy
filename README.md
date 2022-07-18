# bilibili_proxy
a proxy service to fetch the audio source from bilibili.com

# Installation and Deployment

## Dependencies

+ make sure your image `shuyangzhang/kyouka` version >= 0.7.1

```bash
docker pull shuyangzhang/kyouka
```

## Instruction

1. pull latest version of `shuyangzhang/bilibili_proxy` image.

```bash
docker pull shuyangzhang/bilibili_proxy
```

2. start up a bproxy container, reflect port to your local. ( e.g. `127.0.0.1:11936`, you can modify the port number as you like. )

```bash
docker run --name bproxy --restart always -d -p 127.0.0.1:11936:8080 shuyangzhang/bilibili_proxy
```

3. add `LOCAL_BPROXY` and `LOCAL_BPROXY_URL` settings at the end of your `.env` config file.

> WARN: the port should be same to step2 that you configured.

```bash
LOCAL_BPROXY=true
LOCAL_BPROXY_URL=http://host.docker.internal:11936
```

4. finally, run a new container for `shuyangzhang/kyouka` image.

```bash
docker run --name kyouka-manager --env-file .env -v /var/run/docker.sock:/var/run/docker.sock --restart always -d shuyangzhang/kyouka
```

5. enjoy!