// admin/rooms/index.js
const { roomApi, roomTypeApi } = require('../../../services/api')
const { formatRoomStatus, getRoomStatusClass, formatPrice } = require('../../../utils/util')
const app = getApp()

Page({
  data: {
    rooms: [],
    roomTypes: [],
    loading: true,
    refreshing: false,
    isAdmin: false,
    selectedRoomTypeId: '',
    filterStatus: ''
  },
  
  onLoad() {
    this.checkAdminAuth()
  },
  
  onShow() {
    if (this.data.isAdmin) {
      this.loadRoomTypes()
      this.loadRooms()
    }
  },
  
  onPullDownRefresh() {
    this.setData({ refreshing: true })
    this.loadRoomTypes()
    this.loadRooms()
  },
  
  // 检查管理员权限
  checkAdminAuth() {
    const adminInfo = app.globalData.adminInfo || wx.getStorageSync('adminInfo')
    
    if (adminInfo && adminInfo.isAdmin) {
      app.globalData.adminInfo = adminInfo
      this.setData({ isAdmin: true })
      this.loadRoomTypes()
      this.loadRooms()
    } else {
      wx.redirectTo({
        url: '/pages/admin/login/index'
      })
    }
  },
  
  // 加载房间类型列表
  loadRoomTypes() {
    roomTypeApi.getRoomTypes().then(roomTypes => {
      this.setData({ roomTypes })
    }).catch(() => {
      // 处理错误
    })
  },
  
  // 加载房间列表
  loadRooms() {
    this.setData({ loading: true })
    
    const { selectedRoomTypeId, filterStatus } = this.data
    const params = {
      admin: true
    }
    
    if (selectedRoomTypeId) {
      params.room_type_id = selectedRoomTypeId
    }
    
    if (filterStatus) {
      params.status = filterStatus
    }
    
    roomApi.getRooms(params).then(rooms => {
      // 处理房间数据
      const processedRooms = rooms.map(room => {
        return {
          ...room,
          statusText: formatRoomStatus(room.status),
          statusClass: getRoomStatusClass(room.status),
          priceText: formatPrice(room.actual_price)
        }
      })
      
      this.setData({
        rooms: processedRooms,
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
  
  // 筛选房间类型
  filterByRoomType(e) {
    const roomTypeId = e.currentTarget.dataset.id
    this.setData({
      selectedRoomTypeId: roomTypeId === this.data.selectedRoomTypeId ? '' : roomTypeId
    }, () => {
      this.loadRooms()
    })
  },
  
  // 筛选房间状态
  filterByStatus(e) {
    const status = e.currentTarget.dataset.status
    this.setData({
      filterStatus: status === this.data.filterStatus ? '' : status
    }, () => {
      this.loadRooms()
    })
  },
  
  // 创建房间
  createRoom() {
    wx.navigateTo({
      url: '/pages/admin/rooms/create/index'
    })
  },
  
  // 编辑房间
  editRoom(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/admin/rooms/edit/index?id=${id}`
    })
  },
  
  // 查看房间详情
  viewRoom(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/room/detail/index?id=${id}`
    })
  },
  
  // 删除房间
  deleteRoom(e) {
    const { id, number } = e.currentTarget.dataset
    
    wx.showModal({
      title: '删除房间',
      content: `确定要删除房间"${number}"吗？删除后无法恢复。`,
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '删除中...',
            mask: true
          })
          
          roomApi.deleteRoom(id).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
            
            // 刷新房间列表
            this.loadRooms()
          }).catch(() => {
            wx.hideLoading()
          })
        }
      }
    })
  },
  
  // 导航到活动管理
  navigateToActivities() {
    wx.redirectTo({
      url: '/pages/admin/activities/index'
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
