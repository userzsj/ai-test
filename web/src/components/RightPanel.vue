<template>
  <div class="save-panel">
    <!-- 主保存按钮 -->
    <div
      class="sp-main"
      :class="{ disabled: saving }"
      @click="!saving && emit('save')"
      title="保存"
    >
      <div class="sp-main-icon" :class="{ loading: saving }">
        <el-icon :size="20"><Document /></el-icon>
      </div>
      <span class="sp-main-text">保存</span>
    </div>

    <!-- 分隔 -->
    <div class="sp-divider" v-if="buttons.length"></div>

    <!-- 扩展按钮组 -->
    <div class="sp-extras">
      <template v-for="btn in buttons" :key="btn.key">
        <el-tooltip
          :content="btn.tip || btn.label"
          placement="left"
          :show-after="300"
        >
          <div
            class="sp-extra-btn"
            :class="{
              active: activeKey === btn.key && btn.expandable,
              clickable: !btn.expandable,
              disabled: saving
            }"
            @click="!saving && handleBtnClick(btn)"
          >
            <el-icon :size="18"><component :is="btn.icon" /></el-icon>
            <span class="sp-extra-label">{{ btn.label?.slice(0, 2) }}</span>
            <span class="sp-extra-full">{{ btn.label }}</span>
          </div>
        </el-tooltip>
      </template>
    </div>

    <!-- 展开的子抽屉 -->
    <teleport to="body">
      <transition name="drawer-slide">
        <div v-if="activeKey && !saving" class="sp-drawer">
          <div class="sp-drawer-head">
            <span>{{ activeLabel }}</span>
            <el-icon :size="18" @click="activeKey = ''"><Close /></el-icon>
          </div>
          <div class="sp-drawer-body">
            <slot name="drawer" :activeKey="activeKey" />
          </div>
          <div class="sp-drawer-footer" v-if="showDrawerConfirm">
            <el-button size="small" @click="activeKey = ''">取消</el-button>
            <el-button type="primary" size="small" :loading="saving" @click="emit('drawer-confirm', activeKey)">确认</el-button>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Close, Document } from '@element-plus/icons-vue'

const props = defineProps({
  buttons: { type: Array, default: () => [] },
  saving: { type: Boolean, default: false },
  showDrawerConfirm: { type: Boolean, default: true }
})

const emit = defineEmits(['save', 'btn-click', 'drawer-confirm'])

const activeKey = ref('')

const activeLabel = computed(() => {
  return props.buttons.find(b => b.key === activeKey.value)?.label || ''
})

function handleBtnClick(btn) {
  if (props.saving) return
  if (btn.expandable) {
    activeKey.value = activeKey.value === btn.key ? '' : btn.key
  } else {
    emit('btn-click', btn)
    btn.onClick?.()
  }
}
</script>

<style scoped>
/* ========== 主面板 ========== */
.save-panel {
  position: fixed;
  right: 16px;
  top: 100px;
  z-index: 500;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  background: rgba(30, 30, 50, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  padding: 8px 6px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  width: 56px;
}

/* 主保存按钮 */
.sp-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 0;
  cursor: pointer;
  border-radius: 14px;
  transition: all 0.2s;
  width: 100%;
}
.sp-main:hover:not(.disabled) {
  background: rgba(64,158,255,0.15);
}
.sp-main.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.sp-main-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409EFF, #36cfc9);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: all 0.2s;
}
.sp-main-icon.loading {
  opacity: 0.7;
  animation: pulse 1.5s ease infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.95); }
}
.sp-main:hover:not(.disabled) .sp-main-icon {
  box-shadow: 0 4px 16px rgba(64,158,255,0.5);
}
.sp-main-text {
  font-size: 11px;
  color: rgba(255,255,255,0.8);
  letter-spacing: 1px;
}

/* 分隔 */
.sp-divider {
  width: 20px;
  height: 1px;
  background: rgba(255,255,255,0.12);
  margin: 4px 0;
}

/* 扩展按钮组 */
.sp-extras {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
}

.sp-extra-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 7px 0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  color: rgba(255,255,255,0.55);
}
.sp-extra-btn:hover:not(.disabled) {
  background: rgba(255,255,255,0.06);
  color: #fff;
}
.sp-extra-btn.active {
  background: rgba(64,158,255,0.2);
  color: #409EFF;
}
.sp-extra-btn.clickable:active:not(.disabled) {
  transform: scale(0.95);
}
.sp-extra-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

/* 快捷文字（2字） */
.sp-extra-label {
  font-size: 10px;
  line-height: 1;
  letter-spacing: 1px;
  color: inherit;
}

/* 完整文字（默认隐藏，hover 时 tooltip 显示） */
.sp-extra-full {
  display: none;
}

/* ========== 抽屉 ========== */
.sp-drawer {
  position: fixed;
  right: 90px;
  top: 100px;
  width: 320px;
  max-height: 380px;
  background: rgba(20, 20, 40, 0.95);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  z-index: 501;
}

.sp-drawer-head {
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}
.sp-drawer-head .el-icon {
  color: rgba(255,255,255,0.5);
  cursor: pointer;
}
.sp-drawer-head .el-icon:hover { color: #fff; }

.sp-drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.sp-drawer-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

/* ========== 过渡 ========== */
.drawer-slide-enter-active, .drawer-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.drawer-slide-enter-from, .drawer-slide-leave-to {
  transform: translateX(30px);
  opacity: 0;
}
</style>