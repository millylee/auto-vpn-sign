const env = process.env || {};
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  // 标签页变化
  browser.on('targetchanged', async target => {
    const newPage = await target.page();
    // url变化
    newPage.on('framenavigated', async () => {
      await newPage.waitForSelector('.breadcrumb-item > .btn');
      if (newPage.url().indexOf('/user')) {
        // TODO: newPage.click() 适配方法
        await newPage.evaluate(() => {
          document.querySelector('.breadcrumb-item > .btn').click();
        });
        console.log('签到完成');
        await browser.close();
      }
    });
  });
  try {
    console.time('OpenLoginPage');
    const page = await browser.newPage();
    await page.goto('https://www.hjtnt.link/auth/login');
    console.timeEnd('OpenLoginPage');
    console.time('AutoLogin');

    await page.type('#email', env?.EMAIL || '');
    await page.type('#password', env?.PASSWORD || '');

    const [response] = await Promise.all([
      page.waitForNavigation(),
      page.click('.login'),
    ]);
    await response;
    console.log('填写邮箱与密码并进行登录');
  } catch (error) {
    console.log('签到出错', error);
    await browser.close();
  }
})();

process.on('exit', (error) => {
  console.log('异常退出：' + error)
});