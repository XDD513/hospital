"""
体质测试API自动提交脚本（批量预约号版）
直接调用后端API提交测试答案，支持批量处理多个预约号

使用前需要安装依赖：
pip install requests

使用方法：
python auto_submit_test_api.py
"""

import requests
import random
import json
from datetime import datetime

class ConstitutionTestAPI:
    def __init__(self, base_url="http://localhost:8080"):
        """
        初始化API客户端

        Args:
            base_url: 后端API基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.questions = None  # 缓存问卷题目（避免重复请求）

    def login(self, username, password):
        """
        登录获取token

        Args:
            username: 用户名（手机号）
            password: 密码
        """
        url = f"{self.base_url}/api/user/login"
        data = {
            "username": username,
            "password": password
        }

        print(f"\n{'='*60}")
        print(f"正在登录: {username}")
        print(f"{'='*60}")
        response = self.session.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.token = result.get("data", {}).get("token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                print("✅ 登录成功！")
                return True
            else:
                print(f"❌ 登录失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 登录请求失败: {response.status_code}")
            return False

    def logout(self):
        """
        退出登录，清除Redis缓存

        Returns:
            bool: 退出登录是否成功
        """
        if not self.token:
            print("⚠️  未登录，无需退出")
            return True

        url = f"{self.base_url}/api/user/logout"
        
        print(f"\n{'='*60}")
        print("正在退出登录...")
        print(f"{'='*60}")
        response = self.session.post(url)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                print("✅ 退出登录成功！")
                # 清除token和请求头
                self.token = None
                self.session.headers.pop("Authorization", None)
                return True
            else:
                print(f"⚠️  退出登录失败: {result.get('message')}")
                return False
        else:
            print(f"⚠️  退出登录请求失败: {response.status_code}")
            return False

    def get_questionnaire(self):
        """获取问卷题目（缓存机制，避免重复请求）"""
        if self.questions:
            print(f"✅ 使用缓存的问卷题目（共 {len(self.questions)} 道）")
            return self.questions

        url = f"{self.base_url}/api/constitution/questionnaire"

        print("正在获取问卷题目...")
        response = self.session.get(url)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                self.questions = result.get("data", [])
                print(f"✅ 获取到 {len(self.questions)} 道题目")
                return self.questions
            else:
                print(f"❌ 获取问卷失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 获取问卷请求失败: {response.status_code}")
            return None

    def generate_answers(self, questions, strategy="random"):
        """
        生成答案

        Args:
            questions: 问题列表
            strategy: 答题策略
                - "random": 随机选择
                - "middle": 选择中间选项
                - "healthy": 倾向健康选项（完全不符合/基本不符合）
                - "unhealthy": 倾向不健康选项（用于测试特定体质）

        Returns:
            dict: {问题ID: 选项ID}
        """
        answers = {}

        for question in questions:
            question_id = question.get("id")
            options = question.get("options", [])

            if not options:
                continue

            # 根据策略选择选项
            if strategy == "random":
                selected_option = random.choice(options)
            elif strategy == "middle":
                # 选择中间选项（通常是"不确定"）
                mid_index = len(options) // 2
                selected_option = options[mid_index]
            elif strategy == "healthy":
                # 选择前两个选项（完全不符合/基本不符合）
                selected_option = options[random.randint(0, min(1, len(options) - 1))]
            elif strategy == "unhealthy":
                # 选择后两个选项（基本符合/完全符合）
                selected_option = options[random.randint(max(0, len(options) - 2), len(options) - 1)]
            else:
                selected_option = options[0]

            answers[str(question_id)] = selected_option.get("id")

        return answers

    def submit_test(self, answers, appointment_id=None):
        """
        提交测试

        Args:
            answers: 答案字典 {问题ID: 选项ID}
            appointment_id: 预约ID（可选）

        Returns:
            dict: 测试结果（失败返回None）
        """
        url = f"{self.base_url}/api/constitution/test/submit"

        data = {
            "answers": answers
        }

        if appointment_id:
            data["appointmentId"] = appointment_id

        response = self.session.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                test_result = result.get("data", {})
                # 补充预约ID到结果中
                test_result["appointmentId"] = appointment_id
                return test_result
            else:
                print(f"  ❌ 提交失败: {result.get('message')}")
                return None
        else:
            print(f"  ❌ 提交请求失败: {response.status_code}")
            print(f"  响应内容: {response.text}")
            return None

    def get_latest_result(self):
        """获取最新测试结果"""
        url = f"{self.base_url}/api/constitution/test/latest"

        print("\n正在获取最新测试结果...")
        response = self.session.get(url)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                test_result = result.get("data", {})
                self.print_result(test_result)
                return test_result
            else:
                print(f"❌ 获取结果失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 获取结果请求失败: {response.status_code}")
            return None

    def print_result(self, result):
        """打印单条测试结果"""
        print(f"\n{'='*60}")
        print(f"📊 测试结果（预约ID: {result.get('appointmentId', '无')}）")
        print(f"{'='*60}")
        print(f"测试ID: {result.get('id')}")
        print(f"主要体质: {result.get('primaryConstitutionName')}")

        primary_detail = result.get('primaryConstitutionDetail', {})
        if primary_detail:
            print(f"体质描述: {primary_detail.get('description', '')[:50]}...")  # 截取前50字
            print(f"养生建议: {primary_detail.get('healthAdvice', '')[:50]}...")

        if result.get('secondaryConstitutionName'):
            print(f"\n次要体质: {result.get('secondaryConstitutionName')}")

        print(f"\n测试日期: {result.get('testDate')}")
        print(f"{'='*60}")

    def print_batch_summary(self, total, success_results, failed_ids):
        """打印批量处理汇总"""
        print(f"\n{'='*80}")
        print(f"📋 批量测试汇总")
        print(f"{'='*80}")
        print(f"总预约数: {total}")
        print(f"成功数: {len(success_results)}")
        print(f"失败数: {len(failed_ids)}")
        if failed_ids:
            print(f"失败的预约ID: {','.join(map(str, failed_ids))}")

        # 统计体质分布
        constitution_count = {}
        for result in success_results:
            primary = result.get('primaryConstitutionName', '未知')
            constitution_count[primary] = constitution_count.get(primary, 0) + 1

        print(f"\n体质分布:")
        for constitution, count in constitution_count.items():
            print(f"  {constitution}: {count} 个")
        print(f"{'='*80}")

    def export_results(self, results, filename=None):
        """
        导出批量结果到JSON文件
        """
        if not results:
            print("\n❌ 无结果可导出")
            return

        if not filename:
            # 生成默认文件名（包含时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"体质测试批量结果_{timestamp}.json"

        # 整理导出数据
        export_data = {
            "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(results),
            "results": results
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 结果已导出到文件: {filename}")
        except Exception as e:
            print(f"\n❌ 导出文件失败: {str(e)}")

    def run_batch_test(self, username, password, appointment_ids, strategy="random", export=True):
        """
        运行批量测试流程

        Args:
            username: 用户名
            password: 密码
            appointment_ids: 预约ID列表（如 [1001, 1002, 1003]）
            strategy: 答题策略
            export: 是否导出结果到文件

        Returns:
            tuple: (success_results, failed_ids) 成功结果列表和失败ID列表
        """
        print(f"{'='*80}")
        print(f"开始批量体质测试（共 {len(appointment_ids)} 个预约）")
        print(f"答题策略: {strategy}")
        print(f"{'='*80}")

        # 1. 登录
        if not self.login(username, password):
            return [], appointment_ids

        # 2. 获取问卷题目（缓存）
        questions = self.get_questionnaire()
        if not questions:
            return [], appointment_ids

        success_results = []
        failed_ids = []

        # 3. 循环处理每个预约ID
        for i, appointment_id in enumerate(appointment_ids, 1):
            print(f"\n【{i}/{len(appointment_ids)}】正在处理预约ID: {appointment_id}")

            # 生成答案（每个预约可生成不同答案）
            answers = self.generate_answers(questions, strategy=strategy)
            print(f"  ✅ 生成 {len(answers)} 个答案")

            # 提交测试
            result = self.submit_test(answers, appointment_id=appointment_id)
            if result:
                print(f"  ✅ 提交成功！主要体质: {result.get('primaryConstitutionName')}")
                self.print_result(result)  # 打印详细结果
                success_results.append(result)
            else:
                print(f"  ❌ 预约ID {appointment_id} 处理失败")
                failed_ids.append(appointment_id)

        # 4. 打印汇总
        self.print_batch_summary(len(appointment_ids), success_results, failed_ids)

        # 5. 导出结果
        if export and success_results:
            self.export_results(success_results)

        # 6. 退出登录，清除Redis缓存
        self.logout()

        return success_results, failed_ids

    def run_single_test(self, username, password, strategy="random", appointment_id=None):
        """
        运行单个测试流程（保留原有功能）

        Args:
            username: 用户名
            password: 密码
            strategy: 答题策略
            appointment_id: 预约ID（可选）

        Returns:
            dict: 测试结果（失败返回None）
        """
        print("=" * 60)
        print("开始单个体质测试")
        print("=" * 60)

        # 1. 登录
        if not self.login(username, password):
            return None

        # 2. 获取问卷
        questions = self.get_questionnaire()
        if not questions:
            return None

        # 3. 生成答案
        answers = self.generate_answers(questions, strategy=strategy)
        print(f"✅ 生成了 {len(answers)} 个答案")

        # 4. 提交测试
        result = self.submit_test(answers, appointment_id=appointment_id)
        if result:
            self.print_result(result)
        else:
            result = None

        # 5. 退出登录，清除Redis缓存
        self.logout()

        return result


def main():
    """主函数（支持选择单个/批量测试）"""
    print("=" * 80)
    print("体质测试API自动提交脚本（批量预约号版）")
    print("=" * 80)

    # 1. 基础配置
    base_url = input("请输入后端API地址 (直接回车使用默认 http://localhost:8080): ").strip()
    if not base_url:
        base_url = "http://localhost:8080"

    username = input("请输入用户名（手机号）: ").strip()
    password = input("请输入密码: ").strip()

    # 2. 选择测试模式
    print("\n请选择测试模式:")
    print("1. 单个测试（支持单个预约ID或无预约）")
    print("2. 批量测试（支持多个预约ID）")
    mode_choice = input("请输入选项 (1/2，默认1): ").strip() or "1"

    # 3. 选择答题策略
    print("\n请选择答题策略:")
    print("1. random - 随机选择选项")
    print("2. middle - 总是选择中间选项（不确定）")
    print("3. healthy - 倾向于选择健康选项（完全不符合/基本不符合）")
    print("4. unhealthy - 倾向于选择不健康选项（用于测试特定体质）")
    strategy_choice = input("请输入选项 (1/2/3/4，默认1): ").strip()
    strategy_map = {
        "1": "random",
        "2": "middle",
        "3": "healthy",
        "4": "unhealthy"
    }
    strategy = strategy_map.get(strategy_choice, "random")

    # 4. 执行对应模式
    api = ConstitutionTestAPI(base_url=base_url)
    if mode_choice == "2":
        # 批量测试
        appointment_input = input("\n请输入预约ID列表（用逗号分隔，如 1001,1002,1003）: ").strip()
        if not appointment_input:
            print("❌ 批量测试必须输入预约ID列表！")
            return

        # 解析预约ID列表（处理空格、空值）
        appointment_ids = []
        for item in appointment_input.split(","):
            item = item.strip()
            if item.isdigit():
                appointment_ids.append(int(item))

        if not appointment_ids:
            print("❌ 无效的预约ID列表！请输入数字，用逗号分隔")
            return

        # 询问是否导出结果
        export_choice = input("是否导出结果到JSON文件？(y/n，默认y): ").strip().lower() or "y"
        export = export_choice == "y"

        # 运行批量测试
        api.run_batch_test(username, password, appointment_ids, strategy=strategy, export=export)

    else:
        # 单个测试（保留原有逻辑）
        appointment_id_input = input("请输入预约ID（可选，直接回车跳过）: ").strip()
        appointment_id = int(appointment_id_input) if appointment_id_input else None

        result = api.run_single_test(username, password, strategy=strategy, appointment_id=appointment_id)
        if result:
            print("\n✅ 单个测试完成！")
        else:
            print("\n❌ 单个测试失败！")

    print("\n" + "=" * 80)
    print("脚本执行结束")
    print("=" * 80)


if __name__ == "__main__":
    main()
