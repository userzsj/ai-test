<template>
    <div class="register-container">
        <!-- Three.js 背景 -->
        <ThreeBackground />

        <div class="register-box">
            <h2>创建账号</h2>
            <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleRegister">
                <el-form-item prop="name">
                    <el-input v-model="form.name" placeholder="姓名" prefix-icon="User" class="glass-input" />
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="form.email" placeholder="邮箱" prefix-icon="Message" class="glass-input" />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password
                        class="glass-input" />
                </el-form-item>
                <el-form-item prop="confirmPassword">
                    <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Lock"
                        show-password class="glass-input" />
                </el-form-item>


                <!-- 验证码 -->
                <el-form-item prop="captcha_text">
                    <div class="captcha-row">
                        <el-input v-model="form.captcha_text" placeholder="验证码" class="glass-input captcha-input" />
                        <div class="captcha-box" @click="refreshCaptcha">
                            <img v-if="captchaImage" :src="captchaImage" alt="验证码" class="captcha-img" />
                            <div v-else class="captcha-placeholder">
                                <span class="refresh-text">点击获取</span>
                            </div>
                        </div>
                    </div>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" :loading="loading" @click="handleRegister" class="register-btn">
                        注 册
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="loading" @click="router.push('/login')" class="login-btn">
                        已有账号？去登录
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/api'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import ThreeBackground from '@/components/ThreeBackground.vue'

const router = useRouter()

const formRef = ref()
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

async function refreshCaptcha() {
    try {
        const data = await authAPI.getCaptcha()
        captchaImage.value = data.captcha_image
        captchaId.value = data.captcha_id
        form.captcha_id = data.captcha_id
    } catch (error) {
        ElMessage.error('获取验证码失败')
    }
}

const validateConfirmPassword = (rule, value, callback) => {
    if (value !== form.password) {
        callback(new Error('两次输入的密码不一致'))
    } else {
        callback()
    }
}

const rules = {
    name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '姓名长度为 2-20 个字符', trigger: 'blur' }
    ],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码至少 6 位', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
    ],
    captcha_text: [
        { required: true, message: '请输入验证码', trigger: 'blur' }
    ]
}

async function handleRegister() {
    const valid = await formRef.value.validate().catch(() => false)
    if (!valid) return

    loading.value = true
    try {
        await authAPI.register({
            name: form.name,
            email: form.email,
            password: form.password,
            captcha_id: form.captcha_id,
            captcha_text: form.captcha_text
        })
        ElMessage.success('注册成功！请查收邮件验证邮箱')
        router.push('/login')
    } catch (error) {
        refreshCaptcha()
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    refreshCaptcha()
})
</script>

<style scoped>
.register-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.register-box {
    width: 460px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.15);
    z-index: 1;
    animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.register-box h2 {
    text-align: center;
    margin-bottom: 28px;
    color: #fff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    font-weight: 400;
    letter-spacing: 3px;
    font-size: 26px;
}

/* 毛玻璃输入框 */
:deep(.glass-input .el-input__wrapper) {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: none !important;
    border-radius: 14px !important;
    transition: all 0.3s ease;
}

:deep(.glass-input .el-input__wrapper:hover) {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

:deep(.glass-input .el-input__wrapper.is-focus) {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: #f093fb !important;
    box-shadow: 0 0 0 2px rgba(240, 147, 251, 0.2) !important;
}

:deep(.glass-input input) {
    color: #fff !important;
}

:deep(.glass-input input::placeholder) {
    color: rgba(255, 255, 255, 0.65) !important;
}

:deep(.glass-input .el-input__prefix) {
    color: rgba(255, 255, 255, 0.75) !important;
}

/* 验证码区域 */
.captcha-row {
    display: flex;
    gap: 10px;
    width: 100%;
    align-items: center;
}

.captcha-input {
    flex: 1;
}

.captcha-box {
    width: 105px;
    height: 40px;
    border-radius: 10px;
    cursor: pointer;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    transition: all 0.3s ease;
    flex-shrink: 0;
}

.captcha-box:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.45);
    transform: scale(1.02);
}

.captcha-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.captcha-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    color: rgba(255, 255, 255, 0.85);
}

.refresh-text {
    font-size: 12px;
    white-space: nowrap;
}

/* 按钮 */
.register-btn {
    width: 100%;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    height: 46px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 2px;
}

.register-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5) !important;
}

.login-btn {
    width: 100%;
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 14px !important;
    height: 42px !important;
    font-size: 14px !important;
    color: #fff !important;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease !important;
}

.login-btn:hover {
    background: rgba(255, 255, 255, 0.2) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}
</style>