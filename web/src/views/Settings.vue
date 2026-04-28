<template>
    <div class="settings-page">
        <!-- 页面头部 -->
        <div class="page-head">
            <h2>系统设置</h2>
            <p>全局配置管理，变更后点击保存生效</p>
        </div>

        <!-- 设置列表 -->
        <div class="settings-list">
            <!-- 基本设置 -->
            <section class="setting-section">
                <h3 class="section-title"><el-icon>
                        <Tools />
                    </el-icon>基本设置</h3>
                <div class="setting-row">
                    <label>系统名称</label>
                    <el-input v-model="form.siteName" placeholder="显示在标题栏" style="width: 320px" />
                </div>
                <div class="setting-row">
                    <label>ICP 备案号</label>
                    <el-input v-model="form.icp" placeholder="京ICP备XXXXXXXX号" style="width: 320px" />
                </div>
            </section>

            <!-- 语言与地区 -->
            <section class="setting-section">
                <h3 class="section-title"><el-icon>
                        <ChatDotRound />
                    </el-icon>语言与地区</h3>
                <div class="setting-row">
                    <label>界面语言</label>
                    <el-select v-model="form.language" style="width: 200px">
                        <el-option label="简体中文" value="zh-CN" />
                        <el-option label="English (US)" value="en-US" />
                    </el-select>
                </div>
                <div class="setting-row">
                    <label>时区</label>
                    <el-select v-model="form.timezone" style="width: 200px">
                        <el-option label="(UTC+8) 北京时间" value="Asia/Shanghai" />
                        <el-option label="(UTC+9) 东京时间" value="Asia/Tokyo" />
                    </el-select>
                </div>
                <div class="setting-row">
                    <label>日期格式</label>
                    <el-radio-group v-model="form.dateFormat">
                        <el-radio value="YYYY-MM-DD">2026-04-28</el-radio>
                        <el-radio value="MM/DD/YYYY">04/28/2026</el-radio>
                    </el-radio-group>
                </div>
            </section>

            <!-- 屏保设置 -->
            <section class="setting-section">
                <h3 class="section-title"><el-icon>
                        <Monitor />
                    </el-icon>屏保设置</h3>
                <div class="setting-row">
                    <label>启用屏保</label>
                    <el-switch v-model="form.screensaverEnabled" />
                </div>
                <div class="setting-row">
                    <label>触发时间</label>
                    <el-select v-model="form.screensaverDelay" :disabled="!form.screensaverEnabled"
                        style="width: 200px">
                        <el-option label="5 分钟" :value="5" />
                        <el-option label="10 分钟" :value="10" />
                        <el-option label="30 分钟" :value="30" />
                    </el-select>
                </div>
                <div class="setting-row">
                    <label>屏保图片</label>
                    <div class="screensaver-area">
                        <div class="ss-grid">
                            <div v-for="(img, idx) in form.screensaverImages" :key="idx" class="ss-item"
                                :style="{ backgroundImage: `url(${img})` }">
                                <span class="ss-del" @click="removeSS(idx)"><el-icon>
                                        <Close />
                                    </el-icon></span>
                            </div>
                            <div class="ss-add" @click="ssInputRef?.click()">
                                <el-icon :size="24">
                                    <Plus />
                                </el-icon>
                                <span>添加图片</span>
                            </div>
                        </div>
                        <input ref="ssInputRef" type="file" accept="image/*" multiple hidden @change="onSSUpload" />
                    </div>
                </div>
            </section>

            <!-- 安全设置 -->
            <section class="setting-section">
                <h3 class="section-title"><el-icon>
                        <Lock />
                    </el-icon>安全设置</h3>
                <div class="setting-row">
                    <label>Token 过期</label>
                    <el-select v-model="form.tokenExpire" style="width: 200px">
                        <el-option label="30 分钟" :value="30" />
                        <el-option label="1 小时" :value="60" />
                        <el-option label="2 小时" :value="120" />
                        <el-option label="1 天" :value="1440" />
                    </el-select>
                </div>
                <div class="setting-row">
                    <label>登录锁定次数</label>
                    <el-input-number v-model="form.maxLoginAttempts" :min="3" :max="20" />
                </div>
                <div class="setting-row">
                    <label>首次强制改密</label>
                    <el-switch v-model="form.forcePasswordChange" />
                </div>
            </section>

            <!-- 注册设置 -->
            <section class="setting-section">
                <h3 class="section-title"><el-icon>
                        <User />
                    </el-icon>注册设置</h3>
                <div class="setting-row">
                    <label>开放注册</label>
                    <el-switch v-model="form.openRegister" />
                </div>
                <div class="setting-row">
                    <label>邮箱验证</label>
                    <el-switch v-model="form.requireEmailVerify" />
                </div>
                <div class="setting-row">
                    <label>默认角色</label>
                    <el-select v-model="form.defaultRole" style="width: 200px">
                        <el-option label="普通用户" value="USER" />
                        <el-option label="管理员" value="ADMIN" />
                    </el-select>
                </div>
            </section>
        </div>
        <RightPanel :saving="loading" :buttons="[
            { key: 'reset', icon: RefreshRight, label: '重置', tip: '重置表单', expandable: false }
        ]" @save="handleSave" @btn-click="handleBtnClick">
        </RightPanel>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Tools, ChatDotRound, Monitor, Lock, User, Check, Plus, Close, RefreshRight, Upload, Edit, Clock } from '@element-plus/icons-vue'
import RightPanel from '@/components/RightPanel.vue'

const loading = ref(false)

function handleSave() {
    loading.value = true
    setTimeout(() => { loading.value = false; ElMessage.success('设置已保存') }, 1000)
}
function handleBtnClick(btn) {
    if (btn.key === 'reset') {
        // 直接执行，不展开
        console.log('重置表单')
    }
}

const saving = ref(false)
const ssInputRef = ref(null)

const form = reactive({
    siteName: '用户管理系统',
    icp: '',
    language: 'zh-CN',
    timezone: 'Asia/Shanghai',
    dateFormat: 'YYYY-MM-DD',
    screensaverEnabled: true,
    screensaverDelay: 10,
    screensaverImages: [],
    tokenExpire: 30,
    maxLoginAttempts: 5,
    forcePasswordChange: false,
    openRegister: true,
    requireEmailVerify: true,
    defaultRole: 'USER'
})

const defaults = { ...form, screensaverImages: [] }

function onSSUpload(e) {
    const files = e.target.files
    if (!files?.length) return
    for (const f of files) {
        const r = new FileReader()
        r.onload = ev => form.screensaverImages.push(ev.target.result)
        r.readAsDataURL(f)
    }
    e.target.value = ''
}

function removeSS(idx) {
    form.screensaverImages.splice(idx, 1)
}

function saveSettings() {
    saving.value = true
    setTimeout(() => { saving.value = false; ElMessage.success('设置已保存') }, 500)
}

function resetSettings() {
    ElMessageBox.confirm('确定恢复默认设置？', '提示', { type: 'warning' }).then(() => {
        Object.assign(form, defaults)
        ElMessage.success('已恢复默认')
    }).catch(() => { })
}
</script>

<style scoped>
.settings-page {
    /* max-width: 800px; */
    padding: 0 0 40px;
}

.page-head {
    margin-bottom: 28px;
}

.page-head h2 {
    font-size: 20px;
    color: #1a1a2e;
    margin: 0;
}

.page-head p {
    color: #999;
    font-size: 13px;
    margin-top: 4px;
}

.settings-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.setting-section {
    background: #fff;
    border-radius: 12px;
    padding: 20px 28px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #f0f0f0;
}

.setting-row {
    display: flex;
    align-items: center;
    padding: 8px 0;
}

.setting-row:first-of-type {
    padding-top: 0;
}

.setting-row label {
    width: 140px;
    font-size: 13px;
    color: #555;
    flex-shrink: 0;
}

/* 屏保 */
.screensaver-area {
    flex: 1;
}

.ss-grid {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.ss-item {
    width: 130px;
    height: 80px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    position: relative;
    border: 1px solid #eee;
}

.ss-del {
    position: absolute;
    top: -6px;
    right: -6px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #f56c6c;
    font-size: 12px;
    opacity: 0;
    transition: 0.2s;
}

.ss-item:hover .ss-del {
    opacity: 1;
}

.ss-add {
    width: 130px;
    height: 80px;
    border: 2px dashed #d0d0d0;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    color: #bbb;
    cursor: pointer;
    transition: 0.2s;
}

.ss-add:hover {
    border-color: #409EFF;
    color: #409EFF;
    background: rgba(64, 158, 255, 0.03);
}

.ss-add span {
    font-size: 12px;
}

.actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
}
</style>