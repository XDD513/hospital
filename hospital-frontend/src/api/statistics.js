import request from './request'

/**
 * 管理员统计数据API
 */

// 获取管理员统计数据
export function getAdminStats() {
  return request({
    url: '/statistics/admin',
    method: 'get'
  })
}

// 获取最近预约列表
export function getRecentAppointments() {
  return request({
    url: '/statistics/recent-appointments',
    method: 'get'
  })
}

// 获取月度统计
export function getMonthlyStats() {
  return request({
    url: '/statistics/monthly',
    method: 'get'
  })
}

// 获取科室统计
export function getDepartmentStats() {
  return request({
    url: '/statistics/department',
    method: 'get'
  })
}

// 获取医生统计
export function getDoctorStats() {
  return request({
    url: '/statistics/doctor',
    method: 'get'
  })
}

// 获取预约趋势数据
export function getAppointmentTrend(dateRange) {
  return request({
    url: '/statistics/appointment-trend',
    method: 'get',
    params: dateRange
  })
}

/**
 * 医生统计数据API
 */

// 获取医生今日统计
export function getDoctorTodayStats(doctorId) {
  return request({
    url: `/statistics/doctor/${doctorId}/today`,
    method: 'get'
  })
}

// 获取医生评价统计
export function getDoctorReviewStats(doctorId) {
  return request({
    url: `/statistics/doctor/${doctorId}/reviews`,
    method: 'get'
  })
}

/**
 * 患者统计数据API
 */

// 获取患者统计数据
export function getPatientStats() {
  return request({
    url: '/statistics/patient',
    method: 'get'
  })
}

// 获取患者最近预约
export function getPatientRecentAppointments() {
  return request({
    url: '/statistics/patient/recent-appointments',
    method: 'get'
  })
}
