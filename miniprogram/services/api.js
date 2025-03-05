// API服务
const app = getApp();

// 基础请求函数
const request = (url, method, data) => {
  return new Promise((resolve, reject) => {
    // 显示加载中
    wx.showLoading({
      title: '加载中',
      mask: true
    });
    
    // 获取存储的token (如果有)
    const adminInfo = wx.getStorageSync('adminInfo');
    const header = {
      'content-type': 'application/json'
    };
    
    // 如果是管理员接口，添加token
    if (adminInfo && adminInfo.token && url.includes('/api/admin/')) {
      header['Authorization'] = `Bearer ${adminInfo.token}`;
    }
    
    wx.request({
      url: `${app.globalData.baseUrl}${url}`,
      method: method,
      data: data,
      header: header,
      success: (res) => {
        wx.hideLoading();
        if (res.data.code === 0) {
          resolve(res.data.data);
        } else {
          // 如果是未授权错误，且是管理员接口，清除管理员信息
          if (res.data.code === 401 && url.includes('/api/admin/')) {
            wx.removeStorageSync('adminInfo');
            app.globalData.adminInfo = null;
            
            // 跳转到管理员登录页
            wx.navigateTo({
              url: '/pages/admin/login/index'
            });
          }
          
          wx.showToast({
            title: res.data.errorMsg || '请求失败',
            icon: 'none',
            duration: 2000
          });
          reject(res.data);
        }
      },
      fail: (err) => {
        wx.hideLoading();
        wx.showToast({
          title: '网络错误',
          icon: 'none',
          duration: 2000
        });
        reject(err);
      }
    });
  });
};

// 活动相关API
const activityApi = {
  // 获取活动列表
  getActivities: (params) => {
    return request('/api/activities', 'GET', params);
  },
  // 获取活动详情
  getActivityById: (id) => {
    return request(`/api/activities/${id}`, 'GET');
  },
  // 创建活动
  createActivity: (data) => {
    return request('/api/admin/activities', 'POST', data);
  },
  // 更新活动
  updateActivity: (id, data) => {
    return request(`/api/admin/activities/${id}`, 'PUT', data);
  },
  // 删除活动
  deleteActivity: (id) => {
    return request(`/api/admin/activities/${id}`, 'DELETE');
  },
  // 获取活动的房间列表
  getActivityRooms: (activityId, params) => {
    return request(`/api/activities/${activityId}/rooms`, 'GET', params);
  }
};

// 房间相关API
const roomApi = {
  // 获取房间列表
  getRooms: (params) => {
    return request('/api/rooms', 'GET', params);
  },
  // 获取房间详情
  getRoomById: (id) => {
    return request(`/api/rooms/${id}`, 'GET');
  },
  // 创建房间
  createRoom: (data) => {
    return request('/api/admin/rooms', 'POST', data);
  },
  // 更新房间
  updateRoom: (id, data) => {
    return request(`/api/admin/rooms/${id}`, 'PUT', data);
  },
  // 删除房间
  deleteRoom: (id) => {
    return request(`/api/admin/rooms/${id}`, 'DELETE');
  },
  // 抢购房间
  grabRoom: (id, data) => {
    return request(`/api/rooms/${id}/grab`, 'POST', data);
  },
  // 批量导入房间
  batchImportRooms: (data) => {
    return request('/api/admin/rooms/batch_import', 'POST', data);
  }
};

// 房间类型相关API
const roomTypeApi = {
  // 获取房间类型列表
  getRoomTypes: (params) => {
    return request('/api/room_types', 'GET', params);
  },
  // 获取房间类型详情
  getRoomTypeById: (id) => {
    return request(`/api/room_types/${id}`, 'GET');
  },
  // 创建房间类型
  createRoomType: (data) => {
    return request('/api/admin/room_types', 'POST', data);
  },
  // 更新房间类型
  updateRoomType: (id, data) => {
    return request(`/api/admin/room_types/${id}`, 'PUT', data);
  },
  // 删除房间类型
  deleteRoomType: (id) => {
    return request(`/api/admin/room_types/${id}`, 'DELETE');
  }
};

// 抢购记录相关API
const grabApi = {
  // 获取抢购记录列表
  getGrabRecords: (params) => {
    return request('/api/grabs', 'GET', params);
  },
  // 获取抢购记录详情
  getGrabRecordById: (id) => {
    return request(`/api/grabs/${id}`, 'GET');
  },
  // 确认购买
  confirmGrab: (id, data) => {
    return request(`/api/grabs/${id}/confirm`, 'POST', data);
  },
  // 取消抢购
  cancelGrab: (id, data) => {
    return request(`/api/grabs/${id}/cancel`, 'POST', data);
  },
  // 管理员获取所有抢购记录
  getAdminGrabRecords: (params) => {
    return request('/api/admin/grabs', 'GET', params);
  },
  // 管理员更新抢购记录状态
  updateGrabStatus: (id, data) => {
    return request(`/api/admin/grabs/${id}/status`, 'PUT', data);
  }
};

// 用户相关API
const userApi = {
  // 用户登录/注册
  login: (data) => {
    return request('/api/users/login', 'POST', data);
  },
  // 管理员登录
  adminLogin: (data) => {
    return request('/api/admin/login', 'POST', data);
  },
  // 获取用户信息
  getUserProfile: (params) => {
    return request('/api/users/profile', 'GET', params);
  },
  // 更新用户信息
  updateUserProfile: (data) => {
    return request('/api/users/profile', 'PUT', data);
  },
  // 获取用户统计信息
  getUserStats: () => {
    return request('/api/users/stats', 'GET');
  },
  // 管理员获取用户列表
  getAdminUsers: (params) => {
    return request('/api/admin/users', 'GET', params);
  }
};

// 系统相关API
const systemApi = {
  // 获取系统配置
  getConfig: () => {
    return request('/api/system/config', 'GET');
  },
  // 更新系统配置
  updateConfig: (data) => {
    return request('/api/admin/system/config', 'PUT', data);
  },
  // 获取系统日志
  getLogs: (params) => {
    return request('/api/admin/system/logs', 'GET', params);
  },
  // 获取系统统计数据
  getStats: (params) => {
    return request('/api/admin/system/stats', 'GET', params);
  }
};

// 文件上传API
const uploadApi = {
  // 上传图片
  uploadImage: (filePath) => {
    return new Promise((resolve, reject) => {
      wx.showLoading({
        title: '上传中',
        mask: true
      });
      
      wx.uploadFile({
        url: `${app.globalData.baseUrl}/api/upload/image`,
        filePath: filePath,
        name: 'file',
        success: (res) => {
          wx.hideLoading();
          const data = JSON.parse(res.data);
          if (data.code === 0) {
            resolve(data.data);
          } else {
            wx.showToast({
              title: data.errorMsg || '上传失败',
              icon: 'none',
              duration: 2000
            });
            reject(data);
          }
        },
        fail: (err) => {
          wx.hideLoading();
          wx.showToast({
            title: '上传失败',
            icon: 'none',
            duration: 2000
          });
          reject(err);
        }
      });
    });
  }
};

module.exports = {
  activityApi,
  roomApi,
  roomTypeApi,
  grabApi,
  userApi,
  systemApi,
  uploadApi
};
