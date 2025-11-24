import request from './request'

/**
 * 药膳推荐相关API
 */

/**
 * 获取全部药膳列表（分页，不包含AI推荐）
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getRecipeList(params) {
  return request({
    url: '/recipe/list',
    method: 'get',
    params: {
      pageNum: params.pageNum || params.page || 1,
      pageSize: params.pageSize || params.size || 10
    }
  })
}

/**
 * 获取药膳详情
 * @param {number} id - 药膳ID
 */
export function getRecipeDetail(id) {
  return request({
    url: `/recipe/${id}`,
    method: 'get'
  })
}

/**
 * 获取个性化推荐药膳（分页）
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码，默认1
 * @param {number} params.pageSize - 每页数量，默认10
 * @param {string} params.season - 季节（可选）
 */
export function getRecommendedRecipes(params = {}) {
  return request({
    url: '/recipe/recommend',
    method: 'get',
    params: {
      pageNum: params.pageNum || 1,
      pageSize: params.pageSize || 10,
      season: params.season
    }
  })
}

/**
 * 获取时令药膳
 * @param {string} season - 季节（SPRING/SUMMER/AUTUMN/WINTER）
 * @param {number} limit - 数量限制
 */
export function getSeasonalRecipes(season, limit = 10) {
  return request({
    url: `/recipe/season/${season}`,
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取热门药膳
 * @param {number} limit - 数量限制
 */
export function getPopularRecipes(limit = 10) {
  return request({
    url: '/recipe/popular',
    method: 'get',
    params: { limit }
  })
}

/**
 * 收藏药膳
 * @param {number} recipeId - 药膳ID
 * @param {string} remark - 备注（可选）
 */
export function favoriteRecipe(recipeId, remark = '') {
  return request({
    url: `/recipe/favorite/${recipeId}`,
    method: 'post',
    params: { remark }
  })
}

/**
 * 取消收藏药膳
 * @param {number} recipeId - 药膳ID
 */
export function unfavoriteRecipe(recipeId) {
  return request({
    url: `/recipe/favorite/${recipeId}`,
    method: 'delete'
  })
}

/**
 * 获取用户收藏的药膳列表（分页）
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页数量
 */
export function getFavoriteRecipes(params = {}) {
  return request({
    url: '/recipe/favorites',
    method: 'get',
    params: {
      pageNum: params.pageNum || 1,
      pageSize: params.pageSize || 10
    }
  })
}

/**
 * 查询适用食材
 * @param {string} constitutionType - 体质类型代码
 */
export function getSuitableIngredients(constitutionType) {
  return request({
    url: `/recipe/ingredients/${constitutionType}`,
    method: 'get'
  })
}

/**
 * 搜索药膳
 * @param {Object} params - 搜索参数
 * @param {string} params.keyword - 关键词
 * @param {string} params.season - 季节
 * @param {string} params.constitutionType - 体质类型
 * @param {number} params.page - 页码
 * @param {number} params.size - 每页数量
 */
export function searchRecipes(params) {
  return request({
    url: '/recipe/search',
    method: 'get',
    params
  })
}

