<template>
    <div class="register-container">
        <div class="register-box">
            <h2>用户注册</h2>
            <el-form :model="form" :rules="rules" ref="formRef">
                <!-- 原有字段 -->
                <el-form-item prop="name">
                    <el-input v-model="form.name" placeholder="姓名" prefix-icon="User" />
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="form.email" placeholder="邮箱" prefix-icon="Message" />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock"
                        show-password />
                </el-form-item>
                <el-form-item prop="confirmPassword">
                    <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Lock"
                        show-password />
                </el-form-item>

                <!-- 验证码 -->
                <el-form-item prop="captcha_text">
                    <div class="captcha-row">
                        <el-input v-model="form.captcha_text" placeholder="验证码" style="width: 60%" />
                        <div class="captcha-image" @click="refreshCaptcha">
                            <img v-if="captchaImage" :src="captchaImage" alt="验证码" />
                            <span v-else>点击获取</span>
                        </div>
                    </div>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%">
                        注 册
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :loading="loading" @click="router.push('/login')" style="width: 100%">
                        去登录
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

// 获取验证码
async function refreshCaptcha() {
    try {
        const data = await authAPI.getCaptcha()
        console.log(data);
        
        captchaImage.value = data.captcha_image
        captchaId.value = data.captcha_id
        form.captcha_id = data.captcha_id
    } catch (error) {
        ElMessage.error('获取验证码失败')
    }
}

// 自定义验证：确认密码
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
        refreshCaptcha()  // 注册失败刷新验证码
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-box {
    width: 450px;
    padding: 40px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.register-box h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.captcha-row {
    display: flex;
    gap: 10px;
    width: 100%;
}

.captcha-image {
    width: 120px;
    height: 40px;
    border: 1px solid #ddd;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f5f7fa;
}

.captcha-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.tip {
    text-align: center;
    color: #999;
    font-size: 14px;
    margin-top: 20px;
}
</style>