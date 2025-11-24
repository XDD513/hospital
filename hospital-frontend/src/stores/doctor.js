import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDoctorProfile, updateDoctorProfile } from '@/api/doctor'
import { getDoctorTodayStats } from '@/api/statistics'
import message from '@/plugins/message'

/**
 * 医生端专用Store
 */
export const useDoctorStore = defineStore('doctor', () => {
  // 医生信息
  const doctorInfo = ref(null)
  
  // 今日统计数据
  const todayStats = ref({
    appointments: 0,
    completed: 0,
    pending: 0,
    total: 0
  })
  
  // 加载状态
  const loading = ref(false)

  /**
   * 获取医生信息
   */
  const fetchDoctorInfo = async () => {
    try {
      loading.value = true
      const res = await getDoctorProfile()
      if (res.code === 200) {
        doctorInfo.value = res.data
        return res.data
      } else {
        message.error(res.message || '获取医生信息失败')
        return null
      }
    } catch (error) {

      message.error('获取医生信息失败')
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新医生信息
   */
  const updateInfo = async (data) => {
    try {
      loading.value = true
      const res = await updateDoctorProfile(data)
      if (res.code === 200) {
        message.success('更新成功')
        // 重新获取医生信息
        await fetchDoctorInfo()
        return true
      } else {
        message.error(res.message || '更新失败')
        return false
      }
    } catch (error) {

      message.error('更新失败')
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取今日统计数据
   */
  const fetchTodayStats = async () => {
    if (!doctorInfo.value?.id) {

      return
    }

    try {
      const res = await getDoctorTodayStats(doctorInfo.value.id)
      if (res.code === 200) {
        todayStats.value = res.data || {
          appointments: 0,
          completed: 0,
          pending: 0,
          total: 0
        }
      }
    } catch (error) {

    }
  }

  /**
   * 刷新所有数据
   */
  const refreshAll = async () => {
    await fetchDoctorInfo()
    await fetchTodayStats()
  }

  /**
   * 清空数据
   */
  const clearData = () => {
    doctorInfo.value = null
    todayStats.value = {
      appointments: 0,
      completed: 0,
      pending: 0,
      total: 0
    }
  }

  /**
   * 获取医生ID
   */
  const getDoctorId = () => {
    return doctorInfo.value?.id || null
  }

  return {
    // 状态
    doctorInfo,
    todayStats,
    loading,
    
    // 方法
    fetchDoctorInfo,
    updateInfo,
    fetchTodayStats,
    refreshAll,
    clearData,
    getDoctorId
  }
})

