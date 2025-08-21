import httpx
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from notify import notify

load_dotenv()


def mask_sensitive_info(text: str) -> str:
    """脱敏敏感信息，保留首尾，隐藏中间"""
    if not text:
        return text
    
    if len(text) <= 2:
        return text  # 太短不脱敏
    elif len(text) == 3:
        return text[0] + "*" + text[-1]  # 3字符：首*尾
    elif len(text) <= 6:
        return text[:2] + "*" * (len(text) - 4) + text[-2:]  # 短字符串：保留前后2位
    else:
        # 长字符串：保留前后3位
        middle_len = len(text) - 6
        return text[:3] + "*" * middle_len + text[-3:]


def format_account_display(email: str, site_url: str) -> str:
    """格式化账号显示，进行脱敏处理"""
    # 处理邮箱
    if "@" in email:
        username, domain = email.split("@", 1)
        masked_username = mask_sensitive_info(username)
        masked_email = f"{masked_username}@{domain}"
    else:
        masked_email = mask_sensitive_info(email)
    
    # 处理网址
    if site_url.startswith("http"):
        from urllib.parse import urlparse
        parsed = urlparse(site_url)
        domain = parsed.netloc
        masked_domain = mask_sensitive_info(domain)
        masked_url = masked_domain
    else:
        masked_url = mask_sensitive_info(site_url)
    
    return f"{masked_email}-->{masked_url}"


def get_accounts_config() -> List[Dict[str, str]]:
    """从环境变量获取账号配置（JSON格式）"""
    accounts_json = os.getenv("ACCOUNTS")
    if not accounts_json:
        print("[Config] 未找到 ACCOUNTS 环境变量")
        return []

    try:
        accounts = json.loads(accounts_json)
        if not isinstance(accounts, list):
            print("[Config] ACCOUNTS 必须是数组格式")
            return []

        # 验证每个账号配置的必要字段
        valid_accounts = []
        for i, account in enumerate(accounts):
            if not isinstance(account, dict):
                print(f"[Config] 账号 {i + 1} 配置格式错误，跳过")
                continue

            required_fields = ["site_url", "email", "password"]
            if all(field in account and account[field] for field in required_fields):
                valid_accounts.append(account)
            else:
                print(
                    f"[Config] 账号 {i + 1} 缺少必要字段 (site_url, email, password)，跳过"
                )

        return valid_accounts

    except json.JSONDecodeError as e:
        print(f"[Config] ACCOUNTS 格式错误: {e}")
        return []


def checkin_single_account(account: Dict[str, str]) -> Dict[str, Any]:
    """单个账号签到"""
    site_url = account["site_url"]
    email = account["email"]
    password = account["password"]

    login_url = f"{site_url}/auth/login"
    checkin_url = f"{site_url}/user/checkin"

    headers = {
        "origin": site_url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    login_data = {"email": email, "passwd": password}

    result = {
        "site_url": site_url,
        "email": email,
        "success": False,
        "message": "",
        "error": None,
    }

    # 获取脱敏后的显示格式
    display_id = format_account_display(email, site_url)
    
    try:
        print(f"[CheckIn] [{display_id}] 准备登录")

        with httpx.Client(headers=headers, http2=True) as client:
            # 登录
            response = client.post(login_url, data=login_data)
            login_result = response.json()
            print(f"[CheckIn] [{display_id}] 登录结果: {login_result['msg']}")

            # 签到
            checkin_response = client.post(checkin_url)
            checkin_result = checkin_response.json()
            message = checkin_result["msg"]
            print(f"[CheckIn] [{display_id}] 签到结果: {message}")

            result["success"] = True
            result["message"] = message

    except Exception as e:
        error_msg = str(e)
        print(f"[CheckIn] [{display_id}] 捕获异常: {error_msg}")
        result["error"] = error_msg
        result["message"] = f"签到失败: {error_msg}"

    return result


def send_push_notification(results: List[Dict[str, Any]]):
    """发送推送通知"""
    if not results:
        return

    # 构建推送内容
    content_lines = ["📊 自动签到结果汇总", ""]
    success_count = 0
    total_count = len(results)

    for result in results:
        email = result["email"]
        site_url = result["site_url"]
        success = result["success"]
        message = result["message"]

        # 获取脱敏后的显示格式
        display_id = format_account_display(email, site_url)

        if success:
            success_count += 1
            status_icon = "✅"
        else:
            status_icon = "❌"

        content_lines.append(f"{status_icon} {display_id}")
        content_lines.append(f"   {message}")
        content_lines.append("")

    content_lines.append(f"📈 成功率: {success_count}/{total_count}")
    
    title = f"签到领流量 ({success_count}/{total_count})"
    content = "\n".join(content_lines)

    try:
        notify.push_message(title, content, 'text')
        print("[CheckIn] 推送完成")
    except Exception as e:
        print(f"[CheckIn] 推送失败: {e}")


def main():
    """主函数"""
    print("[CheckIn] 开始执行多账号签到")

    # 获取账号配置
    accounts = get_accounts_config()
    if not accounts:
        print("[CheckIn] 未找到有效的账号配置")
        return

    print(f"[CheckIn] 找到 {len(accounts)} 个账号配置")

    # 执行签到
    results = []
    for account in accounts:
        result = checkin_single_account(account)
        results.append(result)

    # 发送推送通知
    send_push_notification(results)

if __name__ == "__main__":
    main()
