#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用AI补全药膳信息的脚本
"""

import pymysql
import json
import requests
import time
from typing import Dict, Any, Optional

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '5845201314',
    'database': 'tcm_health_system',
    'charset': 'utf8mb4'
}

# DeepSeek AI配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-d578be5b1e7245ecb313400e8f893735"
DEEPSEEK_MODEL = "deepseek-chat"

# 体质类型映射
CONSTITUTION_MAP = {
    'PINGHE': '平和质',
    'QIXU': '气虚质',
    'YANGXU': '阳虚质',
    'YINXU': '阴虚质',
    'TANSHI': '痰湿质',
    'SHIRE': '湿热质',
    'XUEYU': '血瘀质',
    'QIYU': '气郁质',
    'TEBING': '特禀质'
}

# 季节映射
SEASON_MAP = {
    'SPRING': '春季',
    'SUMMER': '夏季',
    'AUTUMN': '秋季',
    'WINTER': '冬季',
    'ALL': '四季'
}


def call_ai_api(prompt: str, max_retries: int = 3) -> Optional[str]:
    """调用DeepSeek AI API"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}'
    }
    
    data = {
        'model': DEEPSEEK_MODEL,
        'messages': [
            {
                'role': 'system',
                'content': '你是一位专业的中医药膳专家，擅长根据药膳名称和现有信息，补全详细的药膳信息。请用中文回答，返回JSON格式的数据。'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7,
        'max_tokens': 2000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return content
            else:
                print(f"API返回格式异常: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                return None
    
    return None


def parse_ai_response(response: str) -> Dict[str, Any]:
    """解析AI返回的JSON数据"""
    try:
        # 清理响应文本，提取JSON部分
        response = response.strip()
        
        # 如果包含代码块标记，提取JSON部分
        if '```json' in response:
            response = response.split('```json')[1].split('```')[0].strip()
        elif '```' in response:
            # 可能是 ```json 或 ```
            parts = response.split('```')
            for i, part in enumerate(parts):
                if 'json' in part.lower() or (i > 0 and '{' in part):
                    response = part.strip()
                    if response.startswith('json'):
                        response = response[4:].strip()
                    break
        
        # 查找第一个 { 和最后一个 }
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            response = response[start_idx:end_idx + 1]
        
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        print(f"原始响应: {response[:500]}...")  # 只显示前500字符
        return {}


def generate_prompt(recipe: Dict[str, Any]) -> str:
    """生成AI提示词"""
    recipe_name = recipe.get('recipe_name', '')
    current_efficacy = recipe.get('efficacy', '')
    current_season = recipe.get('season', '')
    current_constitution = recipe.get('constitution_type', '')
    current_ingredients = recipe.get('ingredients', '[]')
    current_steps = recipe.get('steps', '[]')
    current_cooking_time = recipe.get('cooking_time')
    current_servings = recipe.get('servings')
    current_category = recipe.get('category', '')
    
    # 解析现有食材
    try:
        ingredients_list = json.loads(current_ingredients) if current_ingredients else []
        ingredients_text = ', '.join([f"{item.get('name', '')} {item.get('amount', '')}" for item in ingredients_list])
    except:
        ingredients_text = current_ingredients
    
    prompt = f"""请根据以下药膳信息，补全并优化详细信息。请返回JSON格式，包含以下字段：

药膳名称：{recipe_name}
现有功效：{current_efficacy or '未填写'}
现有适用季节：{current_season or '未填写'}
现有适用体质：{current_constitution or '未填写'}
现有食材：{ingredients_text}
现有制作步骤：{current_steps}
现有制作时间：{current_cooking_time or '未填写'}分钟
现有适宜人数：{current_servings or '未填写'}人份
分类：{current_category}

请返回以下格式的JSON（所有字段都必须填写）：
{{
    "efficacy": "详细的功效说明（50-100字）",
    "season": "适用季节，多个用逗号分隔（SPRING/SUMMER/AUTUMN/WINTER/ALL）",
    "constitutionType": "适用体质，多个用逗号分隔（PINGHE/QIXU/YANGXU/YINXU/TANSHI/SHIRE/XUEYU/QIYU/TEBING）",
    "cookingTime": 制作时间（分钟，整数）,
    "servings": 适宜人数（人份，整数）,
    "steps": ["步骤1", "步骤2", "步骤3", ...]（制作步骤数组，至少5步，每步详细描述）,
    "suitableSymptoms": "适用症状（50-100字）",
    "contraindications": "禁忌说明（30-50字）",
    "tips": "烹饪小贴士（30-50字）"
}}

注意：
1. 如果现有信息合理，请优化并保留
2. 如果现有信息不完整，请根据药膳名称和食材补全
3. 制作步骤要详细、可操作
4. 所有文本用中文
5. 只返回JSON，不要其他说明文字"""
    
    return prompt


def update_recipe(conn, recipe_id: int, data: Dict[str, Any], update_all: bool = False) -> bool:
    """更新药膳信息到数据库
    
    Args:
        conn: 数据库连接
        recipe_id: 药膳ID
        data: AI返回的数据
        update_all: 是否更新所有字段（True）或只更新空字段（False）
    """
    try:
        cursor = conn.cursor()
        
        # 如果需要检查现有值，先查询
        existing = None
        if not update_all:
            check_cursor = conn.cursor(pymysql.cursors.DictCursor)
            check_cursor.execute("SELECT * FROM herbal_recipe WHERE id = %s", (recipe_id,))
            existing = check_cursor.fetchone()
            check_cursor.close()
        
        # 构建更新SQL
        update_fields = []
        update_values = []
        
        # 功效
        if 'efficacy' in data:
            if update_all or not existing or not existing.get('efficacy'):
                update_fields.append('efficacy = %s')
                update_values.append(data['efficacy'])
        
        # 季节
        if 'season' in data:
            if update_all or not existing or not existing.get('season'):
                update_fields.append('season = %s')
                update_values.append(data['season'])
        
        # 体质
        if 'constitutionType' in data:
            if update_all or not existing or not existing.get('constitution_type'):
                update_fields.append('constitution_type = %s')
                update_values.append(data['constitutionType'])
        
        # 制作时间
        if 'cookingTime' in data:
            try:
                cooking_time = int(data['cookingTime'])
                if update_all or not existing or not existing.get('cooking_time'):
                    update_fields.append('cooking_time = %s')
                    update_values.append(cooking_time)
            except (ValueError, TypeError):
                print(f"    警告: cookingTime 值无效: {data.get('cookingTime')}")
        
        # 适宜人数
        if 'servings' in data:
            try:
                servings = int(data['servings'])
                if update_all or not existing or not existing.get('servings'):
                    update_fields.append('servings = %s')
                    update_values.append(servings)
            except (ValueError, TypeError):
                print(f"    警告: servings 值无效: {data.get('servings')}")
        
        # 制作步骤
        if 'steps' in data and isinstance(data['steps'], list):
            if update_all or not existing or not existing.get('steps'):
                update_fields.append('steps = %s')
                update_values.append(json.dumps(data['steps'], ensure_ascii=False))
        
        # 适用症状
        if 'suitableSymptoms' in data:
            if update_all or not existing or not existing.get('suitable_symptoms'):
                update_fields.append('suitable_symptoms = %s')
                update_values.append(data['suitableSymptoms'])
        
        # 禁忌说明
        if 'contraindications' in data:
            if update_all or not existing or not existing.get('contraindications'):
                update_fields.append('contraindications = %s')
                update_values.append(data['contraindications'])
        
        # 烹饪小贴士
        if 'tips' in data:
            if update_all or not existing or not existing.get('tips'):
                update_fields.append('tips = %s')
                update_values.append(data['tips'])
        
        if not update_fields:
            print(f"  没有需要更新的字段")
            cursor.close()
            return False
        
        update_values.append(recipe_id)
        
        sql = f"""
            UPDATE herbal_recipe 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        cursor.execute(sql, update_values)
        conn.commit()
        cursor.close()
        
        return True
        
    except Exception as e:
        print(f"  更新数据库失败: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("药膳信息AI补全脚本")
    print("=" * 60)
    print()
    print("提示: 此脚本将使用AI补全药膳信息并更新到数据库")
    print("     默认只更新空字段，保留已有数据")
    print()
    
    # 询问是否更新所有字段
    update_all = False
    try:
        choice = input("是否更新所有字段（包括已有数据的字段）？(y/N): ").strip().lower()
        update_all = choice == 'y'
    except:
        pass
    
    # 连接数据库
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("✓ 数据库连接成功")
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return
    
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 查询所有药膳
        cursor.execute("SELECT * FROM herbal_recipe ORDER BY id")
        recipes = cursor.fetchall()
        cursor.close()
        
        print(f"✓ 找到 {len(recipes)} 条药膳记录")
        print()
        
        # 处理每条药膳
        success_count = 0
        fail_count = 0
        
        for idx, recipe in enumerate(recipes, 1):
            recipe_id = recipe['id']
            recipe_name = recipe['recipe_name']
            
            print(f"[{idx}/{len(recipes)}] 处理: {recipe_name} (ID: {recipe_id})")
            
            # 生成提示词
            prompt = generate_prompt(recipe)
            
            # 调用AI API
            print("  正在调用AI API...")
            ai_response = call_ai_api(prompt)
            
            if not ai_response:
                print("  ✗ AI API调用失败")
                fail_count += 1
                time.sleep(1)  # 避免请求过快
                continue
            
            # 解析AI响应
            print("  正在解析AI响应...")
            ai_data = parse_ai_response(ai_response)
            
            if not ai_data:
                print("  ✗ AI响应解析失败")
                fail_count += 1
                time.sleep(1)
                continue
            
            # 显示补全的信息
            print("  ✓ AI补全信息:")
            if 'efficacy' in ai_data:
                print(f"    功效: {ai_data['efficacy'][:50]}...")
            if 'season' in ai_data:
                print(f"    季节: {ai_data['season']}")
            if 'constitutionType' in ai_data:
                print(f"    体质: {ai_data['constitutionType']}")
            if 'cookingTime' in ai_data:
                print(f"    制作时间: {ai_data['cookingTime']}分钟")
            if 'servings' in ai_data:
                print(f"    适宜人数: {ai_data['servings']}人份")
            if 'steps' in ai_data:
                print(f"    制作步骤: {len(ai_data['steps'])}步")
            
            # 更新数据库
            print("  正在更新数据库...")
            if update_recipe(conn, recipe_id, ai_data, update_all):
                print("  ✓ 更新成功")
                success_count += 1
            else:
                print("  ✗ 更新失败或无需更新")
                fail_count += 1
            
            print()
            time.sleep(2)  # 避免API请求过快
        
        # 统计结果
        print("=" * 60)
        print(f"处理完成！")
        print(f"成功: {success_count} 条")
        print(f"失败: {fail_count} 条")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("✓ 数据库连接已关闭")


if __name__ == '__main__':
    main()

