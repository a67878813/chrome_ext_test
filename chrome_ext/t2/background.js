// background.js

// 监听扩展程序图标的点击事件
chrome.action.onClicked.addListener((tab) => {
  // 当用户点击图标时，这段代码会执行
  console.log('点击事件');
  //console.log('id= ', tab.id);
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

// 用于跟踪当前显示的索引，初始为 -1 以确保第一次点击时从 0 开始
let displayIndex = 0;
// 你的全局变量，现在是一个对象数组
let mySharedDataArray = [//max 4 digits
    { text: "D", color: "#33FF57" },
    { text: "T", color: "#f8ff33ff" },
    { text: "d", color: "#3357FF" },
    { text: "Y", color: "#d92fffff" },
    { text: "Copy", color: "#b2b2b2ff" }
];

// 在徽章上显示文本
chrome.action.setBadgeText({ text: mySharedDataArray[0].text }); 
chrome.action.setBadgeBackgroundColor({ color: mySharedDataArray[0].color });
// 改变鼠标悬停时的提示文本
chrome.action.setTitle({ title: 'Alt C 切换组\n Alt O 发送至API \n 可能需手动配置快捷键' });


// 监听来自其他脚本（如内容脚本）的消息
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action === "getGroup") {

      // 获取当前索引对应的对象
      const currentData = mySharedDataArray[displayIndex];

      // 返回当前组的 text 内容
      sendResponse({ status: "success", text: currentData.text });

    // } else if (request.action === "changeGroup") {
    //   displayIndex = (displayIndex + 1) % mySharedDataArray.length;
    //   const nextData = mySharedDataArray[displayIndex];
    //   chrome.action.setBadgeText({ text: nextData.text.substring(0, 4) });
    //   chrome.action.setBadgeBackgroundColor({ color: nextData.color });
    //   sendResponse({ status: "success", newText: nextData.text, newColor: nextData.color });
    // }
  }
);

// 监听命令事件
chrome.commands.onCommand.addListener((command) => {
  if (command === "change_group") {
    console.log("用户按下了 'change_group' 快捷键");
      // 递增索引，并使用取余实现循环
      displayIndex = (displayIndex + 1) % mySharedDataArray.length;
      // 获取更新后索引对应的对象
      const nextData = mySharedDataArray[displayIndex];
      // 更改扩展程序图标的徽章文本
      // 注意：徽章文本最多为 4 个字符
      chrome.action.setBadgeText({ text: nextData.text.substring(0, 4) });
      // 更改扩展程序图标的徽章背景颜色
      chrome.action.setBadgeBackgroundColor({ color: nextData.color });


    // other功能的代码
  } else if (command === "start-action") {
    console.log("用户按下了 'start-action' 快捷键");
    // 执行开始新动作的代码
  }
});