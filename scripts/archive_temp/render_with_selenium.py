from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, time

def render_html(html_path, png_path, width=1400, height=980):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f"--window-size={width},{height}")
    chrome_options.add_argument("--force-device-scale-factor=2")
    chrome_options.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("file:///" + os.path.abspath(html_path).replace("\\", "/"))
    time.sleep(1) # wait for fonts to settle
    driver.save_screenshot(png_path)
    driver.quit()
    print("Rendered PNG via Chrome Headless successfully!")

if __name__ == '__main__':
    render_html(
        r'E:\TestingProject\ảnh file docx\Hinh_2.1_Agile_Scrum_Workflow.html',
        r'E:\TestingProject\ảnh file docx\Hinh_2.1_Agile_Scrum_Workflow.png'
    )
