#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补全ingredient.sql文件中空字段的脚本
使用AI自动补全缺失的信息（性味、归经、功效等）
"""

import re
import requests
import time
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ingredient_completion.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ========== 配置项（可根据需要修改） ==========
@dataclass
class Config:
    """配置类"""
    # AI API配置
    deepseek_api_url: str = "https://api.deepseek.com/v1/chat/completions"
    deepseek_api_key: str = "sk-d578be5b1e7245ecb313400e8f893735"
    deepseek_model: str = "deepseek-chat"
    
    # 文件路径配置
    input_sql_path: str = "hospital-appointment-system/sql/ingredient.sql"
    output_sql_path: str = "hospital-appointment-system/sql/ingredient_completed.sql"
    
    # 请求配置
    max_retries: int = 3
    request_interval: int = 2  # API请求间隔（秒）
    timeout: int = 30  # 请求超时时间（秒）
    
    # 字段配置
    required_fields: List[str] = None
    constitution_options: List[str] = None
    
    def __post_init__(self):
        """初始化默认值"""
        if self.required_fields is None:
            self.required_fields = [
                'properties', 'flavor', 'meridian', 'efficacy',
                'suitable_constitution', 'unsuitable_constitution'
            ]
        
        if self.constitution_options is None:
            self.constitution_options = [
                'PINGHE', 'QIXU', 'YANGXU', 'YINXU', 'TANSHI',
                'SHIRE', 'XUEYU', 'QIYU', 'TEBING'
            ]

# 初始化配置
config = Config()

# ========== AI API调用 ==========
def call_ai_api(prompt: str) -> Optional[str]:
    """
    调用DeepSeek AI API
    :param prompt: 提示词
    :return: AI返回的内容
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.deepseek_api_key}'
    }
    
    data = {
        'model': config.deepseek_model,
        'messages': [
            {
                'role': 'system',
                'content': '''你是一位专业的中医药材专家，擅长根据食材信息补全详细的性味、归经、功效等信息。
要求：
1. 严格按照用户指定的格式返回JSON数据
2. 性味只能选择：寒、凉、平、温、热（仅选一个）
3. 味道只能用：甘、辛、酸、苦、咸（可多个，顿号分隔）
4. 归经使用中医标准经络名称（可多个，顿号分隔）
5. 功效说明简洁明了，20-50字
6. 体质类型严格使用指定代码，多个用逗号分隔'''
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0.7,
        'max_tokens': 1500,
        'top_p': 0.95
    }
    
    for attempt in range(config.max_retries):
        try:
            logger.debug(f"AI API请求（尝试{attempt+1}/{config.max_retries}）: {prompt[:50]}...")
            response = requests.post(
                config.deepseek_api_url,
                headers=headers,
                json=data,
                timeout=config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                logger.debug(f"AI API响应: {content[:100]}...")
                return content
            else:
                logger.error(f"API返回格式异常: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API调用失败 (尝试 {attempt + 1}/{config.max_retries}): {str(e)}"
            logger.error(error_msg)
            if attempt < config.max_retries - 1:
                sleep_time = config.request_interval * (attempt + 1)
                logger.info(f"等待{sleep_time}秒后重试...")
                time.sleep(sleep_time)
            else:
                return None
        except Exception as e:
            logger.error(f"API调用未知错误: {str(e)}", exc_info=True)
            return None
    
    return None


def parse_ai_response(response: str) -> Dict[str, Any]:
    """
    解析AI返回的JSON数据
    :param response: AI返回的原始内容
    :return: 解析后的字典
    """
    try:
        # 去除首尾空白
        response = response.strip()
        
        # 处理代码块格式
        if '```json' in response:
            # 提取JSON代码块
            response = response.split('```json')[1].split('```')[0].strip()
        elif '```' in response:
            # 处理没有指定json类型的代码块
            parts = response.split('```')
            for part in parts:
                part_clean = part.strip()
                if part_clean.startswith('{') and part_clean.endswith('}'):
                    response = part_clean
                    break
        
        # 提取JSON部分（处理可能包含的多余文字）
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            logger.error(f"未找到有效的JSON数据: {response[:100]}...")
            return {}
        
        json_str = response[start_idx:end_idx + 1]
        
        # 使用json.loads更安全（替换eval）
        parsed_data = json.loads(json_str)
        logger.debug(f"成功解析JSON: {parsed_data}")
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {str(e)}")
        if 'json_str' in locals():
            logger.error(f"原始JSON字符串: {json_str[:200]}...")
        else:
            logger.error(f"原始响应: {response[:200]}...")
        return {}
    except Exception as e:
        logger.error(f"解析AI响应失败: {str(e)}", exc_info=True)
        logger.error(f"原始响应: {response[:200]}...")
        return {}


# ========== 食材数据处理 ==========
def enrich_ingredient_with_ai(name: str, category: str, existing_data: Dict[str, str]) -> Dict[str, Any]:
    """
    使用AI补全食材的空字段
    :param name: 食材名称
    :param category: 食材分类
    :param existing_data: 已有的数据
    :return: 补全的字段字典
    """
    # 构建现有信息描述
    existing_info = []
    field_mapping = {
        'properties': '性味',
        'flavor': '味道',
        'meridian': '归经',
        'efficacy': '功效',
        'suitable_constitution': '适宜体质',
        'unsuitable_constitution': '不宜体质'
    }
    
    for field, label in field_mapping.items():
        value = existing_data.get(field)
        if value and value not in ['NULL', '', None]:
            existing_info.append(f"{label}：{value}")
    
    existing_text = "，".join(existing_info) if existing_info else "无"
    
    # 找出需要补全的字段
    missing_fields = []
    for field in config.required_fields:
        value = existing_data.get(field)
        if not value or value == 'NULL' or value.strip() == '':
            missing_fields.append(field)
    
    if not missing_fields:
        return {}
    
    # 构建体质选项说明
    constitution_desc = ", ".join(config.constitution_options)
    
    # 构建提示词
    prompt = f"""请根据以下食材信息，补全缺失的字段。请严格按照要求返回JSON格式，只包含需要补全的字段：

### 食材基本信息
名称：{name}
分类：{category or '未分类'}
现有信息：{existing_text}

### 需要补全的字段
{', '.join(missing_fields)}

### 字段填写要求
1. properties（性味）：只能选择一个值，可选值：寒、凉、平、温、热
2. flavor（味道）：可选择多个，用顿号分隔，可选值：甘、辛、酸、苦、咸
3. meridian（归经）：中医标准经络名称，多个用顿号分隔（如：脾、胃、肺）
4. efficacy（功效）：20-50字，简洁明了描述主要功效
5. suitableConstitution（适宜体质）：使用英文代码，多个用逗号分隔，可选值：{constitution_desc}
6. unsuitableConstitution（不宜体质）：使用英文代码，多个用逗号分隔，无则留空字符串

### 输出格式要求
- **只返回需要补全的字段**，已有有效数据的字段不要返回
- 严格使用JSON格式，不要包含任何额外说明文字
- 字段名严格按照上述指定（如suitableConstitution首字母大写，unsuitableConstitution首字母大写）
- 字符串值不要包含多余的空格和特殊字符
- 如果unsuitableConstitution（不宜体质）确实没有，可以返回空字符串""

### 示例输出（仅供格式参考）
{{
    "properties": "温",
    "flavor": "甘、辛",
    "meridian": "脾、胃",
    "efficacy": "温中益气，健脾和胃，适合日常滋补",
    "suitableConstitution": "QIXU,YANGXU",
    "unsuitableConstitution": "YINXU,SHIRE"
}}"""
    
    # 调用AI并解析结果
    ai_response = call_ai_api(prompt)
    if not ai_response:
        logger.warning(f"食材[{name}]AI调用失败")
        return {}
    
    logger.debug(f"食材[{name}]AI原始响应: {ai_response[:200]}...")
    ai_data = parse_ai_response(ai_response)
    logger.debug(f"食材[{name}]AI解析结果: {ai_data}")
    
    # 字段名映射（AI返回的驼峰命名 -> 数据库的下划线命名）
    field_mapping = {
        'suitableConstitution': 'suitable_constitution',
        'unsuitableConstitution': 'unsuitable_constitution'
    }
    
    # 验证AI返回的字段有效性
    valid_data = {}
    for field, value in ai_data.items():
        # 转换为数据库字段名
        db_field = field_mapping.get(field, field)
        
        # 检查是否需要补全此字段
        if db_field not in missing_fields:
            continue
            
        # 验证字段值
        if db_field == 'properties' and value in ['寒', '凉', '平', '温', '热']:
            valid_data[db_field] = value
        elif db_field == 'flavor':
            # 验证味道是否符合要求
            flavors = [f.strip() for f in value.split('、') if f.strip()]
            valid_flavors = [f for f in flavors if f in ['甘', '辛', '酸', '苦', '咸']]
            if valid_flavors:
                valid_data[db_field] = '、'.join(valid_flavors)
        elif db_field == 'meridian':
            # 简单验证归经格式（实际可根据中医标准经络列表进行严格验证）
            meridians = [m.strip() for m in value.split('、') if m.strip()]
            if meridians:
                valid_data[db_field] = '、'.join(meridians)
        elif db_field == 'efficacy':
            # 验证功效长度（放宽限制，允许10-100字）
            efficacy = value.strip()
            if 10 <= len(efficacy) <= 100:
                valid_data[db_field] = efficacy
            else:
                logger.warning(f"食材[{name}]功效长度不符合要求（{len(efficacy)}字）: {efficacy}")
        elif db_field == 'suitable_constitution' or db_field == 'unsuitable_constitution':
            # 验证体质代码
            if isinstance(value, str):
                value_clean = value.strip()
                if value_clean == '':
                    # 空字符串是有效的（表示没有不宜体质）
                    valid_data[db_field] = ''
                else:
                    constitutions = [c.strip() for c in value_clean.split(',') if c.strip()]
                    valid_constitutions = [c for c in constitutions if c in config.constitution_options]
                    if valid_constitutions:
                        valid_data[db_field] = ','.join(valid_constitutions)
                    else:
                        logger.warning(f"食材[{name}]字段[{db_field}]包含无效体质代码: {constitutions}")
                        valid_data[db_field] = ''
            else:
                valid_data[db_field] = ''
    
    return valid_data


# ========== SQL解析与生成 ==========
def parse_sql_insert(line: str) -> Optional[Tuple[int, Dict[str, str]]]:
    """
    解析INSERT语句，返回(id, 字段字典)
    :param line: SQL语句行
    :return: 解析结果
    """
    # 匹配 INSERT INTO `ingredient` VALUES (...) 或 INSERT INTO ingredient VALUES (...)
    pattern = r"INSERT\s+INTO\s+`?ingredient`?\s+VALUES\s*\((.+?)\);"
    match = re.search(pattern, line, re.IGNORECASE)
    if not match:
        return None
    
    values_str = match.group(1)
    
    # 分割值（考虑引号内的逗号，处理转义字符）
    values = []
    current = ""
    in_quotes = False
    quote_char = None
    escape_mode = False
    
    for char in values_str:
        if escape_mode:
            current += char
            escape_mode = False
            continue
            
        if char == '\\':
            current += char
            escape_mode = True
            continue
            
        if char in ["'", '"'] and not in_quotes:
            in_quotes = True
            quote_char = char
            current += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            current += char
        elif char == ',' and not in_quotes:
            values.append(current.strip())
            current = ""
        else:
            current += char
    
    if current:
        values.append(current.strip())
    
    # 检查字段数量（原表应该有13个字段）
    if len(values) < 13:
        logger.warning(f"字段数量异常（{len(values)}个）: {line[:100]}...")
        return None
    
    # 解析字段
    try:
        ingredient_id = int(values[0])
        
        # 清理值（去除引号和处理NULL）
        def clean_value(v: str) -> Optional[str]:
            v = v.strip()
            if v.upper() == 'NULL':
                return None
            # 去除首尾引号
            if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
                return v[1:-1].replace("''", "'").replace('""', '"')
            return v
        
        data = {
            'id': str(ingredient_id),
            'name': clean_value(values[1]),
            'category': clean_value(values[2]),
            'properties': clean_value(values[3]),
            'flavor': clean_value(values[4]),
            'meridian': clean_value(values[5]),
            'efficacy': clean_value(values[6]),
            'suitable_constitution': clean_value(values[7]) or '',
            'unsuitable_constitution': clean_value(values[8]) or '',
            'image': clean_value(values[9]),
            'status': clean_value(values[10]),
            'created_at': clean_value(values[11]),
            'updated_at': clean_value(values[12])
        }
        
        return (ingredient_id, data)
        
    except Exception as e:
        logger.error(f"解析SQL语句失败: {str(e)}", exc_info=True)
        logger.error(f"SQL语句: {line[:100]}...")
        return None


def format_sql_value(value: Optional[Union[str, int]]) -> str:
    """
    格式化SQL值
    :param value: 原始值
    :return: 格式化后的SQL值
    """
    if value is None or value == '' or str(value).upper() == 'NULL':
        return 'NULL'
    
    # 转义单引号
    value_str = str(value).replace("'", "''")
    
    # 处理特殊字符
    value_str = value_str.replace("\\", "\\\\")
    
    return f"'{value_str}'"


def format_sql_insert(ingredient_id: int, data: Dict[str, str]) -> str:
    """
    格式化INSERT语句
    :param ingredient_id: 食材ID
    :param data: 食材数据
    :return: 格式化后的SQL语句
    """
    values = [
        str(ingredient_id),
        format_sql_value(data.get('name')),
        format_sql_value(data.get('category')),
        format_sql_value(data.get('properties')),
        format_sql_value(data.get('flavor')),
        format_sql_value(data.get('meridian')),
        format_sql_value(data.get('efficacy')),
        format_sql_value(data.get('suitable_constitution')),
        format_sql_value(data.get('unsuitable_constitution')),
        format_sql_value(data.get('image')),
        format_sql_value(data.get('status')),
        format_sql_value(data.get('created_at')),
        format_sql_value(data.get('updated_at'))
    ]
    
    return f"INSERT INTO `ingredient` VALUES ({', '.join(values)});"


# ========== 辅助函数 ==========
def check_file_exists(file_path: str) -> bool:
    """
    检查文件是否存在
    :param file_path: 文件路径
    :return: 是否存在
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"文件不存在: {file_path}")
        return False
    if not path.is_file():
        logger.error(f"不是文件: {file_path}")
        return False
    return True


def backup_original_file(file_path: str) -> bool:
    """
    备份原始文件
    :param file_path: 原始文件路径
    :return: 备份是否成功
    """
    try:
        backup_path = f"{file_path}.backup.{time.strftime('%Y%m%d%H%M%S')}"
        with open(file_path, 'r', encoding='utf-8') as f_in, \
             open(backup_path, 'w', encoding='utf-8') as f_out:
            f_out.write(f_in.read())
        logger.info(f"原始文件已备份到: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"备份文件失败: {str(e)}", exc_info=True)
        return False


# ========== 主函数 ==========
def main():
    """主函数"""
    print("=" * 60)
    print("补全ingredient.sql空字段脚本")
    print("=" * 60)
    print()
    
    # 检查配置
    logger.info("开始执行脚本...")
    
    # 检查输入文件
    print(f"[步骤1] 检查输入文件: {config.input_sql_path}")
    if not check_file_exists(config.input_sql_path):
        print("  ✗ 输入文件不存在或无效")
        return
    print("  ✓ 文件存在且有效")
    
    # 备份原始文件
    print(f"\n[步骤2] 备份原始文件...")
    if backup_original_file(config.input_sql_path):
        print("  ✓ 备份成功")
    else:
        print("  ! 备份失败，是否继续？(Y/n): ", end='')
        choice = input().strip().lower()
        if choice == 'n':
            print("  操作已取消")
            return
    
    # 读取文件
    print(f"\n[步骤3] 读取SQL文件...")
    try:
        with open(config.input_sql_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"  ✓ 读取成功，共 {len(lines)} 行")
    except Exception as e:
        print(f"  ✗ 读取文件失败: {str(e)}")
        logger.error(f"读取文件失败: {str(e)}", exc_info=True)
        return
    
    # 解析INSERT语句
    print(f"\n[步骤4] 解析INSERT语句...")
    ingredients = []
    non_insert_lines = []  # 非INSERT语句（用于保留文件结构）
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            non_insert_lines.append(line)
            continue
            
        parsed = parse_sql_insert(line)
        if parsed:
            ingredients.append(parsed)
        else:
            non_insert_lines.append(line)
    
    print(f"  ✓ 解析完成")
    print(f"    - 总记录数: {len(ingredients)}")
    print(f"    - 非INSERT语句数: {len(non_insert_lines)}")
    
    # 找出需要补全的记录
    print(f"\n[步骤5] 检查需要补全的记录...")
    need_complete = []
    
    for ingredient_id, data in ingredients:
        missing_fields = []
        for field in config.required_fields:
            value = data.get(field)
            if not value or value == 'NULL' or value.strip() == '':
                missing_fields.append(field)
        
        if missing_fields:
            need_complete.append((ingredient_id, data, missing_fields))
    
    if not need_complete:
        print("  ✓ 所有记录字段都已完整，无需补全")
        return
    
    print(f"  ✓ 发现 {len(need_complete)} 条记录需要补全")
    # 显示前10条需要补全的记录
    display_count = min(10, len(need_complete))
    for i in range(display_count):
        ingredient_id, data, missing = need_complete[i]
        print(f"    - ID {ingredient_id}: {data['name']} (缺失: {', '.join(missing)})")
    if len(need_complete) > 10:
        print(f"    ... 还有 {len(need_complete) - 10} 条记录需要补全")
    
    # 确认是否继续
    print()
    try:
        choice = input(f"是否使用AI补全这 {len(need_complete)} 条记录？(Y/n，默认Y): ").strip().lower()
        if choice == 'n':
            print("  操作已取消")
            return
    except KeyboardInterrupt:
        print("\n  操作已取消")
        return
    except:
        print("  输入异常，默认继续...")
    
    # 使用AI补全
    print(f"\n[步骤6] 使用AI补全缺失字段...")
    print("=" * 60)
    completed_count = 0
    failed_count = 0
    skipped_count = 0
    
    # 用于保存补全结果的字典
    ingredient_dict = {ing_id: data.copy() for ing_id, data in ingredients}
    
    for idx, (ingredient_id, data, missing_fields) in enumerate(need_complete, 1):
        name = data['name']
        category = data['category'] or '未分类'
        
        print(f"\n[{idx:3d}/{len(need_complete)}] 处理: {name:10s} (ID: {ingredient_id})")
        print(f"  分类: {category}")
        print(f"  缺失字段: {', '.join(missing_fields)}")
        
        try:
            # 调用AI补全
            ai_data = enrich_ingredient_with_ai(name, category, data)
            
            if ai_data:
                # 更新数据
                updated_fields = []
                for field, value in ai_data.items():
                    if field in missing_fields:
                        # 对于unsuitable_constitution，空字符串也是有效值
                        if value or (field == 'unsuitable_constitution' and value == ''):
                            ingredient_dict[ingredient_id][field] = value
                            display_value = value if len(str(value)) <= 30 else str(value)[:30] + '...'
                            updated_fields.append(f"{field}='{display_value}'")
                
                if updated_fields:
                    print(f"  ✓ 补全成功: {', '.join(updated_fields)}")
                    logger.info(f"食材[{name}]补全成功: {list(ai_data.keys())}")
                    completed_count += 1
                else:
                    print(f"  ! 未获取到有效补全数据")
                    logger.warning(f"食材[{name}]AI返回了数据但未匹配到缺失字段: {list(ai_data.keys())}, 缺失字段: {missing_fields}")
                    skipped_count += 1
            else:
                print(f"  ✗ 补全失败（AI未返回有效数据）")
                logger.warning(f"食材[{name}]AI未返回有效数据")
                failed_count += 1
                
        except Exception as e:
            print(f"  ✗ 处理异常: {str(e)}")
            logger.error(f"处理食材[{name}]异常: {str(e)}", exc_info=True)
            failed_count += 1
        
        # 进度显示
        progress = (idx / len(need_complete)) * 100
        print(f"  进度: {progress:5.1f}%", end='')
        
        # 避免API请求过快（最后一条不等待）
        if idx < len(need_complete):
            sleep_time = config.request_interval
            print(f" (等待{sleep_time}秒)...", end='', flush=True)
            time.sleep(sleep_time)
            print()
        else:
            print()
    
    print("\n" + "=" * 60)
    print(f"补全处理统计:")
    print(f"  成功补全: {completed_count:3d} 条")
    print(f"  补全失败: {failed_count:3d} 条")
    print(f"  跳过（无有效数据）: {skipped_count:3d} 条")
    print("=" * 60)
    
    # 生成新的SQL文件
    print(f"\n[步骤7] 生成新的SQL文件...")
    try:
        # 创建输出目录（如果不存在）
        output_path = Path(config.output_sql_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config.output_sql_path, 'w', encoding='utf-8') as f:
            # 写入文件头（非INSERT语句）
            for line in non_insert_lines:
                f.write(line)
            
            # 写入更新后的INSERT语句（按ID排序）
            print(f"  写入 {len(ingredient_dict)} 条记录...")
            for ingredient_id in sorted(ingredient_dict.keys()):
                data = ingredient_dict[ingredient_id]
                sql_line = format_sql_insert(ingredient_id, data)
                f.write(sql_line + '\n')
            
            # 写入文件尾
            f.write('\n-- 补全时间: ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write('SET FOREIGN_KEY_CHECKS = 1;\n')
        
        print(f"  ✓ 新文件生成成功: {config.output_sql_path}")
        
        # 验证文件大小
        file_size = output_path.stat().st_size
        print(f"  ✓ 文件大小: {file_size:,} 字节")
        
    except Exception as e:
        print(f"  ✗ 生成文件失败: {str(e)}")
        logger.error(f"生成SQL文件失败: {str(e)}", exc_info=True)
        return
    
    # 最终统计
    print("\n" + "=" * 60)
    print("补全任务完成！")
    print("=" * 60)
    print(f"📊 统计结果:")
    print(f"   原始记录总数: {len(ingredients)}")
    print(f"   需要补全记录: {len(need_complete)}")
    print(f"   成功补全记录: {completed_count}")
    print(f"   补全成功率: {completed_count/len(need_complete)*100:.1f}%" if need_complete else "100%")
    print(f"\n📁 输出文件: {config.output_sql_path}")
    print(f"📄 日志文件: ingredient_completion.log")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  脚本被用户中断，已退出。")
    except Exception as e:
        print(f"\n\n  脚本执行异常: {str(e)}")
        logger.error(f"脚本执行异常: {str(e)}", exc_info=True)
    finally:
        input("\n  按回车键退出...")