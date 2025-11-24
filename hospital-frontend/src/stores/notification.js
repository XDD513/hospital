import { defineStore } from 'pinia'
import { getUnreadNotifications } from '@/api/notification'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    unread: []
  }),
  actions: {
    async fetchUnread(limit = 5) {
      try {
        const res = await getUnreadNotifications(limit)
        this.unread = Array.isArray(res.data) ? res.data : []
      } catch (error) {

        this.unread = []
      }
    },
    addNotification(notification) {
      if (!notification?.id) return
      const existsIndex = this.unread.findIndex(item => item.id === notification.id)
      if (existsIndex !== -1) {
        this.unread.splice(existsIndex, 1, notification)
      } else {
        this.unread.unshift(notification)
        if (this.unread.length > 20) {
          this.unread.length = 20
        }
      }
    },
    removeNotification(notificationId) {
      this.unread = this.unread.filter(item => item.id !== notificationId)
    },
    setNotifications(list) {
      this.unread = Array.isArray(list) ? list : []
    },
    clear() {
      this.unread = []
    }
  }
})

