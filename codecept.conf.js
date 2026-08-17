const { setHeadlessWhen, setCommonPlugins } = require('@codeceptjs/configure');

// Bật chế độ headless khi có biến môi trường HEADLESS=true
setHeadlessWhen(process.env.HEADLESS);

// Bật các plugin phổ biến của CodeceptJS
setCommonPlugins();

/** @type {CodeceptJS.MainConfig} */
exports.config = {
  name: 'yiyi-bookstore-e2e',
  tests: './e2e/tests/*_test.js',
  output: './output',
  helpers: {
    Playwright: {
      url: process.env.BASE_URL || 'http://localhost:5173',
      show: process.env.HEADLESS !== 'true',
      browser: 'chromium',
      waitForTimeout: 5000,
      waitForNavigation: 'load',
      windowSize: '1280x800',
      getPageTimeout: 30000,
      waitForAction: 500
    },
    REST: {
      endpoint: process.env.API_URL || 'http://localhost:8081/api',
      defaultHeaders: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    },
    CustomHelper: {
      require: './e2e/helpers/custom_helper.js'
    }
  },
  include: {
    I: './steps_file.js',
    authPage: './e2e/pages/authPage.js',
    productPage: './e2e/pages/productPage.js',
    cartPage: './e2e/pages/cartPage.js',
    aiChatPage: './e2e/pages/aiChatPage.js'
  },
  plugins: {
    screenshotOnFail: {
      enabled: true,
      uniqueNames: true
    },
    retryFailedStep: {
      enabled: true,
      retries: 2
    },
    tryTo: {
      enabled: true
    },
    eachElement: {
      enabled: true
    },
    stepByStepReport: {
      enabled: false,
      deleteSuccessful: true,
      screenshotsForAllItems: false
    }
  },
  bootstrap: null,
  teardown: null,
  hooks: []
};
