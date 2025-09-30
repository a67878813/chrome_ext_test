
(async function() {
  let subjectElement = null;
  let downshowElement = null;
  let subjectText =null;
  let downshowText=null;
  let groupText;
  let  currentDomain;

  try {

  // 获取网页的标题
  const pageTitle = document.title;
  console.log('--- 脚本开始执行 --- ' + new Date().toLocaleTimeString());
  console.log('网页标题是：', pageTitle);
  console.log('=============\n');

//   let subjectText ; 
//   let downshowText;

  // 获取当前网页的域名
  currentDomain = window.location.hostname;
  //console.log('当前域名是：', currentDomain);

  // 根据域名选择不同的元素选择器==============
  //shuangxiugu 内容选择
    if (currentDomain.includes('111')) {
    // 获取 id 为 'thread_subject' 的元素
        subjectElement = document.getElementById('thread_subject');
        downshowElement = document.querySelector('.downshow');
        subjectText = subjectElement ? subjectElement.textContent.trim() : 'null';
        downshowText = downshowElement ? downshowElement.textContent.trim() : 'null';
    }

    else if (currentDomain.includes('222')) {
        subjectElement = document.querySelector('.post-title');
        downshowElement = document.getElementById('download-link');
        subjectText = subjectElement ? subjectElement.textContent.trim() : 'null';
        downshowText = downshowElement ? downshowElement.textContent.trim() : 'null';
    }
    else if (currentDomain.includes('333')) {
        //subjectElement = document.querySelector('.post-title');
        // 提前定义数组，用于存储提取到的信息
        //let linkData = [];

        // 使用 document.querySelectorAll 找到所有符合条件的链接
        // 选择器: 找到所有 <a> 标签，其子元素包含 <strong>
        // 这样可以避免依赖变化的 p:nth-child 序号
        const allLinks = document.querySelectorAll('a > strong');
        // 遍历所有找到的匹配元素
        allLinks.forEach(strongElement => {
            // 确保 strongElement 的父元素是 <a> 标签
            const anchorElement = strongElement.closest('a');
            if (anchorElement && anchorElement.href) {
                if (anchorElement.href.includes('pan.baidu')) {
                    // 如果 URL 包含 'pan.baidu'，则创建 link 对象
                    const link = {
                        url: anchorElement.href,
                        text: strongElement.textContent.trim()
                    };
                    downshowElement=anchorElement.href
                    // 将数据推入数组
                    //linkData.push(link);
                }
            }
        });

        downshowText = downshowElement ;
    }
    else {
    console.log('当前域名没有匹配的规则，无法获取主题和地址。');
    }
    //  // 根据域名选择不同的元素选择器==============


  //获取group 
  const getResponse = await chrome.runtime.sendMessage({ action: "getGroup" });
  groupText = getResponse ? getResponse.text : 'null';
  //console.log(groupText)



  console.log('获取title:',  subjectText ); 
  console.log('获取address:', downshowText);
  console.log('获取group:', groupText);
  console.log('domain:', currentDomain);
  // 将数据打包成一个 JavaScript 对象
  const dataToSend = {
    title: subjectText|| 'null',
    downloadInfo: downshowText|| 'null',
    group:groupText|| 'null',
    domain:currentDomain|| 'null'
  };


// 指定发送的目标 URL
  const targetUrl = 'http://127.0.0.1:8899/api/data';


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