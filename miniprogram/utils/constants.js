// 活动状态
const ActivityStatus = {
  NOT_STARTED: 'NOT_STARTED',
  IN_PROGRESS: 'IN_PROGRESS',
  ENDED: 'ENDED'
};

// 房间状态
const RoomStatus = {
  AVAILABLE: 'AVAILABLE',
  GRABBED: 'GRABBED',
  SOLD: 'SOLD'
};

// 抢购状态
const GrabStatus = {
  GRABBED: 'GRABBED',
  CONFIRMED: 'CONFIRMED',
  CANCELLED: 'CANCELLED'
};

// 用户角色
const UserRole = {
  USER: 'USER',
  ADMIN: 'ADMIN',
  SUPER_ADMIN: 'SUPER_ADMIN'
};

// 支付方式
const PaymentMethod = {
  CASH: 'CASH',
  WECHAT: 'WECHAT',
  ALIPAY: 'ALIPAY',
  BANK_TRANSFER: 'BANK_TRANSFER'
};

// 房间类型
const RoomType = {
  APARTMENT: 'APARTMENT',
  VILLA: 'VILLA',
  PENTHOUSE: 'PENTHOUSE',
  STUDIO: 'STUDIO',
  DUPLEX: 'DUPLEX'
};

// 房间朝向
const RoomOrientation = {
  EAST: 'EAST',
  SOUTH: 'SOUTH',
  WEST: 'WEST',
  NORTH: 'NORTH',
  SOUTHEAST: 'SOUTHEAST',
  SOUTHWEST: 'SOUTHWEST',
  NORTHEAST: 'NORTHEAST',
  NORTHWEST: 'NORTHWEST'
};

// 页面路径
const PagePath = {
  INDEX: '/pages/index/index',
  ACTIVITY_DETAIL: '/pages/activity/detail/index',
  ROOM_DETAIL: '/pages/room/detail/index',
  USER_GRABS: '/pages/user/grabs/index',
  ADMIN_LOGIN: '/pages/admin/login/index',
  ADMIN_ACTIVITIES: '/pages/admin/activities/index',
  ADMIN_ROOMS: '/pages/admin/rooms/index'
};

// API错误码
const ErrorCode = {
  SUCCESS: 0,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500
};

// 本地存储键
const StorageKey = {
  USER_INFO: 'userInfo',
  ADMIN_INFO: 'adminInfo',
  LOGS: 'logs'
};

module.exports = {
  ActivityStatus,
  RoomStatus,
  GrabStatus,
  UserRole,
  PaymentMethod,
  RoomType,
  RoomOrientation,
  PagePath,
  ErrorCode,
  StorageKey
};
