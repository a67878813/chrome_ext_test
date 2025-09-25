
(async function() {
  // 获取网页的标题
  const pageTitle = document.title;
  console.log('--- 脚本开始执行 --- ' + new Date().toLocaleTimeString());
  console.log('网页标题是：', pageTitle);
  console.log('=============\n');

  // 获取 id 为 'thread_subject' 的元素
  const subjectElement = document.getElementById('thread_subject');
  const downshowElement = document.querySelector('.downshow');


  const subjectText = subjectElement ? subjectElement.textContent.trim() : null;
  const downshowText = downshowElement ? downshowElement.textContent.trim() : null;

  console.log('获取title:', subjectText);
  console.log('获取address:', downshowText);

  // 将数据打包成一个 JavaScript 对象
  const dataToSend = {
    title: subjectText,
    downloadInfo: downshowText
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
      console.error('数据发送失败:', response.statusText);
    }
  } catch (error) {
    console.error('发送请求时发生错误:', error);
  }

  
  console.log('--- 脚本执行完毕 ---');
})();