import request from './request'

/**
 * 查询所有医生列表
 */
export function getDoctorList() {
  return request({
    url: '/doctor/list',
    method: 'get'
  })
}

/**
 * 查询在职医生列表
 */
export function getEnabledDoctorList() {
  return request({
    url: '/doctor/list/enabled',
    method: 'get'
  })
}

/**
 * 按科室查询医生列表
 */
export function getDoctorListByDept(deptId) {
  return request({
    url: `/doctor/list/dept/${deptId}`,
    method: 'get'
  })
}

/**
 * 查询医生详情
 */
export function getDoctorById(id) {
  return request({
    url: `/doctor/${id}`,
    method: 'get'
  })
}

/**
 * 搜索医生
 */
export function searchDoctors(params) {
  return request({
    url: '/doctor/search',
    method: 'get',
    params
  })
}

/**
 * 添加医生
 */
export function addDoctor(data) {
  return request({
    url: '/doctor/add',
    method: 'post',
    data
  })
}

/**
 * 更新医生信息
 */
export function updateDoctor(data) {
  return request({
    url: '/doctor/update',
    method: 'put',
    data
  })
}

/**
 * 删除医生
 */
export function deleteDoctor(id) {
  return request({
    url: `/doctor/${id}`,
    method: 'delete'
  })
}

/**
 * 获取当前登录医生的个人信息
 */
export function getDoctorProfile() {
  return request({
    url: '/doctor/profile',
    method: 'get'
  })
}

/**
 * 更新当前登录医生的个人信息
 */
export function updateDoctorProfile(data) {
  return request({
    url: '/doctor/profile',
    method: 'put',
    data
  })
}

/**
 * 更新医生状态
 */
export function updateDoctorStatus(id, status) {
  return request({
    url: `/doctor/${id}/status`,
    method: 'put',
    data: { status }
  })
}

// 刷新缓存功能已迁移到 /api/cache.js
// 请使用: import { refreshDoctorCache } from '@/api/cache'


