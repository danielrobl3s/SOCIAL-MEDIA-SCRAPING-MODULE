from PIL import Image
from cdriver import Driver

driver = Driver.get('https://tiktok.com/@sabrinacarpenter', headless=True)

driver.save_screenshot('ss.png')

screenshot = Image.open('ss.png')

screenshot.show()