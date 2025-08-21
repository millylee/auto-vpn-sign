import httpx
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


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

    try:
        print(f"[CheckIn] [{email}@{site_url}] 准备登录")

        with httpx.Client(headers=headers, http2=True) as client:
            # 登录
            response = client.post(login_url, data=login_data)
            login_result = response.json()
            print(f"[CheckIn] [{email}@{site_url}] 登录结果: {login_result['msg']}")

            # 签到
            checkin_response = client.post(checkin_url)
            checkin_result = checkin_response.json()
            message = checkin_result["msg"]
            print(f"[CheckIn] [{email}@{site_url}] 签到结果: {message}")

            result["success"] = True
            result["message"] = message

    except Exception as e:
        error_msg = str(e)
        print(f"[CheckIn] [{email}@{site_url}] 捕获异常: {error_msg}")
        result["error"] = error_msg
        result["message"] = f"签到失败: {error_msg}"

    return result


def send_push_notification(results: List[Dict[str, Any]]):
    """发送推送通知"""
    push_plus_token = os.getenv("PUSHPLUS_TOKEN")
    if not push_plus_token:
        return

    # 构建推送内容
    content_lines = ["📊 自动签到结果汇总\n"]
    success_count = 0
    total_count = len(results)

    for result in results:
        email = result["email"]
        site_url = result["site_url"]
        success = result["success"]
        message = result["message"]

        if success:
            success_count += 1
            status_icon = "✅"
        else:
            status_icon = "❌"

        content_lines.append(f"{status_icon} {email}@{site_url}")
        content_lines.append(f"   {message}\n")

    content_lines.append(f"📈 成功率: {success_count}/{total_count}")
    content = "\n".join(content_lines)

    push_plus_data = {
        "token": push_plus_token,
        "title": f"签到领流量 ({success_count}/{total_count})",
        "content": content,
        "template": "txt",
        "channel": "wechat",
    }

    try:
        push_plus_url = "http://www.pushplus.plus/send"
        with httpx.Client() as client:
            client.post(push_plus_url, data=json.dumps(push_plus_data))
        print("[CheckIn] 推送成功")
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

    print("[CheckIn] 所有账号签到完成")


if __name__ == "__main__":
    main()
