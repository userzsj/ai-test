<template>
  <view class="container">
    <view class="register-card">
      <text class="title">创建账号</text>
      
      <uni-forms ref="form" :model="form" :rules="rules">
        <uni-forms-item name="name">
          <uni-easyinput v-model="form.name" placeholder="姓名" prefixIcon="person" />
        </uni-forms-item>
        <uni-forms-item name="email">
          <uni-easyinput v-model="form.email" placeholder="邮箱" prefixIcon="mail" />
        </uni-forms-item>
        <uni-forms-item name="password">
          <uni-easyinput v-model="form.password" type="password" placeholder="密码" prefixIcon="locked" />
        </uni-forms-item>
        <uni-forms-item name="confirmPassword">
          <uni-easyinput v-model="form.confirmPassword" type="password" placeholder="确认密码" prefixIcon="locked" />
        </uni-forms-item>
        
        <!-- 验证码 -->
        <uni-forms-item name="captcha_text">
          <view class="captcha-row">
            <uni-easyinput v-model="form.captcha_text" placeholder="验证码" style="flex: 1;" />
            <view class="captcha-box" @click="refreshCaptcha">
              <image v-if="captchaImage" :src="captchaImage" mode="aspectFill" class="captcha-img" />
              <text v-else class="captcha-placeholder">点击获取</text>
            </view>
          </view>
        </uni-forms-item>
      </uni-forms>
      
      <button class="btn-primary" :loading="loading" @click="handleRegister">注 册</button>
      <button class="btn-outline" @click="goLogin">已有账号？去登录</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { authAPI } from '@/api'

const loading = ref(false)
const captchaImage = ref('')
const captchaId = ref('')
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  captcha_text: '',
  captcha_id: ''
})

const rules = {
  name: { rules: [{ required: true, errorMessage: '请输入姓名' }] },
  email: { rules: [{ required: true, errorMessage: '请输入邮箱' }] },
  password: { 
    rules: [
      { required: true, errorMessage: '请输入密码' },
      { minLength: 6, errorMessage: '密码至少6位' }
    ] 
  },
  confirmPassword: {
    rules: [
      { required: true, errorMessage: '请确认密码' },
      {
        validateFunction: (rule, value, data, callback) => {
          if (value !== form.password) {
            callback('两次输入的密码不一致')
          }
          return true
        }
      }
    ]
  },
  captcha_text: { rules: [{ required: true, errorMessage: '请输入验证码' }] }
}

async function refreshCaptcha() {
  try {
    const data = await authAPI.getCaptcha()
    captchaImage.value = data.captcha_image
    captchaId.value = data.captcha_id
    form.captcha_id = data.captcha_id
  } catch (e) {
    uni.showToast({ title: '获取验证码失败', icon: 'none' })
  }
}

async function handleRegister() {
  loading.value = true
  try {
    await authAPI.register({
      name: form.name,
      email: form.email,
      password: form.password,
      captcha_id: form.captcha_id,
      captcha_text: form.captcha_text
    })
    uni.showToast({ title: '注册成功！请查收邮件验证邮箱' })
    setTimeout(() => {
      uni.navigateTo({ url: '/pages/login/login' })
    }, 1500)
  } catch (e) {
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}

function goLogin() {
  uni.navigateTo({ url: '/pages/login/login' })
}

onMounted(() => {
  refreshCaptcha()
})
</script>

<style>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30rpx;
}
.register-card {
  width: 100%;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(20px);
  border-radius: 30rpx;
  padding: 60rpx 40rpx;
}
.title {
  display: block;
  text-align: center;
  font-size: 44rpx;
  color: #fff;
  margin-bottom: 60rpx;
  font-weight: bold;
}
.captcha-row {
  display: flex;
  gap: 10rpx;
  width: 100%;
}
.captcha-box {
  width: 180rpx;
  height: 70rpx;
  border-radius: 12rpx;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}
.captcha-img {
  width: 100%;
  height: 100%;
  border-radius: 12rpx;
}
.captcha-placeholder {
  color: rgba(255,255,255,0.8);
  font-size: 24rpx;
}
.btn-primary {
  width: 100%;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: #fff;
  border-radius: 50rpx;
  height: 90rpx;
  line-height: 90rpx;
  font-size: 32rpx;
  margin-top: 40rpx;
}
.btn-outline {
  width: 100%;
  background: transparent;
  color: #fff;
  border: 2rpx solid rgba(255,255,255,0.5);
  border-radius: 50rpx;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 28rpx;
  margin-top: 20rpx;
}
</style>