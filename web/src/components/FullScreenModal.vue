<template>
    <div class="fullscreen-wrapper">
        <!-- 正常展示：弹窗关闭时显示 -->
        <template v-if="isShowSmall">
            <div v-if="!visible" class="normal-view">
                <slot />
            </div>

            <!-- 全屏按钮 -->
            <span class="trigger-btn" @click="visible = true" :title="triggerText">
                <el-icon :size="18">
                    <FullScreen />
                </el-icon>
            </span>
        </template>


        <!-- 全屏弹窗 -->
        <el-dialog v-model="visible" :title="title" :fullscreen="true" :show-close="true" :close-on-click-modal="false"
            :destroy-on-close="true" class="fullscreen-dialog">
            <div class="fullscreen-body" v-if="visible">
                <slot name="fullscreen">
                    <slot />
                </slot>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { FullScreen } from '@element-plus/icons-vue'

defineProps({
    title: { type: String, default: '全屏展示' },
    triggerText: { type: String, default: '全屏' },
    isShowSmall: { type: Boolean, default: true },
})

const visible = ref(false)
defineExpose({ visible })
</script>

<style>
.fullscreen-dialog .el-dialog__body {
    padding: 0 !important;
    overflow: auto;
}

.fullscreen-body {
    width: 100%;
    height: 100%;
    overflow: hidden;
}
</style>

<style scoped>
.fullscreen-wrapper {
    position: relative;
}

.normal-view {
    width: 100%;
    height: 100%;
}

.trigger-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 10;
    cursor: pointer;
    color: #999;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s;
    padding: 6px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(4px);
}

.trigger-btn:hover {
    color: #409EFF;
    background: rgba(64, 158, 255, 0.1);
}
</style>