// activity/detail/index.js
const { activityApi, roomApi, roomTypeApi } = require('../../../services/api')
const { formatActivityStatus, getActivityStatusClass, formatPrice } = require('../../../utils/util')
const app = getApp()

Page({
  data: {
    activity: null,
    roomTypes: [],
    rooms: [],
    loading: true,
    currentTab: 0,
    tabs: ['房型介绍', '可选房源']
  },
  
  onLoad(options) {
    if (options.id) {
      this.setData({
        activityId: options.id
      })
      this.loadActivityDetail(options.id)
    } else {
      wx.showToast({
        title: '参数错误',
        icon: 'error'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },
  
  // 加载活动详情
  loadActivityDetail(activityId) {
    this.setData({ loading: true })
    
    // 获取活动详情
    activityApi.getActivityById(activityId).then(activity => {
      // 处理活动状态
      activity.statusText = formatActivityStatus(activity.status)
      activity.statusClass = getActivityStatusClass(activity.status)
      
      this.setData({
        activity,
        loading: false
      })
      
      // 加载房型列表
      this.loadRoomTypes(activityId)
      
      // 加载房间列表
      this.loadRooms(activityId)
    }).catch(() => {
      this.setData({ loading: false })
      wx.showToast({
        title: '加载活动详情失败',
        icon: 'none'
      })
    })
  },
  
  // 加载房型列表
  loadRoomTypes(activityId) {
    roomTypeApi.getRoomTypes({
      activity_id: activityId
    }).then(roomTypes => {
      // 处理房型数据
      roomTypes.forEach(item => {
        item.priceText = formatPrice(item.base_price)
      })
      
      this.setData({ roomTypes })
    })
  },
  
  // 加载房间列表
  loadRooms(activityId) {
    roomApi.getRooms({
      activity_id: activityId,
      status: 'AVAILABLE'
    }).then(rooms => {
      // 处理房间数据
      rooms.forEach(item => {
        item.priceText = formatPrice(item.actual_price)
      })
      
      this.setData({ rooms })
    })
  },
  
  // 切换标签页
  switchTab(e) {
    const index = e.currentTarget.dataset.index
    this.setData({
      currentTab: index
    })
  },
  
  // 查看房间详情
  viewRoomDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/room/detail/index?id=${id}`
    })
  },
  
  // 检查活动密码
  checkPassword() {
    const { activity } = this.data
    
    if (!activity.access_password) {
      return true
    }
    
    return new Promise((resolve) => {
      wx.showModal({
        title: '请输入活动密码',
        editable: true,
        placeholderText: '请输入密码',
        success: (res) => {
          if (res.confirm) {
            if (res.content === activity.access_password) {
              resolve(true)
            } else {
              wx.showToast({
                title: '密码错误',
                icon: 'none'
              })
              resolve(false)
            }
          } else {
            resolve(false)
          }
        }
      })
    })
  },
  
  // 抢购房间
  async grabRoom(e) {
    const { id } = e.currentTarget.dataset
    const { activity } = this.data
    
    // 检查是否登录
    if (!app.globalData.openid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      })
      return
    }
    
    // 检查活动密码
    const passwordValid = await this.checkPassword()
    if (!passwordValid) {
      return
    }
    
    // 确认抢购
    wx.showModal({
      title: '确认抢购',
      content: '您确定要抢购该房间吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '抢购中...',
            mask: true
          })
          
          // 调用抢购API
          roomApi.grabRoom(id, {
            openid: app.globalData.openid
          }).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '抢购成功',
              icon: 'success'
            })
            
            // 刷新房间列表
            this.loadRooms(activity.id)
            
            // 跳转到我的抢购记录
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/user/grabs/index'
              })
            }, 1500)
          }).catch(() => {
            wx.hideLoading()
          })
        }
      }
    })
  }
})
