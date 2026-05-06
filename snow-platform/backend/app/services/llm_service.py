import litellm
from typing import List, Optional, Dict, Any
from loguru import logger
from app.core.config import settings


class LLMService:
    """LLM服务 - 使用LiteLLM统一接口"""
    
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.base_url = settings.LLM_BASE_URL
        logger.info(f"LLM服务初始化完成, 模型: {self.model}")
    
    async def extract_test_points(self, document_content: str, 
                                  rag_context: Optional[str] = None) -> List[Dict[str, Any]]:
        """从文档中提取测试点"""
        
        system_prompt = """你是一个专业的测试工程师。请分析提供的产品需求文档，提取出关键的测试点。

每个测试点应包含：
- title: 测试点标题（简洁明了）
- description: 测试点详细描述
- priority: 优先级（HIGH/MEDIUM/LOW）
- category: 测试分类（功能/UI/性能/安全/兼容性等）

请以JSON数组格式返回，例如：
[
  {
    "title": "用户登录功能",
    "description": "验证用户使用正确的用户名和密码能够成功登录系统",
    "priority": "HIGH",
    "category": "功能"
  }
]

只返回JSON数组，不要有其他内容。"""
        
        user_prompt = f"请分析以下产品需求文档，提取测试点：\n\n{document_content}"
        
        if rag_context:
            user_prompt += f"\n\n参考资料库信息：\n{rag_context}"
        
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.3,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # 解析JSON响应
            import json
            test_points = json.loads(content)
            
            logger.info(f"成功提取 {len(test_points)} 个测试点")
            return test_points
            
        except Exception as e:
            logger.error(f"提取测试点失败: {e}")
            raise
    
    async def generate_test_cases(self, test_point: Dict[str, Any], 
                                  rag_context: Optional[str] = None) -> List[Dict[str, Any]]:
        """根据测试点生成测试用例"""
        
        system_prompt = """你是一个资深的测试工程师。请根据提供的测试点，生成详细的测试用例。

每个测试用例应包含：
- title: 测试用例标题
- precondition: 前置条件
- steps: 测试步骤数组，每个步骤包含 step（操作步骤）和 expected_result（预期结果）
- expected_result: 总体预期结果
- priority: 优先级（HIGH/MEDIUM/LOW）
- case_type: 用例类型（功能/UI/性能/安全/兼容性等）

请以JSON数组格式返回，例如：
[
  {
    "title": "正常登录测试",
    "precondition": "用户已注册且账户处于激活状态",
    "steps": [
      {
        "step": "打开登录页面",
        "expected_result": "显示登录表单"
      },
      {
        "step": "输入正确的用户名和密码",
        "expected_result": "输入框接受输入"
      },
      {
        "step": "点击登录按钮",
        "expected_result": "成功登录并跳转到首页"
      }
    ],
    "expected_result": "用户成功登录系统",
    "priority": "HIGH",
    "case_type": "功能"
  }
]

只返回JSON数组，不要有其他内容。"""
        
        user_prompt = f"""测试点信息：
标题：{test_point.get('title', '')}
描述：{test_point.get('description', '')}
优先级：{test_point.get('priority', 'MEDIUM')}
分类：{test_point.get('category', '')}

请为上述测试点生成详细的测试用例。"""
        
        if rag_context:
            user_prompt += f"\n\n参考资料库信息：\n{rag_context}"
        
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.3,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # 解析JSON响应
            import json
            test_cases = json.loads(content)
            
            logger.info(f"成功生成 {len(test_cases)} 个测试用例")
            return test_cases
            
        except Exception as e:
            logger.error(f"生成测试用例失败: {e}")
            raise


# 全局LLM服务实例
llm_service = LLMService()
