<template>
  <div class="users-container">
    <!-- 头部 -->
    <div class="header">
      <h2>用户管理</h2>
      <div class="header-right">
        <span class="user-info">
          {{ authStore.user?.name }} ({{ authStore.user?.role === 'ADMIN' ? '管理员' : '普通用户' }})
        </span>
        <el-button @click="handleLogout">退出登录</el-button>
      </div>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="keyword"
        placeholder="搜索姓名或邮箱"
        clearable
        @keyup.enter="fetchUsers"
        @clear="fetchUsers"
        style="width: 300px"
      />
      <el-button type="primary" @click="fetchUsers">搜索</el-button>
      <el-button v-if="authStore.isAdmin()" type="success" @click="handleCreate">新建用户</el-button>
    </div>

    <!-- 用户表格 -->
    <el-table :data="users" border stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="row.role === 'ADMIN' ? 'danger' : 'info'">
            {{ row.role === 'ADMIN' ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_verified" label="验证状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_verified ? 'success' : 'warning'">
            {{ row.is_verified ? '已验证' : '未验证' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.create_time).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button
            v-if="authStore.isAdmin() && row.id !== authStore.user?.id"
            type="danger"
            size="small"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchUsers"
        @current-change="fetchUsers"
      />
    </div>

    <!-- 创建/编辑弹窗 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="formRules" ref="formRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item v-if="!editingUser" label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role" v-if="authStore.isAdmin()">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="普通用户" value="USER" />
            <el-option label="管理员" value="ADMIN" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { userAPI } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

// 列表数据
const loading = ref(false)
const users = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const keyword = ref('')

// 弹窗相关
const dialogVisible = ref(false)
const submitLoading = ref(false)
const editingUser = ref(null)
const formRef = ref()
const form = reactive({
  name: '',
  email: '',
  password: '',
  role: 'user'
})

const dialogTitle = computed(() => editingUser.value ? '编辑用户' : '新建用户')

const formRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' }
  ]
}

// 获取用户列表
async function fetchUsers() {
  loading.value = true
  try {
    const data = await userAPI.getList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value
    })
    users.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

// 退出登录
function handleLogout() {
  authStore.logout()
  router.push('/login')
}

// 新建用户
function handleCreate() {
  editingUser.value = null
  Object.assign(form, {
    name: '',
    email: '',
    password: '',
    role: 'user'
  })
  // 新建时密码必填
  formRules.password[0].required = true
  dialogVisible.value = true
}

// 编辑用户
function handleEdit(row) {
  editingUser.value = row
  Object.assign(form, {
    name: row.name,
    email: row.email,
    password: '',
    role: row.role
  })
  // 编辑时密码不必填
  formRules.password[0].required = false
  dialogVisible.value = true
}

// 删除用户
async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除用户 "${row.name}" 吗？`, '提示', {
      type: 'warning'
    })
    await userAPI.delete(row.id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      // 错误已在拦截器处理
    }
  }
}

// 提交表单
async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitLoading.value = true
  try {
    if (editingUser.value) {
      const updateData = {
        name: form.name,
        email: form.email
      }
      if (authStore.isAdmin()) {
        updateData.role = form.role
      }
      await userAPI.update(editingUser.value.id, updateData)
      ElMessage.success('更新成功')
    } else {
      await userAPI.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchUsers()
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
function resetForm() {
  formRef.value?.resetFields()
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}
.header h2 {
  color: #333;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}
.user-info {
  color: #666;
}
.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  padding: 0 10px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>