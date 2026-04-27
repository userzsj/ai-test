<template>
  <template v-for="item in menuList" :key="item.id">
    <!-- 有子节点：渲染为可展开的父菜单 -->
    <el-sub-menu v-if="item.children?.length" :index="item.id">
      <template #title>
        <el-icon v-if="item.icon"><component :is="item.icon" /></el-icon>
        <span>{{ item.name }}</span>
      </template>
      <SideMenuItem :menu-list="item.children" />
    </el-sub-menu>

    <!-- 无子节点：渲染为叶子菜单项 -->
    <el-menu-item v-else :index="item.path">
      <el-icon v-if="item.icon"><component :is="item.icon" /></el-icon>
      <template #title><span>{{ item.name }}</span></template>
    </el-menu-item>
  </template>
</template>

<script setup>
defineProps({ menuList: { type: Array, default: () => [] } })
</script>