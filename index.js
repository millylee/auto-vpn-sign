require('dotenv').config()
const env = process.env || {};
const puppeteer = require('puppeteer');

(async () => {
  console.time('AutoSign');
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto("https://www.hjtnt.link/auth/login");
  await page.type('#email', env?.EMAIL || '');
  await page.type('#password', env?.PASSWORD || '');
  await page.click('.login');
  const targets = await browser.targets();
  targets.map(async target => {
    const pageUrl = await target.url();
    if (pageUrl.indexOf('oauth.telegram.org/embed/') > -1) {
      const newBrowser = await target.browser();
      const newPage = await newBrowser.newPage();
      await newPage.goto('https://www.hjtnt.link/user');
      await newPage.waitForSelector('.breadcrumb-item > .btn');
      // TODO：newPage.click() 不能执行
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

process.on('exit', (code) => {
  if (code !== 0) {
    console.log('异常退出：' + code)
  }
});
