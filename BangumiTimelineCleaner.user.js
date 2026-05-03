// ==UserScript==
// @name         BangumiCleaner (Timeline Only)
// @namespace    https://github.com/Adachi-Git/BangumiCleaner
// @version      0.4
// @description  仅删除页面中所有时间线记录（不删除条目）
// @author       Adachi
// @match        *://bangumi.tv/user/*/timeline
// @match        *://bgm.tv/user/*/timeline
// @match        *://chii.in/user/*/timeline
// @grant        none
// @license      MIT
// ==/UserScript==

(function () {
  'use strict';

  // 获取请求头（基本保持原样）
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

  // 时间线删除链接构造（原 timeline 逻辑保留）
  function buildTimelineDeleteUrl(button) {
    return button.href + '?gh=' + '&ajax=1';
  }

  // 批量删除时间线记录
  function deleteTimelineItems(deleteButtons) {
    return new Promise(function (resolve) {
      var counter = 0;
      var totalItems = deleteButtons.length;

      function deleteNextBatch() {
        var batch = [];
        for (var i = 0; i < 50 && counter < totalItems; i++, counter++) {
          var button = deleteButtons[counter];
          var link = buildTimelineDeleteUrl(button);
          batch.push(
            fetch(link, {
              method: 'GET',
              headers: getHeaders(),
              credentials: 'same-origin'
            })
          );
        }

        Promise.all(batch)
          .then(function (responses) {
            responses.forEach(function (response) {
              if (!response.ok) {
                throw new Error('删除请求失败');
              }
            });

            console.log('成功删除了 ' + batch.length + ' 条时间线记录');

            if (counter < totalItems) {
              setTimeout(deleteNextBatch, 1000);
            } else {
              resolve();
            }
          })
          .catch(function (error) {
            console.error('删除请求错误:', error);
            // 出错也继续尝试后续批次（沿用你原脚本策略）
            deleteNextBatch();
          });
      }

      deleteNextBatch();
    });
  }

  // 创建按钮
  var deleteItemsButton = document.createElement('button');
  deleteItemsButton.textContent = '删除时间线记录';
  deleteItemsButton.style.position = 'fixed';
  deleteItemsButton.style.top = '10px';
  deleteItemsButton.style.left = '10px';
  deleteItemsButton.style.zIndex = '9999';

  document.body.appendChild(deleteItemsButton);

  deleteItemsButton.addEventListener('click', function () {
    var confirmDelete = confirm('确定要开始删除当前页面可见的时间线记录吗？');
    if (!confirmDelete) return;

    var delButtons = document.querySelectorAll('.tml_del');
    if (!delButtons || delButtons.length === 0) {
      alert('没有找到可删除的时间线记录按钮（.tml_del）。请确认你在时间线页面。');
      return;
    }

    deleteTimelineItems(delButtons)
      .then(function () {
        console.log('所有时间线记录已成功删除');
        alert('时间线记录删除完成（本页共 ' + delButtons.length + ' 条）。');
      })
      .catch(function (error) {
        console.error('删除过程中发生错误:', error);
        alert('删除过程中发生错误，详情见控制台。');
      });
  });
})();