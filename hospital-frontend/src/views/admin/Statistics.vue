<template>
  <div class="statistics-container">
    <!-- 概览统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card primary" @click="handleStatClick('total')">
          <div class="stat-icon">
            <el-icon>
              <DataAnalysis />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">本月预约总数</div>
            <div class="stat-value">{{ monthlyStats.totalAppointments }}</div>
            <div class="stat-suffix">次</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card success" @click="handleStatClick('completed')">
          <div class="stat-icon">
            <el-icon>
              <CircleCheck />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">本月完成预约</div>
            <div class="stat-value">{{ monthlyStats.completedAppointments }}</div>
            <div class="stat-suffix">次</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card warning" @click="handleStatClick('cancelled')">
          <div class="stat-icon">
            <el-icon>
              <WarningFilled />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">本月取消预约</div>
            <div class="stat-value">{{ monthlyStats.cancelledAppointments }}</div>
            <div class="stat-suffix">次</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="stat-card danger" @click="handleStatClick('noshow')">
          <div class="stat-icon">
            <el-icon>
              <CircleClose />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">本月爽约数</div>
            <div class="stat-value">{{ monthlyStats.noShowAppointments }}</div>
            <div class="stat-suffix">次</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表统计 -->
    <el-row :gutter="20">
      <!-- 科室预约排行 - 柱状图 -->
      <el-col :xs="24" :md="12">
        <div class="admin-card">
          <div class="card-header">
            <h3>
              <el-icon>
                <TrendCharts />
              </el-icon>
              科室预约排行
            </h3>
            <el-radio-group v-model="deptChartType" size="small" @change="updateDeptChart">
              <el-radio-button label="bar">柱状图</el-radio-button>
              <el-radio-button label="pie">饼图</el-radio-button>
            </el-radio-group>
          </div>
          <div class="card-body">
            <div ref="deptChartRef" style="width: 100%; height: 350px"></div>
          </div>
        </div>
      </el-col>

      <!-- 热门医生排行 - 柱状图 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="never">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h3>医生工作量统计</h3>
              <el-tag type="info" size="small">Top 10</el-tag>
            </div>
          </template>
          <div ref="doctorChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预约状态分布 - 饼图 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :md="12">
        <el-card shadow="never">
          <template #header>
            <h3>本月预约状态分布</h3>
          </template>
          <div ref="statusPieChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>

      <!-- 预约趋势 - 折线图 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <h3>预约趋势统计</h3>
              <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
                end-placeholder="结束日期" size="small" @change="updateTrendChart" />
            </div>
          </template>
          <div ref="trendChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 科室预约热力图 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24">
        <el-card shadow="never">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h3>科室预约热力图</h3>
              <el-tag type="info" size="small">展示各科室在不同时段的预约热度</el-tag>
            </div>
          </template>
          <div ref="departmentHeatmapRef" style="width: 100%; height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 完成率分析 - 仪表盘 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :md="8">
        <el-card shadow="never">
          <template #header>
            <h3>预约完成率</h3>
          </template>
          <div ref="completionGaugeRef" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="8">
        <el-card shadow="never">
          <template #header>
            <h3>医生平均接诊量</h3>
          </template>
          <div ref="avgConsultationGaugeRef" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="8">
        <el-card shadow="never">
          <template #header>
            <h3>患者满意度</h3>
          </template>
          <div ref="satisfactionGaugeRef" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import message from '@/plugins/message'
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'

import { getMonthlyStats, getDepartmentStats, getDoctorStats, getAppointmentTrend } from '@/api/statistics'
import { getAppointmentList } from '@/api/appointment'
import dayjs from 'dayjs'
import * as echarts from 'echarts'

const dateRange = ref([])
const deptChartType = ref('bar')

// 图表实例
const deptChartRef = ref(null)
const doctorChartRef = ref(null)
const statusPieChartRef = ref(null)
const trendChartRef = ref(null)
const completionGaugeRef = ref(null)
const avgConsultationGaugeRef = ref(null)
const satisfactionGaugeRef = ref(null)
const departmentHeatmapRef = ref(null)

let deptChart = null
let doctorChart = null
let statusPieChart = null
let trendChart = null
let completionGauge = null
let avgConsultationGauge = null
let satisfactionGauge = null
let heatmapChart = null

// 月度统计
const monthlyStats = reactive({
  totalAppointments: 0,
  completedAppointments: 0,
  cancelledAppointments: 0,
  noShowAppointments: 0
})

// 科室统计
const deptStats = ref([])

// 医生统计
const doctorStats = ref([])

// 趋势数据
const trendData = ref([])

// 加载月度统计
const loadMonthlyStats = async () => {
  try {
    const res = await getMonthlyStats()
    if (res.code === 200) {
      monthlyStats.totalAppointments = res.data.totalAppointments || 0
      monthlyStats.completedAppointments = res.data.completedAppointments || 0
      monthlyStats.cancelledAppointments = res.data.cancelledAppointments || 0
      monthlyStats.noShowAppointments = res.data.noShowAppointments || 0

      // 数据加载完成后重新初始化相关图表
      nextTick(() => {
        updateStatusPieChart()
        updateCompletionGauge()
        updateAvgConsultationGauge()
        updateSatisfactionGauge()
      })
    }
  } catch (error) {

    message.error('加载月度统计失败')
  }
}

// 加载科室统计
const loadDeptStats = async () => {
  try {
    const res = await getDepartmentStats()
    if (res.code === 200) {
      deptStats.value = res.data || []
      // 数据加载完成后重新初始化图表
      nextTick(() => {
        updateDeptChart()
      })
    }
  } catch (error) {

    message.error('加载科室统计失败')
  }
}

// 加载医生统计
const loadDoctorStats = async () => {
  try {
    const res = await getDoctorStats()
    if (res.code === 200) {
      doctorStats.value = res.data || []
      // 数据加载完成后重新初始化图表
      nextTick(() => {
        updateDoctorChart()
      })
    }
  } catch (error) {

    message.error('加载医生统计失败')
  }
}

// 加载趋势数据
const loadTrendData = async () => {
  try {
    const res = await getAppointmentTrend(dateRange.value)
    if (res.code === 200) {
      trendData.value = res.data || []
      // 数据加载完成后重新初始化图表
      nextTick(() => {
        updateTrendChart()
      })
    }
  } catch (error) {

    message.error('加载趋势数据失败')
  }
}

// 初始化科室图表
const updateDeptChart = () => {
  if (!deptChartRef.value) return
  if (!deptChart) {
    deptChart = echarts.init(deptChartRef.value, null, { useDirtyRect: true })
  }

  const option = deptChartType.value === 'bar' ? {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: deptStats.value.map(d => d.deptName),
      axisLabel: { rotate: 30 }
    },
    yAxis: {
      type: 'value',
      name: '预约数'
    },
    series: [{
      name: '预约数',
      type: 'bar',
      data: deptStats.value.map(d => d.appointmentCount),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#83bff6' },
          { offset: 0.5, color: '#188df0' },
          { offset: 1, color: '#188df0' }
        ])
      },
      barWidth: '60%'
    }]
  } : {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center'
    },
    series: [{
      name: '科室预约',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%'
      },
      data: deptStats.value.map(d => ({
        name: d.deptName,
        value: d.appointmentCount
      }))
    }]
  }

  deptChart.setOption(option)
}

// 初始化医生图表
const updateDoctorChart = () => {
  if (!doctorChartRef.value) return
  if (!doctorChart) {
    doctorChart = echarts.init(doctorChartRef.value, null, { useDirtyRect: true })
  }
  
  // 准备数据，只取前10名
  const topDoctors = doctorStats.value.slice(0, 10)
  const doctorNames = topDoctors.map(d => d.doctorName || '未知医生')
  const appointmentCounts = topDoctors.map(d => d.appointmentCount || 0)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { 
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}<br/>${param.seriesName}: ${param.value} 次`
      }
    },
    legend: {
      data: ['预约数量'],
      top: 10
    },
    grid: {
      left: '15%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: false
    },
    xAxis: {
      type: 'value',
      name: '预约数（次）',
      nameLocation: 'middle',
      nameGap: 30,
      axisLabel: {
        formatter: '{value}'
      }
    },
    yAxis: {
      type: 'category',
      data: doctorNames,
      axisLabel: {
        interval: 0,
        formatter: (value) => {
          return value.length > 6 ? value.substring(0, 6) + '...' : value
        }
      }
    },
    series: [{
      name: '预约数量',
      type: 'bar',
      data: appointmentCounts,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#2af598' },
          { offset: 1, color: '#009efd' }
        ])
      },
      label: {
        show: true,
        position: 'right',
        formatter: '{c}',
        color: '#333'
      },
      barWidth: '60%',
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }

  doctorChart.setOption(option)
}

// 初始化状态饼图
const updateStatusPieChart = () => {
  if (!statusPieChartRef.value) return
  if (!statusPieChart) {
    statusPieChart = echarts.init(statusPieChartRef.value, null, { useDirtyRect: true })
  }
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [{
      name: '预约状态',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {c}次 ({d}%)'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: monthlyStats.completedAppointments, name: '已完成', itemStyle: { color: '#67c23a' } },
        { value: monthlyStats.cancelledAppointments, name: '已取消', itemStyle: { color: '#e6a23c' } },
        { value: monthlyStats.noShowAppointments, name: '爽约', itemStyle: { color: '#f56c6c' } }
      ]
    }]
  }

  statusPieChart.setOption(option)
}

// 初始化趋势图表
const updateTrendChart = () => {
  if (!trendChartRef.value) return
  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value, null, { useDirtyRect: true })
  }

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['总预约', '已完成', '已取消'],
      top: '5%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: trendData.value.map(d => d.date)
    },
    yAxis: {
      type: 'value',
      name: '预约数'
    },
    series: [
      {
        name: '总预约',
        type: 'line',
        smooth: true,
        data: trendData.value.map(d => d.totalCount),
        itemStyle: { color: '#409eff' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
          ])
        }
      },
      {
        name: '已完成',
        type: 'line',
        smooth: true,
        data: trendData.value.map(d => d.completedCount),
        itemStyle: { color: '#67c23a' }
      },
      {
        name: '已取消',
        type: 'line',
        smooth: true,
        data: trendData.value.map(d => d.cancelledCount),
        itemStyle: { color: '#e6a23c' }
      }
    ]
  }

  trendChart.setOption(option)
}

// 初始化完成率仪表盘
const updateCompletionGauge = () => {
  if (!completionGaugeRef.value) return
  if (!completionGauge) {
    completionGauge = echarts.init(completionGaugeRef.value, null, { useDirtyRect: true })
  }

  const completionRate = monthlyStats.totalAppointments > 0 ?
    ((monthlyStats.completedAppointments / monthlyStats.totalAppointments) * 100).toFixed(1) : 0

  const option = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.6, '#f56c6c'],
            [0.8, '#e6a23c'],
            [1, '#67c23a']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'inherit'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'inherit',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'inherit',
          width: 5
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 12,
        distance: -60,
        formatter: (value) => value + '%'
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 16
      },
      detail: {
        fontSize: 30,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: (value) => value + '%',
        color: 'inherit'
      },
      data: [{
        value: completionRate,
        name: '完成率'
      }]
    }]
  }

  completionGauge.setOption(option)
}

// 初始化平均接诊量仪表盘
const updateAvgConsultationGauge = () => {
  if (!avgConsultationGaugeRef.value) return
  if (!avgConsultationGauge) {
    avgConsultationGauge = echarts.init(avgConsultationGaugeRef.value, null, { useDirtyRect: true })
  }

  // 计算平均接诊量：本月完成预约数 / 当前日期
  const currentDay = new Date().getDate()
  const avgValue = monthlyStats.totalAppointments > 0 ? Math.round(monthlyStats.totalAppointments / currentDay) : 0

  const option = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 50,
      splitNumber: 5,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.4, '#e6a23c'],
            [0.7, '#409eff'],
            [1, '#67c23a']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'inherit'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'inherit',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'inherit',
          width: 5
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 12,
        distance: -60
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 16
      },
      detail: {
        fontSize: 30,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: (value) => value + '人',
        color: 'inherit'
      },
      data: [{
        value: avgValue,
        name: '日均接诊'
      }]
    }]
  }

  avgConsultationGauge.setOption(option)
}

// 初始化满意度仪表盘
const updateSatisfactionGauge = () => {
  if (!satisfactionGaugeRef.value) return
  if (!satisfactionGauge) {
    satisfactionGauge = echarts.init(satisfactionGaugeRef.value, null, { useDirtyRect: true })
  }

  const option = {
    series: [{
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 5,
      splitNumber: 5,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.6, '#f56c6c'],
            [0.8, '#e6a23c'],
            [1, '#67c23a']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'inherit'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'inherit',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'inherit',
          width: 5
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 12,
        distance: -60,
        formatter: (value) => value.toFixed(1)
      },
      title: {
        offsetCenter: [0, '-20%'],
        fontSize: 16
      },
      detail: {
        fontSize: 30,
        offsetCenter: [0, '0%'],
        valueAnimation: true,
        formatter: (value) => value + '分',
        color: 'inherit'
      },
      data: [{
        value: monthlyStats.totalAppointments > 0 ? (monthlyStats.completedAppointments / monthlyStats.totalAppointments * 5).toFixed(1) : 0,
        name: '平均评分'
      }]
    }]
  }

  satisfactionGauge.setOption(option)
}

// 初始化所有图表
const initCharts = () => {
  nextTick(() => {
    updateDeptChart()
    updateDoctorChart()
    updateStatusPieChart()
    updateTrendChart()
    updateCompletionGauge()
    updateAvgConsultationGauge()
    updateSatisfactionGauge()
  })
}

// 加载科室预约热力图数据
const loadDepartmentHeatmap = async () => {
  try {
    // 获取最近30天的预约数据
    const endDate = dayjs().format('YYYY-MM-DD')
    const startDate = dayjs().subtract(30, 'day').format('YYYY-MM-DD')
    
    const res = await getAppointmentList({
      page: 1,
      pageSize: 10000,
      startDate,
      endDate
    })
    
    if (res.code === 200 && res.data?.records) {
      const appointments = res.data.records
      
      // 获取所有科室
      const deptRes = await getDepartmentStats({})
      const departments = deptRes.data || []
      
      // 定义时段（8:00-18:00，每小时一个时段）
      const timeSlots = []
      for (let hour = 8; hour < 18; hour++) {
        timeSlots.push(`${hour.toString().padStart(2, '0')}:00-${(hour + 1).toString().padStart(2, '0')}:00`)
      }
      
      // 构建热力图数据：科室 × 时段
      const heatmapData = []
      departments.forEach((dept, deptIndex) => {
        timeSlots.forEach((timeSlot, timeIndex) => {
          // 统计该科室在该时段的预约数
          const count = appointments.filter(apt => {
            const aptDept = apt.deptName || apt.categoryName || ''
            const aptTimeSlot = apt.timeSlot || ''
            return aptDept === dept.deptName && aptTimeSlot === timeSlot
          }).length
          
          if (count > 0) {
            heatmapData.push([timeIndex, deptIndex, count])
          }
        })
      })
      
      // 初始化热力图
      await nextTick()
      initDepartmentHeatmap(departments.map(d => d.deptName), timeSlots, heatmapData)
    }
  } catch (error) {
    console.error('加载科室预约热力图数据失败', error)
  }
}

// 初始化科室预约热力图
const initDepartmentHeatmap = (departments, timeSlots, heatmapData) => {
  if (!departmentHeatmapRef.value) return
  
  if (heatmapChart) {
    heatmapChart.dispose()
  }
  
  heatmapChart = echarts.init(departmentHeatmapRef.value)
  
  const option = {
    tooltip: {
      position: 'top',
      formatter: (params) => {
        return `${departments[params.data[1]]}<br/>${timeSlots[params.data[0]]}<br/>预约数: ${params.data[2]}`
      }
    },
    grid: {
      height: '60%',
      top: '10%',
      left: '15%'
    },
    xAxis: {
      type: 'category',
      data: timeSlots,
      splitArea: {
        show: true
      },
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'category',
      data: departments,
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...heatmapData.map(d => d[2]), 1),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#50a3ba', '#eac736', '#d94e5d']
      }
    },
    series: [{
      name: '预约数量',
      type: 'heatmap',
      data: heatmapData,
      label: {
        show: true,
        formatter: (params) => {
          return params.data[2] > 0 ? params.data[2] : ''
        }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  
  heatmapChart.setOption(option)
}

// 窗口大小改变时重新渲染图表
const handleResize = () => {
  deptChart?.resize()
  doctorChart?.resize()
  statusPieChart?.resize()
  trendChart?.resize()
  completionGauge?.resize()
  avgConsultationGauge?.resize()
  satisfactionGauge?.resize()
  heatmapChart?.resize()
}

// 处理统计卡片点击
const handleStatClick = (type) => {
  // 可以在这里添加跳转到详细页面的逻辑
}

onMounted(() => {
  // 加载统计数据
  loadMonthlyStats()
  loadDeptStats()
  loadDoctorStats()
  loadTrendData()
  loadDepartmentHeatmap()

  // 初始化图表
  initCharts()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时销毁图表和移除事件监听
onBeforeUnmount(() => {
  deptChart?.dispose()
  deptChart = null
  doctorChart?.dispose()
  doctorChart = null
  statusPieChart?.dispose()
  statusPieChart = null
  trendChart?.dispose()
  trendChart = null
  completionGauge?.dispose()
  completionGauge = null
  avgConsultationGauge?.dispose()
  avgConsultationGauge = null
  satisfactionGauge?.dispose()
  satisfactionGauge = null
  heatmapChart?.dispose()
  heatmapChart = null
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="scss">
@use '@/styles/admin-variables.scss' as *;
@use '@/styles/admin-common.scss' as *;

.statistics-container {
  max-width: 1400px;
  margin: 0 auto;

  .stats-row {
    margin-bottom: 20px;
  }
}
</style>
