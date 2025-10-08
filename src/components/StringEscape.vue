<template>
  <div class="string-escape-tool">
    <h1>字符串转义工具</h1>
    <p>支持多种编码格式的双向转义转换</p>

    <div class="input-section">
      原始字符串：
      <textarea id="input" v-model="inputText" rows="4" cols="50" placeholder="输入原始字符串，点击左侧进行转义"></textarea>
    </div>

    <button @click="processString('encode')"">转义</button>
        <!-- 转义模式选择 -->
    <div class=" mode-selector">
      <label>转义模式：</label>
      <select v-model="escapeMode">
        <option value="html">HTML 实体</option>
        <option value="url">URL 编码</option>
        <option value="uri">URI 编码</option>
        <option value="json">JSON 转义</option>
        <option value="base64">Base64</option>
      </select>
  </div>
  <button @click="processString('decode')"">反转义</button>

    <div class=" output-section">
    转义字符串：
    <textarea id="output" v-model="outputText" rows="4" cols="50" placeholder="输入转义字符串，点击右侧按钮进行恢复"></textarea>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const inputText = ref('');
const outputText = ref('');
const escapeMode = ref('html');
const errorMessage = ref('');

// HTML 实体编码/解码
const htmlEncode = (str: string): string => {
  const textarea = document.createElement('textarea');
  textarea.textContent = str;
  return textarea.innerHTML;
};

const htmlDecode = (str: string): string => {
  const textarea = document.createElement('textarea');
  textarea.innerHTML = str;
  return textarea.value;
};

// 处理字符串转换
const processString = (operate: String) => {
  errorMessage.value = '';

  try {
    let result = '';
    if (operate === 'encode') {
      const input = inputText.value;
      console.log('Encoding with mode:', escapeMode.value);
      // 编码
      switch (escapeMode.value) {
        case 'html':
          result = htmlEncode(input);
          break;
        case 'url':
          result = encodeURIComponent(input);
          break;
        case 'uri':
          result = encodeURI(input);
          break;
        case 'json':
          result = JSON.stringify(input);
          break;
        case 'base64':
          result = btoa(unescape(encodeURIComponent(input)));
          break;
        default:
          result = input;
      }
      outputText.value = result;
    } else if (operate === 'decode') {
      console.log('Decoding with mode:', escapeMode.value);
      const output = outputText.value;
      // 解码
      switch (escapeMode.value) {
        case 'html':
          result = htmlDecode(output);
          break;
        case 'url':
          result = decodeURIComponent(output);
          break;
        case 'uri':
          result = decodeURI(output);
          break;
        case 'json':
          result = JSON.parse(output);
          break;
        case 'base64':
          result = decodeURIComponent(escape(atob(output)));
          break;
        default:
          result = output;
      }
      inputText.value = result;
    }
  } catch (error) {
    errorMessage.value = `转换失败: ${error instanceof Error ? error.message : '未知错误'}`;
    outputText.value = '';
  }
};
</script>

<style scoped>
.string-escape-tool {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.mode-selector {
  margin-bottom: 15px;
}

.mode-selector select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  margin-left: 10px;
}

.direction-selector {
  margin-bottom: 20px;
}

.radio-group {
  display: flex;
  gap: 20px;
  margin-left: 10px;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: normal;
  cursor: pointer;
}

.input-section,
.output-section {
  margin-bottom: 15px;
}

textarea {
  width: 100%;
  margin: 10px 0;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.4;
  resize: vertical;
}

button {
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  margin: 10px 0;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .string-escape-tool {
    padding: 15px;
  }

  .radio-group {
    flex-direction: column;
    gap: 10px;
  }

  textarea {
    font-size: 16px;
    /* 防止iOS缩放 */
  }
}
</style>