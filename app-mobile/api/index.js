import axios from 'axios'

const request = axios.create({
  baseURL: 'http://47.95.200.181/api/v1',
  timeout: 10000
})

request.interceptors.request.use(
  (config) => {
    const token = uni.getStorageSync('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== 200) {
      uni.showToast({ title: res.message || '请求失败', icon: 'none' })
      return Promise.reject(new Error(res.message))
    }
    return res.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      if (status === 401) {
        uni.showToast({ title: '登录已过期', icon: 'none' })
        uni.removeStorageSync('access_token')
        uni.removeStorageSync('user')
        uni.reLaunch({ url: '/pages/login/login' })
      } else if (status === 429) {
        uni.showToast({ title: '请求过于频繁', icon: 'none' })
      } else {
        uni.showToast({ title: data.detail || '服务器错误', icon: 'none' })
      }
    } else {
      uni.showToast({ title: '网络错误', icon: 'none' })
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  getCaptcha: () => request.get('/auth/captcha'),
  login: (data) => request.post('/auth/login', data),
  register: (data) => request.post('/auth/register', data),
}

export const userAPI = {
  getMe: () => request.get('/users/me'),
  getList: (params) => request.get('/users/', { params }),
  create: (data) => request.post('/users/', data),
  update: (id, data) => request.put(`/users/${id}`, data),
  delete: (id) => request.delete(`/users/${id}`),
}