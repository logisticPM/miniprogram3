// user/grabs/index.js
const { grabApi } = require('../../../services/api')
const { formatDate, formatGrabStatus, getGrabStatusClass } = require('../../../utils/util')
const app = getApp()

Page({
  data: {
    grabRecords: [],
    loading: true,
    pageNum: 1,
    pageSize: 10,
    hasMore: true,
    refreshing: false
  },

  onLoad() {
    this.loadGrabRecords(true)
  },

  onPullDownRefresh() {
    this.setData({
      refreshing: true,
      pageNum: 1,
      hasMore: true
    })
    this.loadGrabRecords(true)
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadGrabRecords()
    }
  },

  // 加载抢购记录
  loadGrabRecords(reset = false) {
    // 检查是否登录
    if (!app.globalData.openid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      })
      this.setData({ loading: false, refreshing: false })
      wx.stopPullDownRefresh()
      return
    }

    const { pageNum, pageSize } = this.data
    this.setData({ loading: true })

    grabApi.getGrabRecords({
      openid: app.globalData.openid,
      page: pageNum,
      size: pageSize
    }).then(res => {
      // 处理抢购记录数据
      const records = res.data.map(record => {
        return {
          ...record,
          statusText: formatGrabStatus(record.status),
          statusClass: getGrabStatusClass(record.status),
          create_time_text: formatDate(record.create_time),
          confirm_time_text: record.confirm_time ? formatDate(record.confirm_time) : ''
        }
      })

      this.setData({
        grabRecords: reset ? records : [...this.data.grabRecords, ...records],
        loading: false,
        refreshing: false,
        pageNum: pageNum + 1,
        hasMore: records.length === pageSize
      })

      wx.stopPullDownRefresh()
    }).catch(() => {
      this.setData({ 
        loading: false,
        refreshing: false
      })
      wx.stopPullDownRefresh()
      wx.showToast({
        title: '加载抢购记录失败',
        icon: 'none'
      })
    })
  },

  // 查看房间详情
  viewRoomDetail(e) {
    const { roomId } = e.currentTarget.dataset
    if (roomId) {
      wx.navigateTo({
        url: `/pages/room/detail/index?id=${roomId}`
      })
    }
  },

  // 查看活动详情
  viewActivityDetail(e) {
    const { activityId } = e.currentTarget.dataset
    if (activityId) {
      wx.navigateTo({
        url: `/pages/activity/detail/index?id=${activityId}`
      })
    }
  },

  // 确认购买
  confirmGrab(e) {
    const { grabId } = e.currentTarget.dataset
    
    wx.showModal({
      title: '确认购买',
      content: '确认购买后将无法取消，是否继续？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '处理中...',
            mask: true
          })
          
          grabApi.confirmGrab(grabId).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '确认成功',
              icon: 'success'
            })
            
            // 刷新抢购记录
            this.setData({
              pageNum: 1,
              hasMore: true
            })
            this.loadGrabRecords(true)
          }).catch(() => {
            wx.hideLoading()
          })
        }
      }
    })
  },

  // 取消抢购
  cancelGrab(e) {
    const { grabId } = e.currentTarget.dataset
    
    wx.showModal({
      title: '取消抢购',
      content: '确定要取消此次抢购吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '处理中...',
            mask: true
          })
          
          grabApi.cancelGrab(grabId).then(() => {
            wx.hideLoading()
            wx.showToast({
              title: '取消成功',
              icon: 'success'
            })
            
            // 刷新抢购记录
            this.setData({
              pageNum: 1,
              hasMore: true
            })
            this.loadGrabRecords(true)
          }).catch(() => {
            wx.hideLoading()
          })
        }
      }
    })
  }
})
