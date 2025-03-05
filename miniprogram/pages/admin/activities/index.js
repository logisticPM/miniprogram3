// admin/activities/index.js
const { activityApi } = require('../../../services/api')
const { formatActivityStatus, getActivityStatusClass, formatDate } = require('../../../utils/util')
const app = getApp()

Page({
  data: {
    activities: [],
    loading: true,
    refreshing: false,
    isAdmin: false
  },
  
  onLoad() {
    this.checkAdminAuth()
  },
  
  onShow() {
    if (this.data.isAdmin) {
      this.loadActivities()
    }
  },
  
  onPullDownRefresh() {
    this.setData({ refreshing: true })
    this.loadActivities()
  },
  
  // 检查管理员权限
  checkAdminAuth() {
    const adminInfo = app.globalData.adminInfo || wx.getStorageSync('adminInfo')
    
    if (adminInfo && adminInfo.isAdmin) {
      app.globalData.adminInfo = adminInfo
      this.setData({ isAdmin: true })
      this.loadActivities()
    } else {
      wx.redirectTo({
        url: '/pages/admin/login/index'
      })
    }
  },
  
  // 加载活动列表
  loadActivities() {
    this.setData({ loading: true })
    
    activityApi.getActivities({
      admin: true
    }).then(activities => {
      // 处理活动数据
      const processedActivities = activities.map(activity => {
        return {
          ...activity,
          statusText: formatActivityStatus(activity.status),
          statusClass: getActivityStatusClass(activity.status),
          start_time_text: formatDate(activity.start_time),
          end_time_text: formatDate(activity.end_time)
        }
      })
      
      this.setData({
        activities: processedActivities,
        loading: false,
        refreshing: false
      })
      
      wx.stopPullDownRefresh()
    }).catch(() => {
      this.setData({ 
        loading: false,
        refreshing: false
      })
      wx.stopPullDownRefresh()
    })
  },
  
  // 创建活动
  createActivity() {
    wx.navigateTo({
      url: '/pages/admin/activities/create/index'
    })
  },
  
  // 编辑活动
  editActivity(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/admin/activities/edit/index?id=${id}`
    })
  },
  
  // 查看活动详情
  viewActivity(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/activity/detail/index?id=${id}`
    })
  },
  
  // 删除活动
  deleteActivity(e) {
    const { id, name } = e.currentTarget.dataset
    
    wx.showModal({
      title: '删除活动',
      content: `确定要删除活动"${name}"吗？删除后无法恢复。`,
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '删除中...',
            mask: true
          })
          
          activityApi.deleteActivity(id).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
            
            // 刷新活动列表
            this.loadActivities()
          }).catch(() => {
            wx.hideLoading()
          })
        }
      }
    })
  },
  
  // 退出登录
  logout() {
    wx.showModal({
      title: '退出登录',
      content: '确定要退出管理员登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除管理员信息
          app.globalData.adminInfo = null
          wx.removeStorageSync('adminInfo')
          
          // 返回首页
          wx.reLaunch({
            url: '/pages/index/index'
          })
        }
      }
    })
  }
})
