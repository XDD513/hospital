import request from './request'

/**
 * 查询排班列表（管理员用）
 */
export function getScheduleList(params) {
  return request({
    url: '/schedule/list',
    method: 'get',
    params
  })
}

/**
 * 查询医生某天的排班
 */
export function getDoctorScheduleByDate(doctorId, date) {
  return request({
    url: `/schedule/doctor/${doctorId}/date/${date}`,
    method: 'get'
  })
}

/**
 * 查询医生某月的排班
 */
export function getDoctorScheduleByMonth(doctorId, month) {
  return request({
    url: `/schedule/doctor/${doctorId}`,
    method: 'get',
    params: { month }
  })
}

/**
 * 查询医生所有排班（别名）
 */
export const getDoctorSchedules = getDoctorScheduleByMonth

/**
 * 添加排班
 */
export function createSchedule(data) {
  return request({
    url: '/schedule/create',
    method: 'post',
    data
  })
}

/**
 * 添加排班（别名）
 */
export const addSchedule = createSchedule

/**
 * 批量创建排班（多个医生、日期范围、多个时段）
 */
export function createSchedulesBatch(data) {
  return request({
    url: '/schedule/batch/create',
    method: 'post',
    data
  })
}

/**
 * 更新排班
 */
export function updateSchedule(data) {
  return request({
    url: '/schedule/update',
    method: 'put',
    data
  })
}

/**
 * 删除排班
 */
export function deleteSchedule(id) {
  return request({
    url: `/schedule/${id}`,
    method: 'delete'
  })
}

// 刷新缓存功能已迁移到 /api/cache.js
// 请使用: import { refreshScheduleCache } from '@/api/cache'