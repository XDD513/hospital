import request from './request'

/**
 * 养生文章API接口
 */

/**
 * 获取文章列表（分页）
 * @param {Object} params - 查询参数
 * @param {string} params.category - 分类（可选）
 * @param {string} params.constitutionType - 体质类型（可选）
 * @param {number} params.isRecommend - 是否推荐（可选）
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getArticleList(params) {
  return request({
    url: '/article/list',
    method: 'get',
    params
  })
}

/**
 * 获取文章详情
 * @param {number} id - 文章ID
 */
export function getArticleDetail(id) {
  return request({
    url: `/article/${id}`,
    method: 'get'
  })
}

/**
 * 搜索文章
 * @param {Object} params - 查询参数
 * @param {string} params.keyword - 关键词
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function searchArticles(params) {
  return request({
    url: '/article/search',
    method: 'get',
    params
  })
}

/**
 * 发布文章
 * @param {Object} data - 文章数据
 */
export function publishArticle(data) {
  return request({
    url: '/article/publish',
    method: 'post',
    data
  })
}

/**
 * 更新文章
 * @param {number} id - 文章ID
 * @param {Object} data - 文章数据
 */
export function updateArticle(id, data) {
  return request({
    url: `/article/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function deleteArticle(id, userId) {
  return request({
    url: `/article/${id}`,
    method: 'delete',
    params: { userId }
  })
}

/**
 * 点赞文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function likeArticle(id, userId) {
  return request({
    url: `/article/like/${id}`,
    method: 'post',
    params: { userId }
  })
}

/**
 * 取消点赞文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function unlikeArticle(id, userId) {
  return request({
    url: `/article/like/${id}`,
    method: 'delete',
    params: { userId }
  })
}

/**
 * 收藏文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 * @param {string} remark - 备注（可选）
 */
export function favoriteArticle(id, userId, remark = '') {
  return request({
    url: `/article/favorite/${id}`,
    method: 'post',
    params: { userId, remark }
  })
}

/**
 * 取消收藏文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function unfavoriteArticle(id, userId) {
  return request({
    url: `/article/favorite/${id}`,
    method: 'delete',
    params: { userId }
  })
}

/**
 * 获取用户收藏的文章
 * @param {Object} params - 查询参数
 * @param {number} params.userId - 用户ID
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getFavoriteArticles(params) {
  return request({
    url: '/article/favorites',
    method: 'get',
    params
  })
}

/**
 * 获取用户发布的文章
 * @param {Object} params - 查询参数
 * @param {number} params.userId - 用户ID
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getMyArticles(params) {
  return request({
    url: '/article/my',
    method: 'get',
    params
  })
}

/**
 * 获取推荐文章
 * @param {number} limit - 数量限制
 */
export function getRecommendedArticles(limit = 10) {
  return request({
    url: '/article/recommended',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取热门文章
 * @param {number} limit - 数量限制
 */
export function getPopularArticles(limit = 10) {
  return request({
    url: '/article/popular',
    method: 'get',
    params: { limit }
  })
}

/**
 * 检查用户是否已点赞文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function checkLikeStatus(id, userId) {
  return request({
    url: `/article/like/status/${id}`,
    method: 'get',
    params: { userId }
  })
}

/**
 * 检查用户是否已收藏文章
 * @param {number} id - 文章ID
 * @param {number} userId - 用户ID
 */
export function checkFavoriteStatus(id, userId) {
  return request({
    url: `/article/favorite/status/${id}`,
    method: 'get',
    params: { userId }
  })
}

/**
 * 获取所有标签列表
 */
export function getAllTags() {
  return request({
    url: '/article/tags',
    method: 'get'
  })
}

