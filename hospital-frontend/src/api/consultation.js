import request from './request'

/**
 * 接诊记录API
 */

// 获取医生接诊记录列表
export function getConsultationRecords(doctorId, params) {
  return request({
    url: `/consultation/doctor/${String(doctorId)}/records`,
    method: 'get',
    params
  })
}

// 获取接诊记录详情
export function getConsultationRecordById(id) {
  return request({
    url: `/consultation/record/${id}`,
    method: 'get'
  })
}

// 创建接诊记录
export function createConsultationRecord(data) {
  return request({
    url: '/consultation/record/create',
    method: 'post',
    data
  })
}

// 更新接诊记录
export function updateConsultationRecord(data) {
  return request({
    url: '/consultation/record/update',
    method: 'put',
    data
  })
}

// 开始接诊
export function startConsultation(appointmentId) {
  return request({
    url: `/consultation/start/${String(appointmentId)}`,
    method: 'post'
  })
}

// 完成接诊
export function completeConsultation(appointmentId, data) {
  return request({
    url: `/consultation/complete/${String(appointmentId)}`,
    method: 'post',
    data
  })
}

// 导出接诊记录
export function exportConsultationRecords(doctorId, params) {
  return request({
    url: `/consultation/doctor/${doctorId}/export`,
    method: 'get',
    params,
    responseType: 'blob'
  })
}
