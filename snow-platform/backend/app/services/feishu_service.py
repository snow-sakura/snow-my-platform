import httpx
from typing import List, Optional
from loguru import logger
from app.core.config import settings


class FeishuService:
    """飞书Webhook通知服务"""
    
    @staticmethod
    async def send_notification(title: str, content: str, 
                               webhook_url: Optional[str] = None) -> bool:
        """发送飞书通知"""
        
        url = webhook_url or settings.FEISHU_WEBHOOK_URL
        
        if not url:
            logger.warning("飞书Webhook URL未配置")
            return False
        
        message = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": content
                                }
                            ]
                        ]
                    }
                }
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=message,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"飞书通知发送成功: {title}")
                    return True
                else:
                    logger.error(f"飞书通知发送失败: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"飞书通知发送异常: {e}")
            return False
    
    @staticmethod
    async def notify_test_points_extracted(project_name: str, count: int) -> bool:
        """通知测试点提取完成"""
        title = "测试点提取完成"
        content = f"项目【{project_name}】已完成测试点提取，共提取 {count} 个测试点。"
        return await FeishuService.send_notification(title, content)
    
    @staticmethod
    async def notify_test_cases_generated(project_name: str, count: int) -> bool:
        """通知测试用例生成完成"""
        title = "测试用例生成完成"
        content = f"项目【{project_name}】已完成测试用例生成，共生成 {count} 个测试用例。"
        return await FeishuService.send_notification(title, content)


feishu_service = FeishuService()
