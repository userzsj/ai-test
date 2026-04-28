<template>
  <transition name="lock-fade">
    <div v-if="visible" class="screen-lock" @mousemove="handleActivity">
      <!-- 时间显示 -->
      <div class="lock-time">{{ currentTime }}</div>
      <div class="lock-date">{{ currentDate }}</div>

      <!-- 用户信息 -->
      <div class="lock-user">
        <el-avatar :size="160" class="lock-avatar" :src="authStore.user?.avatar || defaultAvatar">
          {{ user?.name?.charAt(0) || 'U' }}
        </el-avatar>
        <div class="lock-username">{{ user?.name || '用户' }}</div>
      </div>

      <!-- 解锁输入 -->
      <div class="lock-input-area">
        <div class="unlock-wrapper">
          <!-- 密码输入框 - 毛玻璃下划线风格（Element Plus） -->
          <div class="unlock-input-box" :class="{ error: hasError }">
            <el-input
              v-model="password"
              type="password"
              placeholder="输入密码解锁"
              :prefix-icon="Lock"
              show-password
              class="unlock-el-input"
              @keyup.enter="unlock"
              @focus="hasError = false"
              autofocus
            />
          </div>

          <!-- 解锁按钮 - 脉冲光环 -->
          <div class="unlock-btn-wrapper">
            <div class="unlock-pulse"></div>
            <button class="unlock-btn" @click="unlock" :disabled="!password">
              <el-icon :size="24" v-if="!unlocking"><ArrowRight /></el-icon>
              <el-icon :size="24" v-else class="rotating"><Loading /></el-icon>
            </button>
          </div>
        </div>

        <!-- 错误提示 -->
        <transition name="shake">
          <div v-if="hasError" class="unlock-error">
            <el-icon><WarningFilled /></el-icon>
            密码错误，请重试
          </div>
        </transition>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Lock, ArrowRight, Loading, WarningFilled } from '@element-plus/icons-vue'
const defaultAvatar = '/default-avatar.png'
const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['update:visible'])
const authStore = useAuthStore()
const user = computed(() => authStore.user)

const password = ref('')
const unlocking = ref(false)
const hasError = ref(false)
const currentTime = ref('')
const currentDate = ref('')
let timer = null

function updateClock() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
  currentDate.value = now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

function unlock() {
  if (!password.value) return

  unlocking.value = true
  setTimeout(() => {
    if (password.value === '123456') {
      password.value = ''
      hasError.value = false
      emit('update:visible', false)
    } else {
      hasError.value = true
      password.value = ''
      setTimeout(() => { hasError.value = false }, 2000)
    }
    unlocking.value = false
  }, 600)
}

function handleActivity() {
  // 预留：自动锁屏功能可在此恢复
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.screen-lock {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: linear-gradient(135deg, #0a0a12 0%, #1a1a2e 50%, #0f0f1e 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  user-select: none;
}

.lock-time {
  font-size: 72px;
  font-weight: 100;
  color: #fff;
  letter-spacing: 6px;
  font-family: 'SF Mono', 'Consolas', monospace;
}

.lock-date {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: -10px;
}

.lock-user {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.lock-avatar {
  background: transparent;
  color: #fff !important;
  font-size: 60px !important;
  line-height: 60px;
  font-weight: 600;
}

.lock-username {
  font-size: 25px;
  color: rgba(255, 255, 255, 0.8);
}

/* 解锁输入区域 */
.lock-input-area {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.unlock-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 输入框容器 */
.unlock-input-box {
  transition: all 0.3s;
}

/* Element Plus 输入框覆盖样式 */
.unlock-el-input {
  width: 260px;
}

.unlock-el-input :deep(.el-input__wrapper) {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  border-radius: 0 !important;
  padding: 0 0 8px 0 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
  transition: border-color 0.3s;
}

.unlock-el-input :deep(.el-input__wrapper:hover) {
  border-bottom-color: rgba(255, 255, 255, 0.25) !important;
}

.unlock-el-input :deep(.el-input.is-focus .el-input__wrapper) {
  border-bottom-color: #409EFF !important;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.4) !important;
}

.unlock-input-box.error .unlock-el-input :deep(.el-input__wrapper) {
  border-bottom-color: #f56c6c !important;
  /* box-shadow: 0 0 8px rgba(245, 108, 108, 0.4) !important; */
}

.unlock-el-input :deep(.el-input__inner) {
  color: #fff !important;
  font-size: 18px !important;
  letter-spacing: 4px !important;
}

.unlock-el-input :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.25) !important;
  letter-spacing: 1px !important;
  font-size: 14px !important;
}

.unlock-el-input :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.4) !important;
}

.unlock-el-input :deep(.el-input.is-focus .el-input__prefix) {
  color: #409EFF !important;
}

.unlock-el-input :deep(.el-input__suffix) {
  color: rgba(255, 255, 255, 0.4) !important;
}

.unlock-el-input :deep(.el-input__suffix:hover) {
  color: rgba(255, 255, 255, 0.7) !important;
}

/* 解锁按钮 */
.unlock-btn-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.unlock-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(64, 158, 255, 0.3);
  animation: pulse-ring 2s ease-out infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.8); opacity: 0; }
}

.unlock-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #409EFF, #36cfc9);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(64, 158, 255, 0.4);
}
.unlock-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 28px rgba(64, 158, 255, 0.6);
}
.unlock-btn:active {
  transform: scale(0.95);
}
.unlock-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.rotating {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 错误提示 */
.unlock-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #f56c6c;
  font-size: 14px;
}

.shake-enter-active { animation: shake 0.4s ease; }

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  50% { transform: translateX(6px); }
  75% { transform: translateX(-4px); }
}

/* 底部提示 */
.lock-tip {
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
  margin-top: 10px;
}

/* 过渡动画 */
.lock-fade-enter-active, .lock-fade-leave-active {
  transition: all 0.4s ease;
}
.lock-fade-enter-from, .lock-fade-leave-to {
  opacity: 0;
}
</style>