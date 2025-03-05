// admin/login/index.js
const { userApi } = require('../../../services/api')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },
  
  // 输入用户名
  inputUsername(e) {
    this.setData({
      username: e.detail.value
    })
  },
  
  // 输入密码
  inputPassword(e) {
    this.setData({
      password: e.detail.value
    })
  },
  
  // 管理员登录
  login() {
    const { username, password } = this.data
    
    // 表单验证
    if (!username.trim()) {
      wx.showToast({
        title: '请输入用户名',
        icon: 'none'
      })
      return
    }
    
    if (!password.trim()) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none'
      })
      return
    }
    
    this.setData({ loading: true })
    
    // 调用登录API
    userApi.adminLogin({
      username,
      password
    }).then(res => {
      this.setData({ loading: false })
      
      // 保存管理员信息
      app.globalData.adminInfo = {
        username: username,
        token: res.token,
        isAdmin: true
      }
      
      // 保存到本地存储
      wx.setStorageSync('adminInfo', app.globalData.adminInfo)
      
      wx.showToast({
        title: '登录成功',
        icon: 'success'
      })
      
      // 跳转到管理页面
      setTimeout(() => {
        wx.redirectTo({
          url: '/pages/admin/activities/index'
        })
      }, 1500)
    }).catch(() => {
      this.setData({ loading: false })
    })
  }
})
