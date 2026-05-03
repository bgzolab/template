// ==UserScript==
// @name         BangumiCleaner (Timeline Auto-Paging)
// @namespace    https://github.com/Adachi-Git/BangumiCleaner
// @version      0.4
// @description  仅删除时间线记录，并自动翻页直到清空
// @author       Adachi
// @match        *://bangumi.tv/user/*/timeline*
// @match        *://bgm.tv/user/*/timeline*
// @match        *://chii.in/user/*/timeline*
// @grant        none
// @license      MIT
// ==/UserScript==

(function () {
  'use strict';

  // 每批删除条数与批次间隔
  var BATCH_SIZE = 50;
  var BATCH_DELAY_MS = 1000;
  var PAGE_DELAY_MS = 1500;

  // localStorage key：用于跨页面继续自动删除
  var LS_RUNNING_KEY = 'bgm_cleaner_timeline_running';

  function sleep(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  function getHeaders() {
    return {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie': document.cookie,
      'Host': window.location.hostname,
      'Referer': window.location.href,
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': navigator.userAgent,
      'X-Requested-With': 'XMLHttpRequest'
    };
  }

  function buildTimelineDeleteUrl(button) {
    // 原脚本逻辑：button.href + '?gh=' + '&ajax=1'
    return button.href + '?gh=' + '&ajax=1';
  }

  async function deleteTimelineItemsOnThisPage() {
    var deleteButtons = Array.from(document.querySelectorAll('.tml_del'));
    if (deleteButtons.length === 0) {
      console.log('[BangumiCleaner] 本页未找到 .tml_del，可视为本页无可删记录。');
      return 0;
    }

    var deleted = 0;
    var counter = 0;

    while (counter < deleteButtons.length) {
      var batchButtons = deleteButtons.slice(counter, counter + BATCH_SIZE);
      counter += batchButtons.length;

      var batchFetches = batchButtons.map(function (btn) {
        var url = buildTimelineDeleteUrl(btn);
        return fetch(url, {
          method: 'GET',
          headers: getHeaders(),
          credentials: 'same-origin'
        }).then(function (resp) {
          if (!resp.ok) throw new Error('删除请求失败: ' + resp.status);
          return resp.text();
        });
      });

      try {
        await Promise.all(batchFetches);
        deleted += batchButtons.length;
        console.log('[BangumiCleaner] 成功删除本页 ' + deleted + '/' + deleteButtons.length);
      } catch (e) {
        console.error('[BangumiCleaner] 批量删除中出现错误（将继续下一批）:', e);
      }

      await sleep(BATCH_DELAY_MS);
    }

    return deleted;
  }

  // 1) 优先从分页 DOM 找“下一页”
  function findNextPageUrlFromDom() {
    // Bangumi 常见分页结构：#multipage / .p / a.next 等；这里做多策略尝试
    var candidates = [
      '#multipage a.next',
      '.p a.next',
      'a.next',
      '#multipage a.p',
      '#multipage a',
      '.p a'
    ];

    for (var i = 0; i < candidates.length; i++) {
      var a = document.querySelector(candidates[i]);
      if (a && a.getAttribute('href')) {
        var text = (a.textContent || '').trim();
        // 尽量筛掉“上一页”
        if (text.includes('下一页') || text.includes('›') || a.classList.contains('next')) {
          return new URL(a.getAttribute('href'), window.location.href).toString();
        }
      }
    }
    return null;
  }

  // 2) 如果 DOM 找不到，尝试用 ?page=N 自增（保守：只有当当前 URL 上有 page 参数时才自增）
  function buildNextPageUrlByPageParam() {
    var url = new URL(window.location.href);
    if (!url.searchParams.has('page')) return null;

    var cur = parseInt(url.searchParams.get('page') || '1', 10);
    if (!Number.isFinite(cur) || cur < 1) cur = 1;

    url.searchParams.set('page', String(cur + 1));
    return url.toString();
  }

  function getNextPageUrl() {
    return findNextPageUrlFromDom() || buildNextPageUrlByPageParam();
  }

  async function runOnceThenMaybeGoNext() {
    var deleted = await deleteTimelineItemsOnThisPage();

    // 等一等，避免页面/服务端状态不同步
    await sleep(PAGE_DELAY_MS);

    var nextUrl = getNextPageUrl();
    if (!nextUrl) {
      console.log('[BangumiCleaner] 未找到下一页，流程结束。');
      localStorage.removeItem(LS_RUNNING_KEY);
      alert('时间线清理完成：未找到下一页。');
      return;
    }

    console.log('[BangumiCleaner] 准备跳转下一页继续：', nextUrl);
    // 保持“运行中”标记，跨页面继续
    localStorage.setItem(LS_RUNNING_KEY, '1');
    window.location.href = nextUrl;
  }

  // UI：开始/停止
  function createControls() {
    var startBtn = document.createElement('button');
    startBtn.textContent = '清空时间线(自动翻页)';
    startBtn.style.position = 'fixed';
    startBtn.style.top = '10px';
    startBtn.style.left = '10px';
    startBtn.style.zIndex = '9999';

    var stopBtn = document.createElement('button');
    stopBtn.textContent = '停止清空';
    stopBtn.style.position = 'fixed';
    stopBtn.style.top = '44px';
    stopBtn.style.left = '10px';
    stopBtn.style.zIndex = '9999';

    startBtn.addEventListener('click', function () {
      var ok = confirm('确定要开始清空时间线并自动翻页吗？\n（会连续删除，直到没有下一页）');
      if (!ok) return;

      localStorage.setItem(LS_RUNNING_KEY, '1');
      runOnceThenMaybeGoNext().catch(function (e) {
        console.error('[BangumiCleaner] 运行失败:', e);
        localStorage.removeItem(LS_RUNNING_KEY);
        alert('运行失败，详情见控制台。');
      });
    });

    stopBtn.addEventListener('click', function () {
      localStorage.removeItem(LS_RUNNING_KEY);
      alert('已停止（下次不会自动继续）。');
    });

    document.body.appendChild(startBtn);
    document.body.appendChild(stopBtn);
  }

  // 初始化 UI
  createControls();

  // 如果上个页面跳转过来仍处于“运行中”，自动继续
  if (localStorage.getItem(LS_RUNNING_KEY) === '1') {
    console.log('[BangumiCleaner] 检测到运行中标记，自动继续清理本页。');
    runOnceThenMaybeGoNext().catch(function (e) {
      console.error('[BangumiCleaner] 自动继续失败:', e);
      localStorage.removeItem(LS_RUNNING_KEY);
    });
  }
})();