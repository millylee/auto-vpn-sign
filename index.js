const env = process.env || {};
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  // 标签页变化
  browser.on('targetchanged', async target => {
    const newPage = await target.page();
    // url变化
    newPage.on('framenavigated', async () => {
      if (newPage.url().indexOf('/user') && browser.isConnected) {
        await newPage.waitForSelector('.breadcrumb-item > .btn');
        // TODO: newPage.click() 适配方法
        await newPage.evaluate(async () => {
          const selector = document.querySelector('.breadcrumb-item > .btn');
          if (selector) {
            if (selector.textContent.trim() === '明日再来') {
              console.log('[Sign] %s', '今日已签到');
            } else {
              document.querySelector('.breadcrumb-item > .btn').click();
              console.log('[Sign] %s', '签到完成');
            }
          } else {
            console.log('[Sign] %s', '签到元素节点不存在');
          }
        });
        await browser.close();
      }
    });
  });
  try {
    if( browser.isConnected) {
      console.time('OpenLoginPage');
      const page = await browser.newPage();
      await page.goto('https://www.hjtnt.link/auth/login');
      console.timeEnd('OpenLoginPage');

      await page.type('#email', env?.EMAIL || '');
      await page.type('#password', env?.PASSWORD || '');

      const [response] = await Promise.all([
        page.waitForNavigation(),
        page.click('.login'),
      ]);
      await response;
      console.log('填写邮箱与密码并进行登录');
    }
  } catch (error) {
    console.log('签到出错', error.message);
    if (browser.isConnected) {
      await browser.close();
    }
  }
})();

process.on('exit', (code) => {
  console.log('异常退出：' + code)
});