# 自动签到

> 每天自动领取流量

Fork 仓库，在 `Settings - Secrets - Actions` 中添加 `EMAIL`、`PASSWORD`、`SITE_URL` 环境变量，然后切到 Actions 手动运行任务看下输出日志，成功后大约在每天凌晨 1 点执行。可以添加 `PUSHPLUS_TOKEN` 用于接收 pushplus 的微信推送。

当前可用的域名后缀为 `.me`、`.top`

改用 `python` 直接请求接口，原无头模式放 `nodejs-headless` 分支。
