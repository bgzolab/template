<template>
  <section
    id="chat-section"
    class="min-h-screen flex flex-col items-center justify-center bg-white px-4 py-16"
  >
    <div class="w-full max-w-lg">
      <div
        class="bg-gray-50 rounded-3xl shadow-xl overflow-hidden border border-gray-100"
      >
        <!-- 顶部状态栏 -->
        <div
          class="flex items-center justify-between gap-3 px-5 py-4 bg-white border-b border-gray-100"
        >
          <div class="flex items-center gap-3">
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
          <!-- 导出 / 清空 -->
          <div class="flex items-center gap-1">
            <button
              @click="exportHistory"
              class="text-xs text-gray-400 hover:text-gray-700 px-2.5 py-1 rounded-lg hover:bg-gray-100 transition-colors"
              title="导出记录"
            >
              导出
            </button>
            <button
              @click="clearHistory"
              class="text-xs text-gray-400 hover:text-red-500 px-2.5 py-1 rounded-lg hover:bg-gray-100 transition-colors"
              title="清空记录"
            >
              清空
            </button>
          </div>
        </div>

        <!-- 消息区域（固定高，可滚动） -->
        <div
          ref="messagesEl"
          class="px-5 py-5 space-y-4 h-64 overflow-y-auto scroll-smooth"
        >
          <!-- 欢迎气泡（始终置顶） -->
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

          <!-- 历史消息 -->
          <template v-for="msg in messages" :key="msg.id">
            <!-- 用户消息 -->
            <div
              v-if="msg.role === 'user'"
              class="flex items-end gap-2 justify-end"
            >
              <div
                class="bg-gray-800 text-white text-sm rounded-2xl rounded-br-sm px-4 py-3 shadow-sm max-w-[75%] leading-relaxed break-words"
              >
                {{ msg.text }}
              </div>
            </div>
            <!-- Bot 回复 -->
            <div v-else class="flex items-end gap-2">
              <img
                :src="avatar"
                :alt="name"
                class="w-8 h-8 rounded-full object-cover flex-shrink-0 mb-1"
              />
              <div
                class="bg-white text-gray-700 text-sm rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm max-w-[75%] leading-relaxed"
              >
                {{ msg.text }}
              </div>
            </div>
          </template>
        </div>

        <!-- 输入区 + 工具栏 -->
        <div class="bg-white border-t border-gray-100">
          <!-- Textarea -->
          <div class="px-4 pt-3 pb-1">
            <textarea
              v-model="message"
              @keydown.enter.exact.prevent="send"
              placeholder="输入你的问题… (Enter 发送，Shift+Enter 换行)"
              rows="2"
              class="w-full text-sm text-gray-800 bg-transparent border-none outline-none resize-none placeholder-gray-400 leading-relaxed"
            ></textarea>
          </div>

          <!-- 引擎分类选择器（下拉） -->
          <div class="flex items-center gap-1.5 px-4 pb-2 flex-wrap">
            <span class="text-xs text-gray-400 flex-shrink-0">发送到：</span>
            <!-- 每个分类 pill + 下拉 -->
            <div
              v-for="cat in categories"
              :key="cat.id"
              class="relative"
              @click.stop
            >
              <button
                @click="toggleCategory(cat.id)"
                :class="[
                  'text-xs px-2.5 py-1 rounded-full border transition-all duration-150 flex items-center gap-1 whitespace-nowrap',
                  activeCategoryId === cat.id
                    ? cat.color + ' text-white border-transparent shadow-sm'
                    : 'bg-transparent text-gray-500 border-gray-200 hover:border-gray-400',
                ]"
              >
                <span>{{ cat.icon }}</span>
                <span>{{ selectedInCategory(cat.id) ?? cat.name }}</span>
                <span class="opacity-50 text-[10px]">▾</span>
              </button>

              <!-- 下拉菜单（向上展开） -->
              <Transition
                enter-active-class="transition-all duration-150 ease-out"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition-all duration-100 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-1"
              >
                <div
                  v-if="openDropdown === cat.id"
                  class="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-30 min-w-[130px]"
                >
                  <p
                    class="px-3 pt-2 pb-1 text-[10px] font-semibold text-gray-400 uppercase tracking-wide"
                  >
                    {{ cat.label }}
                  </p>
                  <button
                    v-for="eng in cat.engines"
                    :key="eng.id"
                    @click="selectEngine(cat.id, eng.id)"
                    :class="[
                      'flex items-center justify-between w-full text-left text-xs px-4 py-2.5 hover:bg-gray-50 transition-colors gap-3',
                      selectedEngineId === eng.id
                        ? 'font-semibold text-gray-900'
                        : 'text-gray-600',
                    ]"
                  >
                    <span>{{ eng.name }}</span>
                    <span
                      v-if="selectedEngineId === eng.id"
                      class="text-green-500 flex-shrink-0"
                      >✓</span
                    >
                  </button>
                </div>
              </Transition>
            </div>
          </div>

          <!-- 发送行 -->
          <div class="flex items-center justify-between px-4 pb-3 gap-2">
            <p class="text-xs text-gray-400 truncate">
              <span
                >已选
                <strong class="text-gray-600">{{
                  currentEngine?.name ?? "—"
                }}</strong></span
              >
              <span v-if="currentEngine?.directOpen" class="ml-1 text-amber-500"
                >（将复制内容到剪贴板）</span
              >
            </p>
            <button
              @click="send"
              :disabled="!message.trim()"
              :class="[
                'text-sm px-4 py-1.5 rounded-full font-medium transition-all duration-150 flex-shrink-0',
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
    </div>
  </section>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  watch,
  nextTick,
  onMounted,
  onBeforeUnmount,
} from "vue";

const STORAGE_KEY = "bgzo_chat_history";

interface Engine {
  id: string;
  name: string;
  url: string;
  directOpen?: boolean; // 不支持 URL query，改为复制到剪贴板后打开
}

interface Category {
  id: string;
  name: string; // pill 上显示（分类名或已选引擎名）
  label: string; // 下拉标题
  icon: string;
  color: string; // Tailwind bg class
  engines: Engine[];
}

interface Message {
  id: string;
  role: "user" | "bot";
  text: string;
  ts: number;
}

const props = defineProps<{ avatar: string; name: string }>();

const categories: Category[] = [
  {
    id: "traditional",
    name: "传统搜索",
    label: "传统搜索引擎",
    icon: "🔍",
    color: "bg-gray-700",
    engines: [
      { id: "google", name: "Google", url: "https://www.google.com/search?q=" },
      { id: "bing", name: "Bing", url: "https://www.bing.com/search?q=" },
    ],
  },
  {
    id: "llm",
    name: "LLM",
    label: "AI / 大语言模型",
    icon: "✨",
    color: "bg-purple-600",
    engines: [
      {
        id: "perplexity",
        name: "Perplexity",
        url: "https://www.perplexity.ai/search?q=",
      },
      { id: "chatgpt", name: "ChatGPT", url: "https://chatgpt.com/?q=" },
      { id: "grok", name: "Grok", url: "https://x.com/i/grok?text=" },
      // DeepSeek 不支持 URL 传参，采用剪贴板方案
      {
        id: "deepseek",
        name: "DeepSeek",
        url: "https://chat.deepseek.com/",
        directOpen: true,
      },
    ],
  },
  {
    id: "archive",
    name: "档案馆",
    label: "互联网档案馆",
    icon: "🗄️",
    color: "bg-amber-600",
    engines: [
      {
        id: "archive_org",
        name: "archive.org",
        url: "https://archive.org/search?query=",
      },
      // archive.is 以 URL 为输入，直接拼接
      { id: "archive_is", name: "archive.is", url: "https://archive.ph/" },
    ],
  },
  {
    id: "mobile",
    name: "手机端",
    label: "手机专有 Schema",
    icon: "📱",
    color: "bg-rose-500",
    engines: [
      {
        id: "xiaohongshu",
        name: "小红书",
        url: "xhsdiscover://search/result?keyword=",
      },
    ],
  },
];

// ── 引擎选择状态 ─────────────────────────────────────────────
const selectedEngineId = ref("google");
const activeCategoryId = ref("traditional");
const openDropdown = ref<string | null>(null);

const currentEngine = computed<Engine | undefined>(() => {
  for (const cat of categories) {
    const eng = cat.engines.find((e) => e.id === selectedEngineId.value);
    if (eng) return eng;
  }
  return undefined;
});

/** 返回该分类内已选引擎名（无则 null，pill 退回显示分类名） */
function selectedInCategory(catId: string): string | null {
  const cat = categories.find((c) => c.id === catId);
  return (
    cat?.engines.find((e) => e.id === selectedEngineId.value)?.name ?? null
  );
}

function toggleCategory(catId: string) {
  openDropdown.value = openDropdown.value === catId ? null : catId;
}

function selectEngine(catId: string, engId: string) {
  selectedEngineId.value = engId;
  activeCategoryId.value = catId;
  openDropdown.value = null;
}

// 点击 pill 区域外关闭下拉
function handleDocClick() {
  if (openDropdown.value !== null) openDropdown.value = null;
}

// ── 消息 & localStorage ──────────────────────────────────────
const messages = ref<Message[]>([]);
const message = ref("");
const messagesEl = ref<HTMLElement | null>(null);

function scrollToBottom() {
  nextTick(() => {
    if (messagesEl.value)
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
  });
}

watch(messages, scrollToBottom, { deep: true });

function loadHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) messages.value = JSON.parse(raw);
  } catch {
    messages.value = [];
  }
}

function saveHistory() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value));
}

function send() {
  const query = message.value.trim();
  if (!query) return;
  const engine = currentEngine.value;
  if (!engine) return;

  const ts = Date.now();
  messages.value.push({ id: `u-${ts}`, role: "user", text: query, ts });

  let botText: string;
  if (engine.directOpen) {
    // 不支持 URL query，复制内容后直接打开
    navigator.clipboard?.writeText(query).catch(() => {});
    window.open(engine.url, "_blank", "noopener,noreferrer");
    botText = `内容已复制到剪贴板，正在打开 ${engine.name} ✂️`;
  } else {
    window.open(
      engine.url + encodeURIComponent(query),
      "_blank",
      "noopener,noreferrer",
    );
    botText = `为你打开 ${engine.name} 🔗`;
  }

  messages.value.push({
    id: `b-${ts + 1}`,
    role: "bot",
    text: botText,
    ts: ts + 1,
  });
  saveHistory();
  message.value = "";
}

function exportHistory() {
  if (messages.value.length === 0) {
    alert("暂无记录可导出");
    return;
  }
  const lines = messages.value.map((m) => {
    const who = m.role === "user" ? "我" : props.name;
    const time = new Date(m.ts).toLocaleString("zh-CN");
    return `[${time}] ${who}：${m.text}`;
  });
  const blob = new Blob([lines.join("\n")], {
    type: "text/plain;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement("a"), {
    href: url,
    download: `chat-${new Date().toISOString().slice(0, 10)}.txt`,
  });
  a.click();
  URL.revokeObjectURL(url);
}

function clearHistory() {
  if (!confirm("确认清空所有聊天记录？")) return;
  messages.value = [];
  localStorage.removeItem(STORAGE_KEY);
}

onMounted(() => {
  loadHistory();
  scrollToBottom();
  document.addEventListener("click", handleDocClick);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleDocClick);
});
</script>
