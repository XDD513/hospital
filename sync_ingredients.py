#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步食材数据脚本
从herbal_recipe表的ingredients字段解析食材，与ingredient表对比，补充缺失的食材
"""

import pymysql
import json
import re
import requests
import time
from datetime import datetime
from typing import Set, Dict, List, Optional, Any

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

# 食材分类映射（根据名称推断分类）
CATEGORY_MAP = {
    # 谷物类
    '米': '谷物', '麦': '谷物', '豆': '谷物', '谷': '谷物', '粮': '谷物',
    '小米': '谷物', '大米': '谷物', '黑米': '谷物', '糯米': '谷物', '薏米': '谷物',
    '红豆': '谷物', '绿豆': '谷物', '黑豆': '谷物', '黄豆': '谷物', '燕麦': '谷物',
    
    # 肉类
    '肉': '肉类', '鸡': '肉类', '鸭': '肉类', '鹅': '肉类', '牛': '肉类',
    '羊': '肉类', '猪': '肉类', '鱼': '肉类', '虾': '肉类', '蟹': '肉类',
    '鸡肉': '肉类', '鸭肉': '肉类', '羊肉': '肉类', '牛肉': '肉类', '猪肉': '肉类',
    '排骨': '肉类', '乌鸡': '肉类', '鸽肉': '肉类', '鲫鱼': '肉类', '鲤鱼': '肉类',
    
    # 蔬菜类
    '菜': '蔬菜', '瓜': '蔬菜', '果': '蔬菜', '萝卜': '蔬菜', '白菜': '蔬菜',
    '山药': '蔬菜', '莲藕': '蔬菜', '冬瓜': '蔬菜', '南瓜': '蔬菜', '韭菜': '蔬菜',
    '雪梨': '蔬菜', '百合': '蔬菜',
    
    # 中药材
    '参': '中药材', '芪': '中药材', '归': '中药材', '苓': '中药材', '术': '中药材',
    '草': '中药材', '枣': '中药材', '杞': '中药材', '耳': '中药材', '花': '中药材',
    '黄芪': '中药材', '党参': '中药材', '当归': '中药材', '茯苓': '中药材', '白术': '中药材',
    '甘草': '中药材', '红枣': '中药材', '枸杞': '中药材', '银耳': '中药材', '红花': '中药材',
    '沙参': '中药材', '麦冬': '中药材', '玉竹': '中药材', '陈皮': '中药材', '决明子': '中药材',
    '乌梅': '中药材', '佛手': '中药材', '菊花': '中药材', '玫瑰花': '中药材', '莲子': '中药材',
    '山楂': '中药材', '黑木耳': '中药材',
    
    # 调料类
    '盐': '调料', '糖': '调料', '油': '调料', '醋': '调料', '酱': '调料',
    '生姜': '调料', '冰糖': '调料', '红糖': '调料', '黄酒': '调料', '食用油': '调料',
    
    # 其他
    '蜂蜜': '其他', '核桃仁': '其他', '虾仁': '其他', '荷叶': '其他'
}


def infer_category(name: str) -> str:
    """根据食材名称推断分类"""
    for keyword, category in CATEGORY_MAP.items():
        if keyword in name:
            return category
    return '其他'


def get_next_id(cursor) -> int:
    """获取下一个可用的ID（使用当前最大ID+1）"""
    cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM ingredient")
    result = cursor.fetchone()
    return result[0] if result else 1


def extract_ingredients_from_recipes(cursor) -> Set[str]:
    """从herbal_recipe表中提取所有食材名称"""
    ingredients_set = set()
    
    try:
        cursor.execute("SELECT ingredients FROM herbal_recipe WHERE ingredients IS NOT NULL AND ingredients != ''")
        rows = cursor.fetchall()
        
        for row in rows:
            ingredients_json = row[0]
            if not ingredients_json:
                continue
            
            try:
                # 解析JSON
                ingredients = json.loads(ingredients_json)
                if isinstance(ingredients, list):
                    for ingredient in ingredients:
                        if isinstance(ingredient, dict) and 'name' in ingredient:
                            name = ingredient['name'].strip()
                            if name:
                                ingredients_set.add(name)
            except json.JSONDecodeError as e:
                print(f"  警告: JSON解析失败: {ingredients_json[:50]}... 错误: {e}")
                continue
    
    except Exception as e:
        print(f"  提取食材失败: {e}")
    
    return ingredients_set


def get_existing_ingredients(cursor) -> Set[str]:
    """获取ingredient表中已存在的食材名称"""
    existing_set = set()
    
    try:
        cursor.execute("SELECT name FROM ingredient")
        rows = cursor.fetchall()
        for row in rows:
            if row[0]:
                existing_set.add(row[0].strip())
    except Exception as e:
        print(f"  查询已有食材失败: {e}")
    
    return existing_set


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
                'content': '你是一位专业的中医药材专家，擅长根据食材名称提供详细的性味、归经、功效等信息。请用中文回答，返回JSON格式的数据。'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7,
        'max_tokens': 1500
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
                print(f"    API返回格式异常: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
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
        print(f"    JSON解析失败: {e}")
        print(f"    原始响应: {response[:200]}...")
        return {}


def enrich_ingredient_with_ai(name: str, category: str) -> Dict[str, any]:
    """使用AI补全食材信息"""
    prompt = f"""请根据以下食材信息，提供详细的中医药性信息。请返回JSON格式，包含以下字段：

食材名称：{name}
分类：{category}

请参考以下示例格式返回JSON（所有字段都必须填写，如果无法确定则使用合理的默认值）：
{{
    "properties": "性味（寒/凉/平/温/热，只能选择一个）",
    "flavor": "味道（甘/辛/酸/苦/咸，可多个用顿号分隔）",
    "meridian": "归经（多个用顿号分隔，如：脾、胃、肺）",
    "efficacy": "功效说明（20-50字，简洁明了）",
    "suitableConstitution": "适宜体质（多个用逗号分隔，如：QIXU,YANGXU，可选值：PINGHE/QIXU/YANGXU/YINXU/TANSHI/SHIRE/XUEYU/QIYU/TEBING）",
    "unsuitableConstitution": "不宜体质（多个用逗号分隔，如：YINXU,SHIRE，如果无则留空字符串）"
}}

注意：
1. 所有文本用中文
2. properties只能选择一个值：寒、凉、平、温、热
3. flavor可以多个，用顿号分隔，如：甘、辛
4. meridian多个用顿号分隔，如：脾、胃、肺
5. efficacy要简洁，20-50字
6. suitableConstitution和unsuitableConstitution使用英文代码，多个用逗号分隔
7. 只返回JSON，不要其他说明文字"""
    
    ai_response = call_ai_api(prompt)
    if not ai_response:
        return {}
    
    return parse_ai_response(ai_response)


def insert_ingredient(cursor, conn, name: str, use_ai: bool = True) -> bool:
    """插入新食材到ingredient表，使用AI补全信息"""
    try:
        # 获取下一个ID
        next_id = get_next_id(cursor)
        
        # 推断分类
        category = infer_category(name)
        
        # 使用AI补全信息
        properties = None
        flavor = None
        meridian = None
        efficacy = None
        suitable_constitution = None
        unsuitable_constitution = None
        
        if use_ai:
            print(f"    正在使用AI补全信息...", end=' ')
            ai_data = enrich_ingredient_with_ai(name, category)
            
            if ai_data:
                properties = ai_data.get('properties')
                flavor = ai_data.get('flavor')
                meridian = ai_data.get('meridian')
                efficacy = ai_data.get('efficacy')
                suitable_constitution = ai_data.get('suitableConstitution') or None
                unsuitable_constitution = ai_data.get('unsuitableConstitution') or None
                
                # 验证和清理数据
                if properties and properties not in ['寒', '凉', '平', '温', '热']:
                    properties = None
                
                print("✓")
            else:
                print("✗ (使用默认值)")
                time.sleep(1)  # 避免API请求过快
        else:
            print(f"    跳过AI补全，使用默认值")
        
        # 构建插入SQL
        sql = """
            INSERT INTO ingredient 
            (id, name, category, properties, flavor, meridian, efficacy, 
             suitable_constitution, unsuitable_constitution, image, status, 
             created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        values = (
            next_id,
            name,
            category,
            properties,
            flavor,
            meridian,
            efficacy,
            suitable_constitution,
            unsuitable_constitution,
            None,  # image
            1,     # status (启用)
            now,   # created_at
            now    # updated_at
        )
        
        cursor.execute(sql, values)
        conn.commit()
        return True
        
    except Exception as e:
        print(f"    插入食材'{name}'失败: {e}")
        conn.rollback()
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("食材数据同步脚本")
    print("=" * 60)
    print()
    
    # 连接数据库
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ 数据库连接成功")
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return
    
    try:
        # 步骤1: 从herbal_recipe表提取所有食材名称
        print("\n[步骤1] 从herbal_recipe表提取食材名称...")
        recipe_ingredients = extract_ingredients_from_recipes(cursor)
        print(f"  ✓ 从药膳表中提取到 {len(recipe_ingredients)} 种食材")
        
        if not recipe_ingredients:
            print("  没有找到任何食材，退出")
            return
        
        # 步骤2: 查询ingredient表中已存在的食材
        print("\n[步骤2] 查询ingredient表中已存在的食材...")
        existing_ingredients = get_existing_ingredients(cursor)
        print(f"  ✓ ingredient表中已有 {len(existing_ingredients)} 种食材")
        
        # 步骤3: 找出缺失的食材
        print("\n[步骤3] 对比并找出缺失的食材...")
        missing_ingredients = recipe_ingredients - existing_ingredients
        
        if not missing_ingredients:
            print("  ✓ 所有食材都已存在，无需添加")
            return
        
        print(f"  ✓ 发现 {len(missing_ingredients)} 种缺失的食材:")
        for name in sorted(missing_ingredients):
            category = infer_category(name)
            print(f"    - {name} (分类: {category})")
        
        # 步骤4: 询问是否继续
        print()
        try:
            choice = input(f"是否添加这 {len(missing_ingredients)} 种食材到ingredient表？(y/N): ").strip().lower()
            if choice != 'y':
                print("  操作已取消")
                return
        except:
            print("  操作已取消")
            return
        
        # 步骤4: 询问是否使用AI补全
        print()
        use_ai = True
        try:
            choice = input("是否使用AI自动补全食材详细信息（性味、归经、功效等）？(Y/n): ").strip().lower()
            use_ai = choice != 'n'
        except:
            pass
        
        # 步骤5: 插入缺失的食材
        print(f"\n[步骤5] 开始添加缺失的食材...")
        success_count = 0
        fail_count = 0
        
        for idx, name in enumerate(sorted(missing_ingredients), 1):
            print(f"  [{idx}/{len(missing_ingredients)}] 正在添加: {name}...")
            if insert_ingredient(cursor, conn, name, use_ai):
                print(f"    ✓ 添加成功")
                success_count += 1
            else:
                print(f"    ✗ 添加失败")
                fail_count += 1
            
            # 避免API请求过快
            if use_ai and idx < len(missing_ingredients):
                time.sleep(2)
        
        # 统计结果
        print("\n" + "=" * 60)
        print("同步完成！")
        print(f"成功添加: {success_count} 种食材")
        print(f"添加失败: {fail_count} 种食材")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 处理过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()
        print("\n✓ 数据库连接已关闭")


if __name__ == '__main__':
    main()

