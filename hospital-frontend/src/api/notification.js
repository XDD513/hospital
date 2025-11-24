import request from './request'

/**
 * 获取用户通知列表
 */
export function getNotifications(params = {}) {
  return request({
    url: '/patient/notifications',
    method: 'get',
    params
  })
}

/**
 * 获取未读通知
 */
export function getUnreadNotifications(limit = 5) {
  return request({
    url: '/patient/notifications/unread',
    method: 'get',
    params: { limit }
  })
}

/**
 * 标记通知为已读
 */
export function markNotificationAsRead(id) {
  return request({
    url: `/patient/notifications/${id}/read`,
    method: 'put'
  })
}

/**
 * 批量标记通知为已读
 */
export function markAllNotificationsAsRead(ids) {
  return request({
    url: '/patient/notifications/read-all',
    method: 'put',
    data: { ids }
  })
}

