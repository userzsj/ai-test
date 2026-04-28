<template>
  <div class="profile-page">
    <!-- 顶部卡片 -->
    <div class="profile-hero-card">
      <!-- 头像区域 -->
      <div class="hero-avatar-section">
        <div class="avatar-wrapper" @click="triggerAvatarUpload">
          <el-avatar :size="100" class="hero-avatar" :src="authStore.user?.avatar || defaultAvatar">
            {{ form.name?.charAt(0) || 'U' }}
          </el-avatar>
          <div class="avatar-overlay">
            <el-icon :size="22"><Camera /></el-icon>
            <span>更换头像</span>
          </div>
        </div>
        <input
          ref="avatarInputRef"
          type="file"
          accept="image/*"
          hidden
          @change="handleAvatarChange"
        />
        <div class="hero-name-row">
          <h1 class="hero-name">{{ form.name }}</h1>
          <el-tag
            :type="form.role === 'ADMIN' ? 'danger' : 'info'"
            effect="dark"
            round
            size="small"
            class="hero-tag"
          >
            {{ form.role === 'ADMIN' ? '管理员' : '普通用户' }}
          </el-tag>
        </div>
        <p class="hero-email">{{ form.email }}</p>
      </div>

      <!-- 统计条 -->
      <div class="hero-stats">
        <div class="hero-stat" v-for="s in stats" :key="s.label">
          <span class="hero-stat-value">{{ s.value }}</span>
          <span class="hero-stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- 编辑切换按钮 -->
      <div class="hero-toggle">
        <el-button
          :type="isEditing ? 'success' : 'primary'"
          :icon="isEditing ? Check : Edit"
          round
          @click="toggleEdit"
        >
          {{ isEditing ? '保存信息' : '编辑资料' }}
        </el-button>
      </div>
    </div>

    <!-- 详细信息卡片 -->
    <div class="profile-detail-card">
      <h3 class="detail-title">
        <el-icon :size="20"><User /></el-icon>
        基本信息
      </h3>

      <div class="detail-grid">
        <!-- 姓名 -->
        <div class="detail-item">
          <div class="detail-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="detail-body">
            <span class="detail-label">姓名</span>
            <template v-if="isEditing">
              <el-input v-model="form.name" class="detail-input" size="small" />
            </template>
            <span v-else class="detail-value">{{ form.name }}</span>
          </div>
        </div>

        <!-- 邮箱 -->
        <div class="detail-item">
          <div class="detail-icon" style="background: rgba(103,194,58,0.1); color: #67C23A;">
            <el-icon><Message /></el-icon>
          </div>
          <div class="detail-body">
            <span class="detail-label">邮箱</span>
            <template v-if="isEditing">
              <el-input v-model="form.email" class="detail-input" size="small" />
            </template>
            <span v-else class="detail-value">{{ form.email }}</span>
          </div>
        </div>

        <!-- 手机号 -->
        <div class="detail-item">
          <div class="detail-icon" style="background: rgba(230,162,60,0.1); color: #E6A23C;">
            <el-icon><Phone /></el-icon>
          </div>
          <div class="detail-body">
            <span class="detail-label">手机号</span>
            <template v-if="isEditing">
              <el-input v-model="form.phone" class="detail-input" size="small" placeholder="未设置" />
            </template>
            <span v-else class="detail-value">{{ form.phone || '未设置' }}</span>
          </div>
        </div>

        <!-- 注册时间 -->
        <div class="detail-item">
          <div class="detail-icon" style="background: rgba(245,108,108,0.1); color: #f56c6c;">
            <el-icon><Calendar /></el-icon>
          </div>
          <div class="detail-body">
            <span class="detail-label">注册时间</span>
            <span class="detail-value">{{ form.createTime }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 安全设置 -->
    <div class="profile-detail-card">
      <h3 class="detail-title">
        <el-icon :size="20"><Lock /></el-icon>
        安全设置
      </h3>
      <div class="security-list">
        <div class="security-item">
          <span class="security-label">登录密码</span>
          <span class="security-desc">定期更换密码保护账号安全</span>
          <el-button size="small" text type="primary" @click="showPasswordDialog = true">修改</el-button>
        </div>
        <div class="security-item">
          <span class="security-label">邮箱验证</span>
          <span class="security-desc" :class="{ verified: form.isVerified }">
            {{ form.isVerified ? '已认证' : '未认证' }}
          </span>
          <el-tag :type="form.isVerified ? 'success' : 'warning'" size="small">
            {{ form.isVerified ? '已验证' : '待验证' }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <el-dialog v-model="showPasswordDialog" title="修改密码" width="420px" :close-on-click-modal="false">
      <el-form :model="passwordForm" label-width="80px">
        <el-form-item label="旧密码">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="changePassword">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import {
  Camera, Edit, Check, User, Message, Phone, Calendar, Lock
} from '@element-plus/icons-vue'
const defaultAvatar = '/default-avatar.png'
const authStore = useAuthStore()

const isEditing = ref(false)
const showPasswordDialog = ref(false)
const avatarInputRef = ref(null)

const form = reactive({
  name: authStore.user?.name || '用户',
  email: authStore.user?.email || '-',
  phone: '',
  role: authStore.user?.role || 'USER',
  isVerified: authStore.user?.is_verified || false,
  createTime: authStore.user?.create_time?.split('T')[0] || '-'
})

const stats = [
  { label: '登录次数', value: 42 },
  { label: '操作记录', value: 128 },
  { label: '所在地区', value: '北京' },
  { label: '账号状态', value: '正常' }
]

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

function toggleEdit() {
  if (isEditing.value) {
    // 保存
    isEditing.value = false
    ElMessage.success('信息已保存')
    // TODO: 调后端接口保存
  } else {
    isEditing.value = true
  }
}

function triggerAvatarUpload() {
  avatarInputRef.value?.click()
}

function handleAvatarChange(e) {
  const file = e.target.files?.[0]
  if (file) {
    ElMessage.success('头像已更新')
    // TODO: 上传到服务器
  }
}

function changePassword() {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }
  if (passwordForm.newPassword.length < 6) {
    ElMessage.error('新密码至少6位')
    return
  }
  ElMessage.success('密码修改成功')
  showPasswordDialog.value = false
  Object.assign(passwordForm, { oldPassword: '', newPassword: '', confirmPassword: '' })
}
</script>

<style scoped>
.profile-page {
  max-width: 860px;
  margin: 0 auto;
}

/* ========== 顶部英雄卡片 ========== */
.profile-hero-card {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
  border-radius: 20px;
  padding: 40px 36px 28px;
  position: relative;
  overflow: hidden;
}
.profile-hero-card::before {
  content: '';
  position: absolute;
  top: -60%;
  right: -30%;
  width: 80%;
  height: 200%;
  background: radial-gradient(circle, rgba(64,158,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}

/* 头像 */
.hero-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}
.avatar-wrapper {
  position: relative;
  cursor: pointer;
  border-radius: 50%;
}
.hero-avatar {
  background: transparent;
  color: #fff !important;
  font-size: 40px !important;
  font-weight: 700;
  border: 4px solid rgba(255,255,255,0.2);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  transition: transform 0.3s;
}
.avatar-wrapper:hover .hero-avatar {
  transform: scale(1.05);
}
.avatar-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #fff;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
}
.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.hero-name-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
}
.hero-name {
  font-size: 24px;
  color: #fff;
  font-weight: 600;
  margin: 0;
}
.hero-email {
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  margin-top: 4px;
}

/* 统计 */
.hero-stats {
  display: flex;
  justify-content: center;
  gap: 0;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,0.1);
}
.hero-stat {
  flex: 1;
  text-align: center;
}
.hero-stat-value {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}
.hero-stat-label {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  margin-top: 2px;
  display: block;
}

/* 编辑按钮 */
.hero-toggle {
  text-align: center;
  margin-top: 24px;
}

/* ========== 详细信息卡片 ========== */
.profile-detail-card {
  background: #fff;
  border-radius: 16px;
  padding: 28px 32px;
  margin-top: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.detail-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: #1a1a2e;
  margin-bottom: 24px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.detail-item {
  display: flex;
  gap: 14px;
}
.detail-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(64,158,255,0.1);
  color: #409EFF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.detail-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.detail-label {
  font-size: 12px;
  color: #bbb;
}
.detail-value {
  font-size: 14px;
  color: #444;
  font-weight: 500;
}
.detail-input {
  width: 180px;
}

/* 安全设置 */
.security-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.security-item {
  display: flex;
  align-items: center;
  gap: 16px;
}
.security-label {
  font-size: 14px;
  color: #444;
  font-weight: 500;
  width: 80px;
  flex-shrink: 0;
}
.security-desc {
  flex: 1;
  font-size: 13px;
  color: #bbb;
}
.security-desc.verified {
  color: #67C23A;
}
</style>