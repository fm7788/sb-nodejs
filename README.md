## 一、服务器在Node.js环境搭建vless-ws-tls脚本

目前新注册的Webhostmost账号的开发者工具（Development Tools）有Terminal，说明可以进入SSH，然后输入以下一键脚本，这样就不用上传文件了

UUID：你的uuid

PORT：服务器可使用的端口，建议留空随机生成

DOMAIN：已解析在CF的域名

```
wget -N https://raw.githubusercontent.com/fm7788/sb-nodejs/main/whm.sh && UUID=你的uuid PORT=服务器可使用的端口 DOMAIN=已解析在CF的域名 bash whm.sh
```

建议使用外部节点保活方式，可使用workers_keep文件进行保活

节点保活及节点信息地址：https://你已解析在CF的域名/你的uuid

-----------------------------------------------------

## 二、Claw.Cloud在Node.js环境搭建vless-ws-tls脚本

填写UUID、端口、域名三个变量再运行脚本，现实一键无交互运行，每次重装后输出节点信息不变

Claw.Cloud专用一键脚本(无交互)：

```
wget -N https://raw.githubusercontent.com/fm7788/sb-nodejs/main/app.js && UUID=你的uuid PORT=服务器可使用的端口 DOMAIN=服务器域名 node app.js
```
----------------------------------------------------------
##三 TUIC在Nodejs/Python一键脚本极简部署

curl -Ls https://raw.githubusercontent.com/fm7788/sb-nodejs/main/tuic/tuic.sh | sed 's/\r$//' | bash

-----------------------------------------------------
-----------------------------------------------------

### 相关教程可参考甬哥博客，视频教程如下：

[JAR最新搭建免费节点最终教程：]((https://www.youtube.com/watch?v=zsFbuPsodrg))

[Webhostmost最新搭建免费节点最终教程（二）：免费节点绕过收费限制？终结了！Webhostmost最后的一期](https://youtu.be/F7qA6XYCHv8)

[Claw.cloud免费VPS搭建代理最终教程：全网最简单 | 两大无交互回车脚本 | 套CDN优选IP | workers反代 | ArgoSB隧道搭建](https://youtu.be/Esofirx8xrE)

更新中……

----------------------------------------------------------

### 感谢你右上角的star🌟
[![Stargazers over time](https://starchart.cc/fm7788/sb-nodejs.svg)](https://starchart.cc/fm7788/sb-nodejs)

### 声明：所有代码来源于Github社区与ChatGPT的整合
