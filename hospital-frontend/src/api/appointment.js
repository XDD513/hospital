import request from './request'

/**
 * 创建预约
 */
export function createAppointment(data) {
  return request({
    url: '/appointment/create',
    method: 'post',
    data
  })
}

/**
 * 取消预约
 */
export function cancelAppointment(id) {
  return request({
    url: `/appointment/cancel/${id}`,
    method: 'post'
  })
}

/**
 * 查询患者预约列表
 */
export function getPatientAppointments() {
  return request({
    url: '/appointment/patient/list',
    method: 'get'
  })
}

/**
 * 导出患者预约列表
 */
export function exportPatientAppointments(params) {
  return request({
    url: '/appointment/patient/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 查询预约详情
 */
export function getAppointmentById(id) {
  return request({
    url: `/appointment/${id}`,
    method: 'get'
  })
}

/**
 * 查询所有预约列表（管理员端）
 */
export function getAppointmentList(params) {
  return request({
    url: '/appointment/list',
    method: 'get',
    params
  })
}

/**
 * 更新预约状态
 */
export function updateAppointmentStatus(id, status) {
  return request({
    url: `/appointment/${id}/status`,
    method: 'put',
    data: { status }
  })
}

/**
 * 删除预约
 */
export function deleteAppointment(id) {
  return request({
    url: `/appointment/${id}`,
    method: 'delete'
  })
}

/**
 * 叫号功能 - 给患者发送广播通知
 */
export function callPatient(appointmentId) {
  return request({
    url: `/appointment/call/${appointmentId}`,
    method: 'post'
  })
}

// 刷新缓存功能已迁移到 /api/cache.js
// 请使用: import { refreshAppointmentCache } from '@/api/cache'