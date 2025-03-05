const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

const formatDate = dateStr => {
  if (!dateStr) return '';
  
  // 如果是字符串，尝试转换为Date对象
  let date;
  if (typeof dateStr === 'string') {
    date = new Date(dateStr);
  } else if (dateStr instanceof Date) {
    date = dateStr;
  } else {
    return '';
  }
  
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  return `${[year, month, day].map(formatNumber).join('-')}`
}

// 格式化活动状态
const formatActivityStatus = status => {
  const statusMap = {
    'NOT_STARTED': '未开始',
    'IN_PROGRESS': '进行中',
    'ENDED': '已结束'
  }
  return statusMap[status] || '未知状态'
}

// 获取活动状态样式类
const getActivityStatusClass = status => {
  const classMap = {
    'NOT_STARTED': 'status-not-started',
    'IN_PROGRESS': 'status-in-progress',
    'ENDED': 'status-ended'
  }
  return classMap[status] || ''
}

// 格式化房间状态
const formatRoomStatus = status => {
  const statusMap = {
    'AVAILABLE': '可抢购',
    'GRABBED': '已抢购',
    'SOLD': '已售出'
  }
  return statusMap[status] || '未知状态'
}

// 获取房间状态样式类
const getRoomStatusClass = status => {
  const classMap = {
    'AVAILABLE': 'status-available',
    'GRABBED': 'status-grabbed',
    'SOLD': 'status-sold'
  }
  return classMap[status] || ''
}

// 格式化抢购状态
const formatGrabStatus = status => {
  const statusMap = {
    'GRABBED': '已抢购',
    'CONFIRMED': '已确认',
    'CANCELLED': '已取消'
  }
  return statusMap[status] || '未知状态'
}

// 获取抢购状态样式类
const getGrabStatusClass = status => {
  const classMap = {
    'GRABBED': 'status-grabbed',
    'CONFIRMED': 'status-confirmed',
    'CANCELLED': 'status-cancelled'
  }
  return classMap[status] || ''
}

// 格式化价格显示（元）
const formatPrice = price => {
  if (price === undefined || price === null) return '¥0.00';
  return `¥${parseFloat(price).toFixed(2)}`
}

// 格式化面积显示（平方米）
const formatArea = area => {
  if (area === undefined || area === null) return '0㎡';
  return `${area}㎡`
}

// 格式化日期时间
const formatDateTime = dateStr => {
  if (!dateStr) return '';
  
  // 如果是字符串，尝试转换为Date对象
  let date;
  if (typeof dateStr === 'string') {
    date = new Date(dateStr);
  } else if (dateStr instanceof Date) {
    date = dateStr;
  } else {
    return '';
  }
  
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()

  return `${[year, month, day].map(formatNumber).join('-')} ${[hour, minute].map(formatNumber).join(':')}`
}

// 格式化房间朝向
const formatOrientation = orientation => {
  const orientationMap = {
    'EAST': '东',
    'SOUTH': '南',
    'WEST': '西',
    'NORTH': '北',
    'SOUTHEAST': '东南',
    'SOUTHWEST': '西南',
    'NORTHEAST': '东北',
    'NORTHWEST': '西北'
  }
  return orientationMap[orientation] || '未知朝向'
}

// 格式化房间类型
const formatRoomType = type => {
  const typeMap = {
    'APARTMENT': '公寓',
    'VILLA': '别墅',
    'PENTHOUSE': '顶层公寓',
    'STUDIO': '单间',
    'DUPLEX': '复式'
  }
  return typeMap[type] || '未知类型'
}

// 格式化支付方式
const formatPaymentMethod = method => {
  const methodMap = {
    'CASH': '现金',
    'WECHAT': '微信支付',
    'ALIPAY': '支付宝',
    'BANK_TRANSFER': '银行转账'
  }
  return methodMap[method] || '未知方式'
}

// 格式化用户角色
const formatUserRole = role => {
  const roleMap = {
    'USER': '用户',
    'ADMIN': '管理员',
    'SUPER_ADMIN': '超级管理员'
  }
  return roleMap[role] || '未知角色'
}

// 计算两个日期之间的天数差
const daysBetween = (startDate, endDate) => {
  // 确保输入是Date对象
  const start = startDate instanceof Date ? startDate : new Date(startDate);
  const end = endDate instanceof Date ? endDate : new Date(endDate);
  
  // 计算天数差
  const diffTime = Math.abs(end - start);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return diffDays;
}

// 检查日期是否在范围内
const isDateInRange = (date, startDate, endDate) => {
  // 确保输入是Date对象
  const checkDate = date instanceof Date ? date : new Date(date);
  const start = startDate instanceof Date ? startDate : new Date(startDate);
  const end = endDate instanceof Date ? endDate : new Date(endDate);
  
  return checkDate >= start && checkDate <= end;
}

// 生成随机字符串
const randomString = (length = 8) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// 深拷贝对象
const deepClone = obj => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime());
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item));
  }
  
  if (obj instanceof Object) {
    const copy = {};
    Object.keys(obj).forEach(key => {
      copy[key] = deepClone(obj[key]);
    });
    return copy;
  }
  
  return obj;
}

// 防抖函数
const debounce = (fn, delay = 300) => {
  let timer = null;
  return function(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  }
}

// 节流函数
const throttle = (fn, interval = 300) => {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      fn.apply(this, args);
    }
  }
}

// 格式化手机号 (123****7890)
const formatPhone = phone => {
  if (!phone || phone.length < 7) return phone;
  return phone.replace(/(\d{3})\d*(\d{4})/, '$1****$2');
}

// 验证手机号
const isValidPhone = phone => {
  return /^1[3-9]\d{9}$/.test(phone);
}

// 验证邮箱
const isValidEmail = email => {
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

module.exports = {
  formatTime,
  formatDate,
  formatDateTime,
  formatActivityStatus,
  getActivityStatusClass,
  formatRoomStatus,
  getRoomStatusClass,
  formatGrabStatus,
  getGrabStatusClass,
  formatPrice,
  formatArea,
  formatOrientation,
  formatRoomType,
  formatPaymentMethod,
  formatUserRole,
  daysBetween,
  isDateInRange,
  randomString,
  deepClone,
  debounce,
  throttle,
  formatPhone,
  isValidPhone,
  isValidEmail
}
