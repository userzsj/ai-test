import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api/v1',  // 加上 /v1
  timeout: 10000
})

// 请求拦截器：自动注入 Token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误
request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res.data
  },
  (error) => {
    console.error('请求错误:', error)  // 加上这行调试

    if (error.response) {
      const { status, data } = error.response

      if (status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        ElMessage.error(data.message || '邮箱或密码错误')
      } else if (status === 403) {
        ElMessage.error(data.message || '权限不足')
      } else if (status === 429) {
        ElMessage.error('请求过于频繁，请稍后再试')
      } else {
        ElMessage.error(data.message || '服务器错误')
      }
    } else {
      ElMessage.error('网络错误，请检查连接')
    }
    return Promise.reject(error)
  }
)

// ========== 认证接口 ==========
export const authAPI = {
  // 获取验证码
  getCaptcha: () => request.get('/auth/captcha'),
  // 登录
  login: (data) => request.post('/auth/login', data),
  // 注册
  register: (data) => request.post('/auth/register', data),
}

// ========== 用户管理接口 ==========
export const userAPI = {
  // 获取当前用户
  getMe: () => request.get('/users/me'),
  // 获取用户列表（分页 + 搜索）
  getList: (params) => request.get('/users/', { params }),
  // 创建用户
  create: (data) => request.post('/users/', data),
  // 更新用户
  update: (id, data) => request.put(`/users/${id}`, data),
  // 删除用户
  delete: (id) => request.delete(`/users/${id}`),
}

export default request