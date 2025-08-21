# 自动签到

> 每天自动领取流量

## 安装和运行

### 使用 uv（推荐）

```bash
# 安装依赖
uv sync

# 运行
uv run main.py
```

### 环境变量配置

#### 账号配置

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

#### 推送配置

- `PUSHPLUS_TOKEN`（可选）：用于接收 pushplus 的微信推送

### GitHub Actions 自动运行

Fork 仓库，在 `Settings - Secrets - Actions` 中添加环境变量：

- `ACCOUNTS`：账号配置的 JSON 字符串
- `PUSHPLUS_TOKEN`（可选）：推送 token

配置完成后，切到 Actions 手动运行任务查看输出日志，成功后大约在每天凌晨 1 点自动执行。
