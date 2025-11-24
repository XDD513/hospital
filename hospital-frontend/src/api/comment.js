import request from './request'

/**
 * 文章评论API接口
 */

/**
 * 获取文章评论列表
 * @param {Object} params - 查询参数
 * @param {number} params.articleId - 文章ID
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getCommentList(params) {
  return request({
    url: '/comment/list',
    method: 'get',
    params
  })
}

/**
 * 发表评论
 * @param {Object} data - 评论数据
 * @param {number} data.articleId - 文章ID
 * @param {number} data.userId - 用户ID
 * @param {string} data.userName - 用户名
 * @param {string} data.content - 评论内容
 * @param {number} data.parentId - 父评论ID（可选，0表示顶级评论）
 */
export function publishComment(data) {
  return request({
    url: '/comment/publish',
    method: 'post',
    data
  })
}

/**
 * 删除评论
 * @param {number} id - 评论ID
 * @param {number} userId - 用户ID
 */
export function deleteComment(id, userId) {
  return request({
    url: `/comment/${id}`,
    method: 'delete',
    params: { userId }
  })
}

/**
 * 点赞评论
 * @param {number} id - 评论ID
 * @param {number} userId - 用户ID
 */
export function likeComment(id, userId) {
  return request({
    url: `/comment/like/${id}`,
    method: 'post',
    params: { userId }
  })
}

/**
 * 取消点赞评论
 * @param {number} id - 评论ID
 * @param {number} userId - 用户ID
 */
export function unlikeComment(id, userId) {
  return request({
    url: `/comment/like/${id}`,
    method: 'delete',
    params: { userId }
  })
}

/**
 * 检查用户是否已点赞评论
 * @param {number} id - 评论ID
 * @param {number} userId - 用户ID
 */
export function checkCommentLikeStatus(id, userId) {
  return request({
    url: `/comment/like/status/${id}`,
    method: 'get',
    params: { userId }
  })
}

