<template>
    <div class="login-container">
        <!-- Three.js 背景 -->
        <ThreeBackground />
        
        <!-- 登录框 - 毛玻璃效果 -->
        <div class="login-box">
            <h2>管理系统</h2>
            <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
                <el-form-item prop="email">
                    <el-input 
                        v-model="form.email" 
                        placeholder="邮箱" 
                        prefix-icon="User"
                        class="glass-input"
                    />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input 
                        v-model="form.password" 
                        type="password" 
                        placeholder="密码" 
                        prefix-icon="Lock"
                        show-password 
                        class="glass-input"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :loading="loading" @click="handleLogin" class="login-btn">
                        登 录
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="loading" @click="router.push('/register')" class="register-btn">
                        去注册
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import ThreeBackground from '@/components/ThreeBackground.vue'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)
const form = reactive({
    email: '',
    password: ''
})

const rules = {
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码至少 6 位', trigger: 'blur' }
    ]
}

async function handleLogin() {
    const valid = await formRef.value.validate().catch(() => false)
    if (!valid) return

    loading.value = true
    try {
        await authStore.login(form)
        ElMessage.success('登录成功')
        router.push('/')
    } catch (error) {
        console.error('登录失败:', error)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.login-box {
    width: 400px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    z-index: 1;
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.login-box h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #fff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    font-weight: 400;
    letter-spacing: 2px;
}

:deep(.glass-input .el-input__wrapper) {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: none !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
}

:deep(.glass-input .el-input__wrapper:hover) {
    background: rgba(255, 255, 255, 0.25) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}

:deep(.glass-input .el-input__wrapper.is-focus) {
    background: rgba(255, 255, 255, 0.25) !important;
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
}

:deep(.glass-input input) {
    color: #fff !important;
}

:deep(.glass-input input::placeholder) {
    color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.glass-input .el-input__prefix) {
    color: rgba(255, 255, 255, 0.8) !important;
}

.login-btn {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    height: 44px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

.login-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
}

.register-btn {
    width: 100%;
    background: rgba(255, 255, 255, 0.15) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    height: 44px !important;
    font-size: 16px !important;
    color: #fff !important;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease !important;
}

.register-btn:hover {
    background: rgba(255, 255, 255, 0.25) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}
</style>