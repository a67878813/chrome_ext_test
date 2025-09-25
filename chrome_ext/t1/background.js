// background.js

// 监听扩展程序图标的点击事件
chrome.action.onClicked.addListener((tab) => {
  // 当用户点击图标时，这段代码会执行
  console.log('123123123123');
  console.log('id= ', tab.id);
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content-script.js']
  });

  // 可以在这里执行更多操作，比如向当前标签页注入脚本
  // chrome.scripting.executeScript({
  //   target: { tabId: tab.id },
  //   files: ['content-script.js']
  // });
});