<template>
    <div class="ds-root">
        <!-- 消息区 -->
        <div class="ds-main" ref="msgContainer">
            <div v-if="messages.length === 0 && !loading" class="ds-empty">
                <h1>菲比揪比</h1>
                <p>有什么可以帮助你的？</p>
            </div>

            <div v-for="msg in messages" :key="msg.id" class="ds-row" :class="{ 'ds-row-user': msg.role === 'user' }">
                <div class="ds-row-inner">
                    <div class="ds-avatar">
                        <img v-if="msg.role === 'ai'" src="/default-avatar.png" class="ds-ai-logo" />
                        <span v-else class="ds-user-icon">{{ authStore.user?.name?.charAt(0) || 'U' }}</span>
                    </div>
                    <div class="ds-text" v-if="msg.role === 'user'">
                        <div class="ds-bubble">{{ msg.content }}</div>
                    </div>
                    <div class="ds-text" v-else v-html="renderContent(msg.content)" />
                </div>
            </div>

            <div v-if="loading" class="ds-row ds-row-ai">
                <div class="ds-row-inner">
                    <div class="ds-avatar">
                        <img src="/default-avatar.png" class="ds-ai-logo" />
                    </div>
                    <div class="ds-text">
                        <span class="ds-dot"></span>
                        <span class="ds-dot"></span>
                        <span class="ds-dot"></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 输入区 -->
        <div class="ds-footer">
            <div class="ds-input-box">
                <input v-model="inputText" placeholder="给 菲比揪比 发送消息" :disabled="loading"
                    @keydown.enter.exact.prevent="handleSend(inputText)" class="ds-input" />
                <button :disabled="!inputText.trim() || loading" @click="handleSend(inputText)" class="ds-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                    </svg>
                </button>
            </div>
            <p class="ds-disclaimer">内容由 AI 生成，仅供参考</p>
        </div>
    </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
const authStore = useAuthStore()
const inputText = ref('')
const loading = ref(false)
const msgContainer = ref(null)

const messages = ref([])
function renderContent(text) {
    if (!text) return ''
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')

    // 解析代码块
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
        const decoded = code.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        const highlighted = lang
            ? hljs.highlight(decoded, { language: lang }).value
            : hljs.highlightAuto(decoded).value
        return `<div class="cb"><div class="cb-h"><span>${lang || 'code'}</span><div class="cb-btns"><button class="cb-btn" data-code="${escapeHTML(decoded)}">复制</button><button class="cb-btn" data-code="${escapeHTML(decoded)}" data-lang="${lang || 'txt'}">下载</button></div></div><pre><code>${highlighted}</code></pre></div>`
    })

    html = html.replace(/`([^`]+)`/g, '<code class="ic">$1</code>')
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    html = html.replace(/\n/g, '<br>')
    return html
}

function escapeHTML(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

function handleCodeClick(e) {
    const btn = e.target.closest('.cb-btn')
    if (!btn) return
    const code = btn.dataset.code
    if (btn.textContent === '复制') {
        navigator.clipboard.writeText(code).then(() => { btn.textContent = '已复制'; setTimeout(() => btn.textContent = '复制', 2000) })
    } else {
        const blob = new Blob([code], { type: 'text/plain' })
        const a = document.createElement('a')
        a.href = URL.createObjectURL(blob)
        a.download = `code.${btn.dataset.lang || 'txt'}`
        a.click()
    }
}
async function handleSend(content) {
    const text = content?.trim?.() || content
    if (!text || loading.value) return

    messages.value.push({ id: Date.now(), role: 'user', content: text })
    inputText.value = ''
    scrollBottom()

    loading.value = true
    try {
        const response = await fetch('https://api.deepseek.com/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${import.meta.env.VITE_DEEPSEEK_API_KEY}`
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: messages.value.map(m => ({
                    role: m.role === 'ai' ? 'assistant' : 'user',
                    content: m.content
                }))
            })
        })

        const data = await response.json()
        const reply = data.choices?.[0]?.message?.content || '抱歉，没有收到回复'
        messages.value.push({ id: Date.now() + 1, role: 'ai', content: reply })
    } catch (e) {
        messages.value.push({ id: Date.now() + 1, role: 'ai', content: '请求失败，请稍后重试' })
    } finally {
        loading.value = false
        scrollBottom()
    }
}

function scrollBottom() {
    nextTick(() => {
        if (msgContainer.value) {
            msgContainer.value.scrollTop = msgContainer.value.scrollHeight
        }
    })
}
onMounted(() => document.addEventListener('click', handleCodeClick))
onUnmounted(() => document.removeEventListener('click', handleCodeClick))
</script>

<style scoped>
/* 代码块 */
:deep(.cb) {
    background: #0d1117;
    border-radius: 8px;
    margin: 10px 0;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

:deep(.cb-h) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 14px;
    background: rgba(255, 255, 255, 0.03);
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
}

:deep(.cb-btns) {
    display: flex;
    gap: 6px;
}

:deep(.cb-btn) {
    background: rgba(255, 255, 255, 0.08);
    border: none;
    color: rgba(255, 255, 255, 0.6);
    padding: 3px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
}

:deep(.cb-btn:hover) {
    background: rgba(255, 255, 255, 0.15);
    color: #fff;
}

:deep(.cb pre) {
    margin: 0;
    padding: 14px;
    overflow-x: auto;
}

:deep(.cb code) {
    font-size: 13px;
    line-height: 1.6;
}

:deep(.ic) {
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
}

.ds-root {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 125px);
    background: #1a1a2e;
    border-radius: 12px;
    overflow: hidden;
}

/* 消息区 */
.ds-main {
    flex: 1;
    overflow-y: auto;
    padding: 16px 16px 0;
}

.ds-empty {
    text-align: center;
    margin-top: 160px;
}

.ds-empty h1 {
    font-size: 32px;
    font-weight: 600;
    color: #fff;
    letter-spacing: 1px;
}

.ds-empty p {
    color: rgba(255, 255, 255, 0.45);
    font-size: 16px;
    margin-top: 10px;
}

.ds-row {
    padding: 0 0;
}

.ds-row-inner {
    display: flex;
    gap: 16px;
    padding: 18px 0;
    max-width: 800px;
    margin: 0 auto;
}

.ds-avatar {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
}

.ds-ai-logo {
    width: 40px;
    height: 40px;
    border-radius: 6px;
}

.ds-user-icon {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    background: #4f46e5;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
}

.ds-text {
    color: rgba(255, 255, 255, 0.85);
    font-size: 15px;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    /* padding-top: 3px; */
    flex: 1;
}

/* 思考动画 */
.ds-dot {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    margin-right: 6px;
    animation: bounce 1.4s infinite;
}

.ds-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.ds-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes bounce {

    0%,
    80%,
    100% {
        transform: translateY(0);
    }

    40% {
        transform: translateY(-8px);
    }
}

/* 输入区 */
.ds-footer {
    padding: 16px 16px 0px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.ds-input-box {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    background: #2a2a3e;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 10px 12px 10px 20px;
    transition: border-color 0.2s;
}

.ds-input-box:focus-within {
    border-color: rgba(99, 102, 241, 0.5);
}

.ds-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: rgba(255, 255, 255, 0.9);
    font-size: 15px;
    resize: none;
    line-height: 1.5;
    padding: 6px 0;
    font-family: inherit;
}

.ds-input::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

.ds-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
}

.ds-btn:hover:not(:disabled) {
    background: #4f46e5;
    color: #fff;
}

.ds-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.ds-disclaimer {
    text-align: center;
    color: rgba(255, 255, 255, 0.2);
    font-size: 12px;
    margin: 12px 0;
}

.ds-row-user .ds-row-inner {
    flex-direction: row-reverse;
    text-align: right;
}

/* 自定义滚动条 - 无背景轨道 */
.ds-main::-webkit-scrollbar {
    width: 4px;
}

.ds-main::-webkit-scrollbar-track {
    background: transparent;
}

.ds-main::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
}

.ds-main::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.25);
}

.ds-main::-webkit-scrollbar-button {
    display: none;
}

.ds-main {
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.12) transparent;
}

.ds-bubble {
    display: inline-block;
    background: #4f46e5;
    color: #fff;
    padding: 10px 16px;
    border-radius: 16px 16px 4px 16px;
    font-size: 15px;
    line-height: 1.5;
    max-width: 100%;
    word-break: break-word;
}
</style>