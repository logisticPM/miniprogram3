// index.js
const { activityApi } = require('../../services/api')
const { formatActivityStatus, getActivityStatusClass } = require('../../utils/util')
const { ActivityStatus } = require('../../utils/constants')

Page({
  data: {
    activities: [],
    loading: true
  },
  
  onLoad() {
    this.loadActivities()
  },
  
  onPullDownRefresh() {
    this.loadActivities(() => {
      wx.stopPullDownRefresh()
    })
  },
  
  // 加载活动列表
  loadActivities(callback) {
    this.setData({ loading: true })
    
    activityApi.getActivities({
      status: ActivityStatus.IN_PROGRESS
    }).then(res => {
      // 处理活动数据
      const activities = res.map(item => {
        return {
          ...item,
          statusText: formatActivityStatus(item.status),
          statusClass: getActivityStatusClass(item.status)
        }
      })
      
      this.setData({
        activities,
        loading: false
      })
      
      if (callback) callback()
    }).catch(() => {
      this.setData({ loading: false })
      if (callback) callback()
    })
  },
  
  // 跳转到活动详情
  goToActivity(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/activity/detail/index?id=${id}`
    })
  },
  
  // 跳转到管理员页面
  goToAdmin() {
    wx.navigateTo({
      url: '/pages/admin/login/index'
    })
  }
})
