<template>
  <view class="container">
    <view class="login-card">
      <text class="title">用户管理系统</text>
      
      <uni-forms ref="form" :model="form" :rules="rules">
        <uni-forms-item name="email">
          <uni-easyinput v-model="form.email" placeholder="邮箱" prefixIcon="mail" />
        </uni-forms-item>
        <uni-forms-item name="password">
          <uni-easyinput v-model="form.password" type="password" placeholder="密码" prefixIcon="locked" />
        </uni-forms-item>
      </uni-forms>
      
      <button class="btn-primary" :loading="loading" @click="handleLogin">登 录</button>
      <button class="btn-outline" @click="goRegister">去注册</button>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)
const form = reactive({ email: '', password: '' })

const rules = {
  email: { rules: [{ required: true, errorMessage: '请输入邮箱' }] },
  password: { rules: [{ required: true, errorMessage: '请输入密码' }] }
}

async function handleLogin() {
  loading.value = true
  try {
    await authStore.login(form)
    uni.showToast({ title: '登录成功' })
    uni.switchTab({ url: '/pages/list/list' })
  } catch (e) {
    // 错误已在拦截器处理
  } finally {
    loading.value = false
  }
}

function goRegister() {
  uni.navigateTo({ url: '/pages/register/register' })
}
</script>

<style>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30rpx;
}
.login-card {
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
.btn-primary {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
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