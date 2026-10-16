#!/usr/bin/env python3
import sys
import os

def patch_at_server(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace import aiohttp
    if 'import aiohttp' in content:
        content = content.replace('import aiohttp', 'import urllib.request\nimport urllib.error')

    # 2. Replace aiohttp ClientSession block in _do_send
    target_pattern = """                timeout = aiohttp.ClientTimeout(total=5)
                connector = aiohttp.TCPConnector(
                    force_close=True,
                    enable_cleanup_closed=True,
                    ssl=False
                )
                
                async with aiohttp.ClientSession(
                    timeout=timeout, 
                    connector=connector
                ) as session:
                    message = {
                        "msgtype": "text",
                        "text": {"content": content}
                    }
                    
                    async with session.post(
                        self.webhook_url,
                        json=message,
                        headers={
                            'Content-Type': 'application/json',
                            'User-Agent': 'Mozilla/5.0'
                        }
                    ) as response:
                        response_text = await response.text()
                        
                        if response.status == 200:
                            try:
                                result = await response.json()
                                if result.get('errcode') == 0:
                                    logger.info(f"企业微信通知发送成功: {sender}")
                                    return
                                else:
                                    raise Exception(f"企业微信API错误: {result}")
                            except json.JSONDecodeError as je:
                                raise Exception(f"响应解析失败: {je}")
                        
                        raise Exception(f"HTTP错误 {response.status}: {response_text}")"""

    replacement = """                message = {
                    "msgtype": "text",
                    "text": {"content": content}
                }
                req = urllib.request.Request(
                    self.webhook_url,
                    data=json.dumps(message).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0'
                    }
                )
                loop = asyncio.get_running_loop()
                def _send():
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        return resp.read().decode('utf-8'), resp.status
                response_text, resp_status = await loop.run_in_executor(None, _send)
                if resp_status == 200:
                    try:
                        result = json.loads(response_text)
                        if result.get('errcode') == 0:
                            logger.info(f"企业微信通知发送成功: {sender}")
                            return
                        else:
                            raise Exception(f"企业微信API错误: {result}")
                    except json.JSONDecodeError as je:
                        raise Exception(f"响应解析失败: {je}")
                raise Exception(f"HTTP错误 {resp_status}: {response_text}")"""

    # Normalize newlines
    normalized_content = content.replace('\r\n', '\n')
    normalized_target = target_pattern.replace('\r\n', '\n')
    normalized_replacement = replacement.replace('\r\n', '\n')

    if normalized_target in normalized_content:
        normalized_content = normalized_content.replace(normalized_target, normalized_replacement)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(normalized_content)
        print(f"Successfully patched {file_path} to use urllib.request")
        return True
    else:
        print("Warning: target block not found in content, checking if already patched")
        if 'urllib.request' in normalized_content:
            print(f"{file_path} is already patched.")
            return True
        return False

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'test_patch.py'
    success = patch_at_server(target)
    sys.exit(0 if success else 1)
