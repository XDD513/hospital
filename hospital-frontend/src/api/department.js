import request from './request'

/**
 * 查询所有科室列表
 */
export function getDepartmentList() {
  return request({
    url: '/department/list',
    method: 'get'
  })
}

/**
 * 查询启用状态的科室列表
 */
export function getEnabledDepartmentList() {
  return request({
    url: '/department/list/enabled',
    method: 'get'
  })
}

/**
 * 查询科室分类列表（全部）
 */
export function getDepartmentCategoryList() {
  return request({
    url: '/department/category/list',
    method: 'get'
  })
}

/**
 * 查询启用科室分类列表
 */
export function getEnabledDepartmentCategoryList() {
  return request({
    url: '/department/category/list/enabled',
    method: 'get'
  })
}

/**
 * 按分类查询启用状态的科室列表
 */
export function getEnabledDepartmentListByCategory(categoryId) {
  return request({
    url: `/department/list/by-category/${categoryId}`,
    method: 'get'
  })
}

/**
 * 查询科室详情
 */
export function getDepartmentById(id) {
  return request({
    url: `/department/${id}`,
    method: 'get'
  })
}

/**
 * 添加科室
 */
export function addDepartment(data) {
  return request({
    url: '/department/add',
    method: 'post',
    data
  })
}

/**
 * 更新科室
 */
export function updateDepartment(data) {
  return request({
    url: '/department/update',
    method: 'put',
    data
  })
}

/**
 * 删除科室
 */
export function deleteDepartment(id) {
  return request({
    url: `/department/${id}`,
    method: 'delete'
  })
}

/**
 * 检查科室代码是否存在
 */
export function checkDeptCode(deptCode) {
  return request({
    url: '/department/check/code',
    method: 'get',
    params: { deptCode }
  })
}

/**
 * 更新科室状态
 */
export function updateDepartmentStatus(id, status) {
  return request({
    url: `/department/${id}/status`,
    method: 'put',
    data: { status }
  })
}

// 刷新缓存功能已迁移到 /api/cache.js
// 请使用: import { refreshDepartmentCache } from '@/api/cache'


