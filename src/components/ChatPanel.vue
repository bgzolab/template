<template>
  <section
    id="chat-section"
    class="min-h-screen flex flex-col items-center justify-center bg-white px-4 py-16"
  >
    <div class="w-full max-w-lg">
      <!-- 聊天窗口容器 -->
      <div
        class="bg-gray-50 rounded-3xl shadow-xl overflow-hidden border border-gray-100"
      >
        <!-- 顶部状态栏 -->
        <div
          class="flex items-center gap-3 px-5 py-4 bg-white border-b border-gray-100"
        >
          <div class="relative flex-shrink-0">
            <img
              :src="avatar"
              :alt="name"
              class="w-10 h-10 rounded-full object-cover"
            />
            <span
              class="absolute bottom-0 right-0 w-3 h-3 bg-green-400 border-2 border-white rounded-full"
            ></span>
          </div>
          <div>
            <p class="text-sm font-semibold text-gray-900 leading-tight">
              {{ name }}
            </p>
            <p class="text-xs text-green-500 leading-tight">有话想说</p>
          </div>
        </div>

        <!-- 消息区域 -->
        <div
          class="px-5 py-6 space-y-4 min-h-[220px] flex flex-col justify-end"
        >
          <!-- 对方（bGZo）消息气泡 -->
          <div class="flex items-end gap-2">
            <img
              :src="avatar"
              :alt="name"
              class="w-8 h-8 rounded-full object-cover flex-shrink-0 mb-1"
            />
            <div
              class="bg-white text-gray-800 text-sm rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm max-w-[75%] leading-relaxed"
            >
              有什么想聊的？去任意一个地方问问吧 ✨
            </div>
          </div>

          <!-- 用户消息气泡（有内容时才显示） -->
          <div v-if="message.trim()" class="flex items-end gap-2 justify-end">
            <div
              class="bg-gray-800 text-white text-sm rounded-2xl rounded-br-sm px-4 py-3 shadow-sm max-w-[75%] leading-relaxed"
            >
              {{ message }}
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="bg-white border-t border-gray-100">
          <div class="px-4 pt-3 pb-1">
            <textarea
              v-model="message"
              @keydown.enter.exact.prevent="send"
              placeholder="输入你的问题… (Enter 发送，Shift+Enter 换行)"
              rows="3"
              class="w-full text-sm text-gray-800 bg-transparent border-none outline-none resize-none placeholder-gray-400 leading-relaxed"
            ></textarea>
          </div>

          <!-- 工具栏：引擎选择 + 发送 -->
          <div class="flex items-center justify-between px-4 pb-3 pt-1">
            <!-- 引擎选择器 -->
            <div class="flex items-center gap-1">
              <span class="text-xs text-gray-400 mr-1">发送到：</span>
              <div class="flex flex-wrap gap-1">
                <button
                  v-for="eng in engines"
                  :key="eng.id"
                  @click="selectedEngine = eng.id"
                  :class="[
                    'text-xs px-2 py-1 rounded-full border transition-all duration-150',
                    selectedEngine === eng.id
                      ? eng.group === 'ai'
                        ? 'bg-purple-600 text-white border-purple-600'
                        : 'bg-gray-800 text-white border-gray-800'
                      : 'bg-transparent text-gray-500 border-gray-200 hover:border-gray-400',
                  ]"
                >
                  {{ eng.name }}
                </button>
              </div>
            </div>

            <!-- 发送按钮 -->
            <button
              @click="send"
              :disabled="!message.trim()"
              :class="[
                'ml-3 text-sm px-4 py-1.5 rounded-full font-medium transition-all duration-150 flex-shrink-0',
                message.trim()
                  ? 'bg-gray-900 text-white hover:bg-gray-700 cursor-pointer'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed',
              ]"
            >
              发送 ↗
            </button>
          </div>
        </div>
      </div>

      <!-- 引擎分组标注 -->
      <div class="flex justify-center gap-4 mt-4 text-xs text-gray-400">
        <span class="flex items-center gap-1">
          <span class="inline-block w-2 h-2 rounded-full bg-gray-800"></span>
          传统搜索
        </span>
        <span class="flex items-center gap-1">
          <span class="inline-block w-2 h-2 rounded-full bg-purple-600"></span>
          AI 搜索
        </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  avatar: string;
  name: string;
}>();

const message = ref("");
const selectedEngine = ref("google");

const engines = [
  // 传统搜索引擎
  {
    id: "google",
    name: "Google",
    group: "traditional",
    url: "https://www.google.com/search?q=",
  },
  {
    id: "bing",
    name: "Bing",
    group: "traditional",
    url: "https://www.bing.com/search?q=",
  },
  // AI 搜索
  {
    id: "perplexity",
    name: "Perplexity",
    group: "ai",
    url: "https://www.perplexity.ai/search?q=",
  },
  {
    id: "chatgpt",
    name: "ChatGPT",
    group: "ai",
    url: "https://chatgpt.com/?q=",
  },
  { id: "grok", name: "Grok", group: "ai", url: "https://x.com/i/grok?text=" },
];

function send() {
  const query = message.value.trim();
  if (!query) return;
  const engine = engines.find((e) => e.id === selectedEngine.value);
  if (!engine) return;
  window.open(
    engine.url + encodeURIComponent(query),
    "_blank",
    "noopener,noreferrer",
  );
}
</script>
