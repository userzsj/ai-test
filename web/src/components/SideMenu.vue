<template>
    <div :style="{ width: collapsed ? '64px' : '220px' }" class="side-menu">
        <el-menu :default-active="activePath" :collapse="collapsed" :router="true" class="custom-menu">
            <SideMenuItem :menu-list="menuTree" />
        </el-menu>
    </div>
</template>

<script setup>
import SideMenuItem from './SideMenuItem.vue'

defineProps({
    menuTree: { type: Array, default: () => [] },
    activePath: { type: String, default: '' },
    collapsed: { type: Boolean, default: false }
})
</script>

<style scoped>
.side-menu {
    height: 100%;
    transition: width 0.25s;
    flex-shrink: 0;
    overflow: hidden;
}
</style>

<style>
.custom-menu {
    height: 100%;
    background: #304156 !important;
    border-right: none !important;
}

.custom-menu .el-menu-item,
.custom-menu .el-sub-menu__title {
    color: #bfcbd9;
    transition: all 0.2s;
}

.custom-menu .el-menu-item:hover,
.custom-menu .el-sub-menu__title:hover {
    background-color: rgba(255, 255, 255, 0.06) !important;
    color: #fff !important;
}

.custom-menu .el-menu-item.is-active {
    background: rgba(64, 158, 255, 0.15) !important;
    color: #409EFF !important;
}

.custom-menu .el-sub-menu .el-menu {
    background: rgba(0, 0, 0, 0.2) !important;
}
</style>