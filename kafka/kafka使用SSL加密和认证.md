# kafka使用SSL加密和认证

1、创建几个目录保存证书

```shell
mkdir /usr/ca
cd /usr/ca
mkdir root client server trust
```

这四个目录分别用来存放 根证书、客户端证书、服务端证书、受信任的证书。

2、为每个Kafka broker生成SSL密钥和证书

```shell
keytool -keystore /usr/ca/server/server.keystore.jks -alias localhost -validity 365 -genkey -keypass 123123 -storepass 123123 -dname "CN=localhost,OU=antiy,O=antiy,L=haerbin,S=haerbin,C=cn"
```

验证证书内容

`````shell
keytool -list -v -keystore /usr/ca/server/server.keystore.jks
`````

3、生成CA认证证书

````shell
req -new -x509 -keyout /usr/ca/root/ca-key -out /usr/ca/root/ca-cert -days 365 -passout pass:123123 -subj "/C=cn/ST=antiy/L=haerbin/O=antiy/OU=antiy/CN=localhost"
````

4、通过CA证书创建一个客户端信任证书

```shell
keytool -keystore /usr/ca/trust/client.truststore.jks -alias CARoot -import -file /usr/ca/root/ca-cert -storepass 123123
```

5、通过CA证书创建一个服务端器端信任证书

```shell
keytool -keystore /usr/ca/trust/server.truststore.jks -alias CARoot -import -file /usr/ca/root/ca-cert -storepass 123123
```

6、服务器证书的签名处理

- 导出证书

```shell
keytool -keystore /usr/ca/server/server.keystore.jks -alias localhost -certreq -file /usr/ca/server/server.cert-file -storepass 123123
```

- 用CA给服务器端证书进行签名处理

```shell
openssl x509 -req -CA /usr/ca/root/ca-cert -CAkey /usr/ca/root/ca-key -in /usr/ca/server/server.cert-file -out /usr/ca/server/server.cert-signed -days 365 -CAcreateserial -passin pass:123123
```

- 将CA证书导入到服务器端keystore。

```shell
keytool -keystore /usr/ca/server/server.keystore.jks -alias CARoot -import -file /usr/ca/root/ca-cert -storepass 123123
```

- 将已签名的服务器证书导入到服务器keystore

```shell
keytool -keystore /usr/ca/server/server.keystore.jks -alias localhost -import -file /usr/ca/server/server.cert-signed -storepass 123123
```

7、客户端SSL证书签发

- 导出客户端证书

```shell
keytool -keystore /usr/ca/client/client.keystore.jks -alias localhost -validity 365 -genkey -keypass 123123 -dname "CN=localhost,OU=antiy,O=antiy,L=haerbin,S=haerbin,C=cn" -ext SAN=DNS:localhost -storepass 123123
```

- 将证书文件导入到keystore

```shell
keytool -keystore /usr/ca/client/client.keystore.jks -alias localhost -certreq -file /usr/ca/client/client.cert-file -storepass 123123
```

- ca给客户端证书签名

```shell
openssl x509 -req -CA /usr/ca/root/ca-cert -CAkey /usr/ca/root/ca-key -in /usr/ca/client/client.cert-file -out /usr/ca/client/client.cert-signed -days 365 -CAcreateserial -passin pass:123123
```

- ca证书导入客户端keystore

```shell
keytool -keystore /usr/ca/client/client.keystore.jks -alias CARoot -import -file /usr/ca/root/ca-cert -storepass 123123
```

- 将已签名的证书导入客户端keystore

```shell
keytool -keystore /usr/ca/client/client.keystore.jks -alias localhost -import -file /usr/ca/client/client.cert-signed -storepass 123123
```

8、kafka配置

````shell

listeners=SSL://ip:9095
advertised.listeners=SSL://ip:9095
ssl.keystore.location=/usr/ca/server/server.keystore.jks
ssl.keystore.password=123123
ssl.key.password=123123
ssl.truststore.location=/usr/ca/trust/server.truststore.jks
ssl.truststore.password=123123
ssl.client.auth=required
ssl.enabled.protocols=TLSv1.2,TLSv1.1,TLSv1
ssl.keystore.type=JKS 
ssl.truststore.type=JKS 
# kafka2.0.x开始，将ssl.endpoint.identification.algorithm设置为了HTTPS，即:需要验证主机名
# 如果不需要验证主机名，那么可以这么设置 ssl.endpoint.identification.algorithm=即可
ssl.endpoint.identification.algorithm=HTTPS
# 设置内部访问也用SSL，默认值为security.inter.broker.protocol=PLAINTEXT
security.inter.broker.protocol=SSL
````

9、客户端配置

```shell
security.protocol=SSL
ssl.truststore.location=/usr/ca/trust/server.truststore.jks
ssl.truststore.password=123123
ssl.keystore.password=123
ssl.keystore.location=/usr/ca/server/server.keystore.jks
```

