// components/navigation-bar/navigation-bar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    title: {
      type: String,
      value: ''
    },
    back: {
      type: Boolean,
      value: true
    },
    color: {
      type: String,
      value: 'black'
    },
    background: {
      type: String,
      value: '#FFF'
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    statusBarHeight: 0,
    navBarHeight: 44
  },

  lifetimes: {
    attached: function() {
      // 获取状态栏高度
      const systemInfo = wx.getSystemInfoSync();
      this.setData({
        statusBarHeight: systemInfo.statusBarHeight
      });
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {
    // 返回上一页
    navigateBack: function() {
      if (this.properties.back) {
        wx.navigateBack({
          delta: 1
        });
      }
    }
  }
})
