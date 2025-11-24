import request from './request'

/**
 * 评价管理API
 */

// 获取医生评价列表
export function getDoctorReviews(doctorId, params) {
  return request({
    url: `/review/doctor/${doctorId}`,
    method: 'get',
    params
  })
}

// 获取评价详情
export function getReviewById(id) {
  return request({
    url: `/review/${id}`,
    method: 'get'
  })
}

// 创建评价
export function createReview(data) {
  return request({
    url: '/review/create',
    method: 'post',
    data
  })
}

// 回复评价
export function replyReview(reviewId, data) {
  return request({
    url: `/review/${reviewId}/reply`,
    method: 'post',
    data
  })
}

// 删除评价
export function deleteReview(id) {
  return request({
    url: `/review/${id}`,
    method: 'delete'
  })
}

// 获取所有评价列表（管理员端）
export function getAllReviews(params) {
  return request({
    url: '/review/list',
    method: 'get',
    params
  })
}
