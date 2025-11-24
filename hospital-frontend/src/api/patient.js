import request from './request'

/**
 * 患者管理API
 */

// 获取今日患者列表（医生端使用）
export function getTodayPatients(doctorId) {
  return request({
    url: `/patient/doctor/${doctorId}/today`,
    method: 'get'
  })
}

// 获取历史患者列表（医生端使用）
export function getHistoryPatients(doctorId, params) {
  return request({
    url: `/patient/doctor/${doctorId}/history`,
    method: 'get',
    params
  })
}

// 获取待接诊患者列表
export function getTodayPendingPatients(doctorId) {
  return request({
    url: `/patient/doctor/${doctorId}/pending`,
    method: 'get'
  })
}

// 获取已接诊患者列表
export function getTodayCompletedPatients(doctorId) {
  return request({
    url: `/patient/doctor/${doctorId}/completed`,
    method: 'get'
  })
}

// 获取所有患者列表（管理员端使用）
export function getPatientList(params) {
  return request({
    url: '/patient/list',
    method: 'get',
    params
  })
}

// 获取患者详情
export function getPatientById(id) {
  return request({
    url: `/patient/${id}`,
    method: 'get'
  })
}

// 添加患者
export function addPatient(data) {
  return request({
    url: '/patient/add',
    method: 'post',
    data
  })
}

// 更新患者信息
export function updatePatient(data) {
  return request({
    url: '/patient/update',
    method: 'put',
    data
  })
}

// 删除患者
export function deletePatient(id) {
  return request({
    url: `/patient/${id}`,
    method: 'delete'
  })
}
