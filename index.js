require('dotenv').config()
const env = process.env || {};
const puppeteer = require('puppeteer');

(async () => {
  console.time('AutoSign'); 
  const browser = await puppeteer.launch({
    // args: ['--no-sandbox'],
    // headless: env.NODE_ENV === 'development' ? false : true,
    headless: false,
  });
  const page = await browser.newPage();

  console.log('[Sign] %s', '准备登录')
  await page.goto("https://www.hjtnt.link/auth/login");
  await page.type('#email', env?.EMAIL || '');
  await page.type('#password', env?.PASSWORD || '');
  await page.click('.login');

  console.log('[Sign] %s', '登录成功');

  const targets = await browser.targets();
  targets.map(async target => {
    const pageUrl = await target.url();
    console.log('[Sign] %s', pageUrl)
    if (pageUrl.indexOf('oauth.telegram.org/embed/') > -1) {
      const newBrowser = await target.browser();
      const newPage = await newBrowser.newPage();
      await newPage.goto('https://www.hjtnt.link/user');
      await newPage.waitForSelector('.breadcrumb-item > .btn');
      // TODO：newPage.click() 不能执行
      // 不能在无头模式中使用
      const ret = await newPage.evaluate(() => {
        const selector = document.querySelector('.breadcrumb-item > .btn');
        if (selector) {
          if (selector.textContent.trim() === '明日再来') {
            return Promise.resolve('今日已签到');
            
          } else {
            document.querySelector('.breadcrumb-item > .btn').click();
            return Promise.resolve('签到完成');
          }
        } else {
          return Promise.resolve('签到元素节点不存在');
        }
      });
      console.log('[Sign] %s', ret);
      await browser.close();
      console.timeEnd('AutoSign');
    }
  });
})();

process.on('uncaughtException', (err) => {
  console.log('[Sign] %s - %s', '捕获未知错误', err.message);
});
