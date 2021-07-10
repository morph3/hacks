import asyncio
from pyppeteer import launch
import time


async def auto_scroll(page):
    await page.evaluate("""
var foo = async function(){
    let height = document.body.scrollHeight;
    while(height > 0){
        window.scrollBy(0,40);
        height -= 40;
        const foo = await new Promise(resolve => setTimeout(resolve, 10));
    }
}
foo();
""",force_expr=True)
    return

async def get_urls_on_page(page):
    urls = await page.evaluate("""
    async () => {
    let urls = []; 
    let elements = document.getElementsByClassName("lazyloaded"); 

    for (var e of elements) { 
        let url = e.getAttribute("data-src"); 
        console.log(url);
        urls.push(url); 
    }

    return urls; // ret urls
    }
    """)
    return urls

async def main():
    root_url = ''
    browser = await launch({'headless':False, 'devtools':True})
    page = await browser.newPage()
    await page.goto(root_url)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
    
    for i in range(1,100):
        await page.goto(f"{root_url}?page={str(i)}")
        await auto_scroll(page)
        urls = await get_urls_on_page(page)
        for u in urls:
            print(u)
    #await browser.close()
    time.sleep(10000)

asyncio.get_event_loop().run_until_complete(main())


