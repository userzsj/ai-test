<template>
    <div class="login-container">
        <div class="login-box">
            <h2>用户管理系统</h2>
            <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
                <el-form-item prop="email">
                    <el-input v-model="form.email" placeholder="邮箱" prefix-icon="User" />
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock"
                        show-password />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%">
                        登 录
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="loading" @click="router.push('/register')" style="width: 100%">
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
        // 错误已经在拦截器里显示了，这里只需要处理加载状态
        // 如果想自定义错误提示，可以在这里处理
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
    width: 400px;
    padding: 40px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-box h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.tip {
    text-align: center;
    color: #999;
    font-size: 13px;
    margin-top: 20px;
}
</style>