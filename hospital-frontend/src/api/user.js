import request from './request'

/**
 * 用户登录
 */
export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

/**
 * 用户注册
 */
export function register(data) {
  return request({
    url: '/user/register',
    method: 'post',
    data
  })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

/**
 * 检查用户名是否存在
 */
export function checkUsername(username) {
  return request({
    url: '/user/check/username',
    method: 'get',
    params: { username }
  })
}

/**
 * 检查手机号是否存在
 */
export function checkPhone(phone) {
  return request({
    url: '/user/check/phone',
    method: 'get',
    params: { phone }
  })
}

/**
 * 退出登录
 */
export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data) {
  return request({
    url: '/user/info',
    method: 'put',
    data
  })
}

/**
 * 获取用户信息（会返回带签名的头像URL）
 */
export function getUserInfoWithSignedAvatar() {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

/**
 * 修改密码
 */
export function changePassword(data) {
  return request({
    url: '/user/password',
    method: 'put',
    data
  })
}

/**
 * 获取用户设置
 */
export function getUserSettings() {
  return request({
    url: '/user/settings',
    method: 'get'
  })
}

/**
 * 更新用户设置
 */
export function updateUserSettings(data) {
  return request({
    url: '/user/settings',
    method: 'put',
    data
  })
}

/**
 * 获取患者预约统计
 */
export function getPatientAppointmentStats() {
  return request({
    url: '/user/appointment-stats',
    method: 'get'
  })
}


