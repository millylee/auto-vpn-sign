# 自动签到

> 每天自动领取流量

## GitHub Actions 自动运行

Fork 仓库，在 `Settings - Secrets - Actions` 中添加环境变量：

- `ACCOUNTS`：必填，账号配置的数组对象

配置完成后，切到 Actions 手动运行任务查看输出日志，成功后大约在每天凌晨 1 点自动执行。

## 账号配置

使用 `ACCOUNTS` 环境变量配置账号信息（JSON 数组格式）：

```json
// 多账号配置示例
[
  {
    "site_url": "https://example1.me",
    "email": "user1@example.com", 
    "password": "password1"
  },
  {
    "site_url": "https://example2.top",
    "email": "user2@example.com",
    "password": "password2"
  }
]

// 单账号配置
[
  {
    "site_url": "https://example.me",
    "email": "user@example.com",
    "password": "password"
  }
]
```

**必要字段说明：**
- `site_url`：站点地址
- `email`：登录邮箱
- `password`：登录密码

## 推送配置

### 飞书机器人
- `FEISHU_WEBHOOK`: 飞书机器人的 Webhook 地址

### 钉钉机器人
- `DINGDING_WEBHOOK`: 钉钉机器人的 Webhook 地址

### 企业微信机器人
- `WEIXIN_WEBHOOK`: 企业微信机器人的 Webhook 地址

### PushPlus 推送
- `PUSHPLUS_TOKEN`: PushPlus 的 Token

### Server酱
- `SERVERPUSHKEY`: Server酱的 SendKey

### 邮箱通知
- `EMAIL_USER`: 发件人邮箱地址
- `EMAIL_PASS`: 发件人邮箱密码/授权码
- `EMAIL_TO`: 收件人邮箱地址

## 本地测试

复制 `.env.example` 为 `.env`，并配置需要的字段

```bash
# 安装依赖
uv sync

# 本地运行
uv run main.py
```
