// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 加载管理员信息
    const adminInfo = wx.getStorageSync('adminInfo')
    if (adminInfo) {
      this.globalData.adminInfo = adminInfo
    }

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        if (res.code) {
          // 这里需要根据实际情况调用微信登录接口获取openid
          console.log('登录成功，code:', res.code)
          // 模拟获取openid
          this.globalData.openid = 'test_openid_' + Date.now()
          
          // 登录后台系统
          const { userApi } = require('./services/api')
          userApi.login({
            openid: this.globalData.openid,
            nickname: '微信用户',
            avatar_url: ''
          }).then(res => {
            this.globalData.userInfo = res
            
            // 如果已经授权，获取用户信息
            wx.getSetting({
              success: setting => {
                if (setting.authSetting['scope.userInfo']) {
                  wx.getUserInfo({
                    success: info => {
                      this.globalData.userInfo.nickname = info.userInfo.nickName
                      this.globalData.userInfo.avatar_url = info.userInfo.avatarUrl
                      
                      // 更新用户信息
                      userApi.login({
                        openid: this.globalData.openid,
                        nickname: info.userInfo.nickName,
                        avatar_url: info.userInfo.avatarUrl
                      })
                    }
                  })
                }
              }
            })
          }).catch(err => {
            console.error('登录失败:', err)
          })
        }
      }
    })
  },
  
  globalData: {
    userInfo: null,
    openid: null,
    adminInfo: null,
    baseUrl: 'http://localhost:5000' // 开发环境API地址，生产环境需要替换为实际地址
  }
})
