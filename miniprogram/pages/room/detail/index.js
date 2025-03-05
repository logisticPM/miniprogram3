// room/detail/index.js
const { roomApi } = require('../../../services/api')
const { formatRoomStatus, getRoomStatusClass, formatPrice } = require('../../../utils/util')
const app = getApp()

Page({
  data: {
    room: null,
    loading: true,
    currentImageIndex: 0
  },
  
  onLoad(options) {
    if (options.id) {
      this.loadRoomDetail(options.id)
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
  
  // 加载房间详情
  loadRoomDetail(roomId) {
    this.setData({ loading: true })
    
    roomApi.getRoomById(roomId).then(room => {
      // 处理房间状态
      room.statusText = formatRoomStatus(room.status)
      room.statusClass = getRoomStatusClass(room.status)
      room.priceText = formatPrice(room.actual_price)
      
      // 处理房间类型
      if (room.room_type) {
        room.room_type.priceText = formatPrice(room.room_type.base_price)
      }
      
      this.setData({
        room,
        loading: false
      })
    }).catch(() => {
      this.setData({ loading: false })
      wx.showToast({
        title: '加载房间详情失败',
        icon: 'none'
      })
    })
  },
  
  // 切换图片
  changeImage(e) {
    this.setData({
      currentImageIndex: e.currentTarget.dataset.index
    })
  },
  
  // 预览图片
  previewImage(e) {
    const { room } = this.data
    if (!room.image_urls || room.image_urls.length === 0) {
      return
    }
    
    wx.previewImage({
      current: room.image_urls[this.data.currentImageIndex],
      urls: room.image_urls
    })
  },
  
  // 抢购房间
  grabRoom() {
    const { room } = this.data
    
    // 检查是否登录
    if (!app.globalData.openid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      })
      return
    }
    
    // 检查房间状态
    if (room.status !== 'AVAILABLE') {
      wx.showToast({
        title: '该房间已被抢购或已售出',
        icon: 'none'
      })
      return
    }
    
    // 确认抢购
    wx.showModal({
      title: '确认抢购',
      content: `您确定要抢购${room.room_number}房间吗？`,
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '抢购中...',
            mask: true
          })
          
          // 调用抢购API
          roomApi.grabRoom(room.id, {
            openid: app.globalData.openid
          }).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '抢购成功',
              icon: 'success'
            })
            
            // 刷新房间详情
            this.loadRoomDetail(room.id)
            
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
