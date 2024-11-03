from tkinter import Tk, filedialog
from PIL import Image
import os


# 检查图片方向
def get_image_orientation(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return "landscape" if width > height else "portrait"


# 转换图片为WebP格式
def convert_to_webp(image_path, output_folder, max_pixels=178956970):
    try:
        with Image.open(image_path) as img:
            # 检查图片大小
            width, height = img.size
            if width * height > max_pixels:
                print(f"Skipping {image_path} because it exceeds the size limit.")
                return

            # 保存图片为WebP格式
            output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + ".webp")
            img.save(output_path, "webp")
            print(f"文件 {os.path.basename(image_path)} 转为 {os.path.basename(output_path)} 成功!")
    except Exception as e:
        print(f"Failed to convert {image_path}: {e}")


# 遍历文件夹中的图片
def process_images(input_folder, output_folder_landscape, output_folder_portrait):
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_folder, filename)
            orientation = get_image_orientation(image_path)
            try:
                if orientation == "landscape":
                    convert_to_webp(image_path, output_folder_landscape)
                else:
                    convert_to_webp(image_path, output_folder_portrait)
            except Exception as e:
                print(f"Error processing {image_path}: {e}. Skipping this image.")


root = Tk()
root.withdraw()

# 获取用户选择的输入目录
input_folder = filedialog.askdirectory(title="选择输入目录")
if not input_folder:
    print("未选择输入目录，程序退出。")
    exit()

# 获取用户选择的横向图片输出目录
output_folder_landscape = filedialog.askdirectory(title="选择横向图片输出目录")
if not output_folder_landscape:
    print("未选择横向图片输出目录，程序退出。")
    exit()

# 获取用户选择的纵向图片输出目录
output_folder_portrait = filedialog.askdirectory(title="选择纵向图片输出目录")
if not output_folder_portrait:
    print("未选择纵向图片输出目录，程序退出。")
    exit()

# 执行转换
process_images(input_folder, output_folder_landscape, output_folder_portrait)
