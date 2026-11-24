const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const url = 'https://kimminseong.github.io/ai-course/week13/split/';

  async function runTest(amount, people) {
    console.log(`\n--- Testing with Amount: "${amount}", People: "${people}" ---`);
    await page.goto(url);

    // Fill amount
    const amountInput = page.locator('#amount');
    await amountInput.fill(amount.toString());

    // Fill people
    const peopleInput = page.locator('#people');
    await peopleInput.fill(people.toString());

    // Wait for potential calculation
    await page.waitForTimeout(500);

    // Get result
    const resultText = await page.locator('#result').innerText();
    console.log(`Result: ${resultText}`);
    return resultText;
  }

  try {
    // 1. 금액 17000, 인원수 3
    const res1 = await runTest(17000, 3);

    // 2. 인원수에 0
    const res2 = await runTest(17000, 0);

    // 3. 금액 비우기
    // For empty value, we need to handle it differently since .fill('') might behave differently
    await page.goto(url);
    const amountInput = page.locator('#amount');
    await amountInput.fill('');
    const peopleInput = page.locator('#people');
    await peopleInput.fill('3');
    await page.waitForTimeout(500);
    const resultText3 = await page.locator('#result').innerText();
    console.log(`\n--- Testing with Amount: "", People: "3" ---`);
    console.log(`Result: ${resultText3}`);

  } catch (error) {
    console.error('Error during testing:', error);
  } finally {
    await browser.close();
  }
})();
