<script setup>
import { ref, watch, onMounted, computed } from "vue";

const STORAGE_KEY = "social-media-card-v1";

const config = ref({
  name: "",
  signature: "",
  avatarUrl: "",
  backgroundUrl: "",
});

const cardRef = ref(null);
const isDownloading = ref(false);
const storageError = ref("");

// 默认渐变背景（当没有设置背景图时）
const bgStyle = computed(() => {
  if (config.value.backgroundUrl) {
    return {
      backgroundImage: `url('${config.value.backgroundUrl}')`,
      backgroundSize: "cover",
      backgroundPosition: "center",
    };
  }
  return {
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  };
});

onMounted(() => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      Object.assign(config.value, JSON.parse(saved));
    }
  } catch {
    // localStorage 不可用时静默降级
  }
});

watch(
  config,
  (val) => {
    storageError.value = "";
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val));
    } catch (e) {
      // QuotaExceededError 通常是因为 base64 图片太大
      storageError.value =
        "图片过大，无法保存到本地缓存。下次刷新后将使用默认值。";
    }
  },
  { deep: true },
);

// 将上传的图片文件转为 base64 data URL
function handleFileUpload(field, event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    config.value[field] = e.target.result;
  };
  reader.readAsDataURL(file);
  // 清空 input value，允许再次上传相同文件
  event.target.value = "";
}

// 清除对应字段的图片
function clearImage(field) {
  config.value[field] = "";
}

// 下载卡片为 PNG（动态 import，避免 SSR 报错）
// 使用 html-to-image 替代 html2canvas，原因：html2canvas 无法解析 oklch()
async function downloadCard() {
  if (!cardRef.value || isDownloading.value) return;
  isDownloading.value = true;
  try {
    const { toPng } = await import("html-to-image");
    const dataUrl = await toPng(cardRef.value, {
      quality: 1,
      pixelRatio: 2,
      backgroundColor: "#ffffff",
    });
    const link = document.createElement("a");
    link.href = dataUrl;
    link.download = `social-card-${Date.now()}.png`;
    link.click();
  } catch (e) {
    console.error("截图失败", e);
  } finally {
    isDownloading.value = false;
  }
}

// 清除全部本地缓存
function clearStorage() {
  if (confirm("确定要清除所有已保存的设置吗？")) {
    localStorage.removeItem(STORAGE_KEY);
    config.value = {
      name: "",
      signature: "",
      avatarUrl: "",
      backgroundUrl: "",
    };
  }
}
</script>

<template>
  <h1 class="text-3xl font-bold text-gray-800 mb-2">社交媒体卡片生成</h1>
  <p class="text-gray-600 mb-8">
    自定义头像、背景、昵称和签名，导出为 PNG 图片。设置自动缓存至本地。
  </p>

  <div class="flex flex-col gap-8">
    <!-- 卡片预览区 -->
    <div class="flex flex-col items-center gap-4 w-full">
      <span class="text-sm font-medium text-gray-500 self-start">预览</span>

      <!-- 卡片本体（html2canvas 截图目标） -->
      <div
        ref="cardRef"
        class="not-prose bg-white rounded-xl shadow-lg relative w-full"
        style="height: 380px"
      >
        <!-- 背景图区（上方 60%） -->
        <div
          class="absolute inset-x-0 top-0 rounded-t-xl"
          style="height: 228px"
          :style="bgStyle"
        />

        <!-- 白色内容区（下方 40%） -->
        <div
          class="absolute inset-x-0 bottom-0 bg-white rounded-b-xl"
          style="height: 152px"
        />

        <!-- 个人资料浮层（跨越上下分界线） -->
        <div
          class="absolute right-4 flex flex-col items-end"
          style="top: 184px"
        >
          <div class="flex items-center gap-2 mr-2">
            <!-- 昵称 -->
            <span
              class="font-serif font-medium text-sm text-white"
              style="text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6)"
            >
              {{ config.name || "你的昵称" }}
            </span>
            <!-- 头像 -->
            <img
              v-if="config.avatarUrl"
              :src="config.avatarUrl"
              class="w-16 h-16 rounded object-cover"
              crossorigin="anonymous"
              alt="avatar"
            />
            <div
              v-else
              class="w-16 h-16 rounded bg-gray-100 flex items-center justify-center"
            >
              <svg
                class="w-9 h-9 text-gray-400"
                viewBox="0 0 24 24"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                />
              </svg>
            </div>
          </div>

          <!-- 签名 -->
          <p
            class="font-serif text-xs text-gray-500 mr-2 mt-1 max-w-xs text-right leading-relaxed"
          >
            {{ config.signature || "这里是你的个人签名" }}
          </p>
        </div>
      </div>

      <!-- 下载按钮 -->
      <button
        @click="downloadCard"
        :disabled="isDownloading"
        class="w-full xl:w-auto px-8 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ isDownloading ? "生成中..." : "下载图片" }}
      </button>

      <!-- CORS 提示 -->
      <p class="text-xs text-amber-600 max-w-sm text-center leading-relaxed">
        提示：使用「上传文件」方式导入图片可确保下载效果最佳。 直接填写 URL
        时，若目标服务器无 CORS 头，截图中该图片将显示为空白。
      </p>
    </div>

    <!-- 编辑面板 -->
    <div class="flex-1 w-full space-y-6">
      <span class="text-sm font-medium text-gray-500">编辑</span>

      <!-- 昵称 -->
      <div class="mt-4">
        <label class="block text-sm font-medium text-gray-700 mb-1.5"
          >昵称</label
        >
        <input
          type="text"
          v-model="config.name"
          maxlength="30"
          placeholder="输入昵称"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
        />
      </div>

      <!-- 个人签名 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5"
          >个人签名</label
        >
        <textarea
          v-model="config.signature"
          rows="2"
          maxlength="100"
          placeholder="输入个人签名"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm resize-none"
        />
      </div>

      <!-- 头像 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5"
          >头像</label
        >
        <div class="flex gap-2">
          <input
            type="url"
            v-model="config.avatarUrl"
            placeholder="输入图片 URL（支持 https://...）"
            class="flex-1 min-w-0 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-mono"
          />
          <label
            class="cursor-pointer flex-shrink-0 px-3 py-2 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 text-sm text-gray-700 transition-colors"
          >
            上传文件
            <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('avatarUrl', $event)"
            />
          </label>
          <button
            v-if="config.avatarUrl"
            @click="clearImage('avatarUrl')"
            class="flex-shrink-0 px-3 py-2 bg-red-50 border border-red-200 rounded-md hover:bg-red-100 text-sm text-red-600 transition-colors"
            title="清除头像"
          >
            清除
          </button>
        </div>
        <!-- 头像预览缩略 -->
        <div v-if="config.avatarUrl" class="mt-2 flex items-center gap-2">
          <img
            :src="config.avatarUrl"
            class="w-10 h-10 rounded object-cover border border-gray-200"
            alt="preview"
            crossorigin="anonymous"
          />
          <span class="text-xs text-gray-400 truncate max-w-xs">{{
            config.avatarUrl.startsWith("data:")
              ? "[本地文件]"
              : config.avatarUrl
          }}</span>
        </div>
      </div>

      <!-- 背景图片 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5"
          >背景图片</label
        >
        <div class="flex gap-2">
          <input
            type="url"
            v-model="config.backgroundUrl"
            placeholder="输入图片 URL（支持 https://...）"
            class="flex-1 min-w-0 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-mono"
          />
          <label
            class="cursor-pointer flex-shrink-0 px-3 py-2 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 text-sm text-gray-700 transition-colors"
          >
            上传文件
            <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload('backgroundUrl', $event)"
            />
          </label>
          <button
            v-if="config.backgroundUrl"
            @click="clearImage('backgroundUrl')"
            class="flex-shrink-0 px-3 py-2 bg-red-50 border border-red-200 rounded-md hover:bg-red-100 text-sm text-red-600 transition-colors"
            title="清除背景"
          >
            清除
          </button>
        </div>
        <!-- 背景预览缩略 -->
        <div v-if="config.backgroundUrl" class="mt-2">
          <div
            class="w-full h-16 rounded border border-gray-200 bg-cover bg-center"
            :style="{ backgroundImage: `url('${config.backgroundUrl}')` }"
          />
          <span class="text-xs text-gray-400 mt-1 block truncate">{{
            config.backgroundUrl.startsWith("data:")
              ? "[本地文件]"
              : config.backgroundUrl
          }}</span>
        </div>
        <p v-else class="mt-1 text-xs text-gray-400">
          未设置时显示默认紫色渐变背景
        </p>
      </div>

      <!-- localStorage 错误提示 -->
      <div
        v-if="storageError"
        class="p-3 bg-amber-50 border border-amber-200 rounded-md text-sm text-amber-700"
      >
        {{ storageError }}
      </div>

      <!-- 清除缓存 -->
      <div class="pt-2 border-t border-gray-100">
        <button
          @click="clearStorage"
          class="text-sm text-red-500 hover:text-red-700 transition-colors"
        >
          清除本地缓存
        </button>
        <p class="text-xs text-gray-400 mt-1">将恢复所有字段为默认值</p>
      </div>
    </div>
  </div>
</template>
