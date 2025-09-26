
(async function() {
  // 获取网页的标题
  const pageTitle = document.title;
  console.log('--- 脚本开始执行 --- ' + new Date().toLocaleTimeString());
  console.log('网页标题是：', pageTitle);
  console.log('=============\n');


  // 获取当前网页的域名
  const currentDomain = window.location.hostname;
  console.log('当前域名是：', currentDomain);
  let subjectElement = null;
  let downshowElement = null;

  // 根据域名选择不同的元素选择器==============
  //xxxx域名 内容选择
    if (currentDomain.includes('xxxxxxxxxxxxxxxxxxxx')) {
    // 获取 id 为 'thread_subject' 的元素
    subjectElement = document.getElementById('thread_subject');
    downshowElement = document.querySelector('.downshow');
    }

    else if (currentDomain.includes('dbbbbbbbbbb')) {
    subjectElement = document.querySelector('.post-title');
    downshowElement = document.getElementById('download-link');
    }
    else if (currentDomain.includes('ccccccccccc')) {
    subjectElement = document.querySelector('.post-title');
    downshowElement = document.getElementById('download-link');
    }
    else {
    console.log('当前域名没有匹配的规则，无法获取主题和地址。');
    }




  //====== 根据域名选择不同的元素选择器===============
  const subjectText = subjectElement ? subjectElement.textContent.trim() : null;
  const downshowText = downshowElement ? downshowElement.textContent.trim() : null;



  //从background.js 获取对应组别text
  const getResponse = await chrome.runtime.sendMessage({ action: "getGroup" });
  const groupText = getResponse ? getResponse.text : null;




  console.log('获取title:', subjectText);
  console.log('获取address:', downshowText);
  console.log('获取group:', groupText);
  console.log('domain:', currentDomain);
  // 将数据打包成一个 JavaScript 对象
  const dataToSend = {
    title: subjectText,
    downloadInfo: downshowText,
    group:groupText,
    domain:currentDomain
  };

// 指定发送的目标 URL
  const targetUrl = 'http://127.0.0.1:8899/api/data';

  try {
    // 使用 fetch() 发送 POST 请求
    const response = await fetch(targetUrl, {
      method: 'POST', // 指定为 POST 方法
      headers: {
        'Content-Type': 'application/json', // 设置请求头，告诉服务器数据格式为 JSON
      },
      body: JSON.stringify(dataToSend), // 将 JavaScript 对象转换为 JSON 字符串
    });


    if (response.ok) {
      console.log('数据发送成功！');
      // 可以选择处理服务器的响应
      // const result = await response.json();
      // console.log('服务器响应:', result);
    } else {
      console.log('数据发送失败:', response.statusText);
    }
  } catch (error) {
    console.log('发送请求时发生错误:', error);
  }
  
  console.log('--- 脚本执行完毕 ---');
})();