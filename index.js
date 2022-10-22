const env = process.env || {};
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  console.time('OpenLoginPage');
  await page.goto('https://www.hjtnt.link/auth/login');
  console.timeEnd('OpenLoginPage');
  console.time('AutoLogin');

  await page.type('#email', env?.EMAIL || '');
  await page.type('#password', env?.PASSWORD || '');
  await page.click('.login');
  console.timeEnd('AutoLogin');
  console.log('填写邮箱与密码并进行登录');

  console.time('AutoSign');
  const signSelector = await page.$('.breadcrumb-item > a');
  if (signSelector) {
    await page.click('.breadcrumb-item > a');
  }
  console.timeEnd('AutoSign');
  console.log('签到完成');

  await browser.close();
})();