import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# 获取当前脚本所在目录，确保图片保存在同级目录下
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def show_comparison(title, img_original, img_processed, save_filename):
    """
    生成 原图 vs 处理后的图 的双栏对比图，并保存到本地
    """
    # 如果是单通道掩膜图，转换为三通道以便与原图拼在一张画布上对比
    if len(img_processed.shape) == 2:
        img_processed = cv2.cvtColor(img_processed, cv2.COLOR_GRAY2BGR)

    # BGR -> RGB 转换
    img_orig_rgb = cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB)
    img_proc_rgb = cv2.cvtColor(img_processed, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 5))
    plt.suptitle(title, fontsize=16)

    # 左侧：原图
    plt.subplot(1, 2, 1)
    plt.imshow(img_orig_rgb)
    plt.title("Original")
    plt.axis("off")

    # 右侧：处理后的图
    plt.subplot(1, 2, 2)
    plt.imshow(img_proc_rgb)
    plt.title("Processed")
    plt.axis("off")

    plt.tight_layout()
    
    # 保存图片到脚本同级目录 (也就是博客的资源文件夹)
    save_path = os.path.join(SCRIPT_DIR, save_filename)
    plt.savefig(save_path, bbox_inches='tight', dpi=150)
    print(f"已保存对比图: {save_filename}")
    
    # plt.show() # 注释掉以防止阻塞自动化运行，读者下载后可自行取消注释
    plt.close()

def main():
    sample_path = os.path.join(SCRIPT_DIR, 'sample.png')
    if not os.path.exists(sample_path):
        print("未找到 sample.jpg，正在生成一张包含几何图形的测试图片...")
        test_img = np.zeros((300, 300, 3), dtype="uint8")
        # 绘制渐变背景
        for i in range(300):
            test_img[i, :, :] = (int(i*0.8), int(i*0.5), 150)
        # 画几个明显的几何图形，方便展示旋转和抠图效果
        cv2.circle(test_img, (150, 150), 80, (0, 255, 255), -1) # 黄色圆
        cv2.rectangle(test_img, (50, 50), (100, 100), (0, 0, 255), -1) # 红色矩形
        cv2.imwrite(sample_path, test_img)

    img_cv = cv2.imread(sample_path) 
    
    print("\n--- 4. 空间域数学操作复现 ---")
    
    # (1) 线性变换（亮度和对比度）与防溢出截断
    alpha = 1.5  
    beta = 50    
    adjusted_img = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=beta)
    show_comparison("Linear Transform (Alpha=1.5, Beta=50)", img_cv, adjusted_img, "demo_linear.png")

    # (2) Gamma 非线性校正
    gamma = 0.5  
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected = cv2.LUT(img_cv, table)
    show_comparison("Gamma Correction (Gamma=0.5)", img_cv, gamma_corrected, "demo_gamma.png")

    # (3) 仿射变换（旋转与插值）
    (h, w) = img_cv.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated_img = cv2.warpAffine(img_cv, M, (w, h), flags=cv2.INTER_LINEAR)
    show_comparison("Affine Transform (Rotate 45 Deg)", img_cv, rotated_img, "demo_affine.png")

    # (4) 逻辑掩膜（Masking）提取 ROI
    mask = np.zeros(img_cv.shape[:2], dtype="uint8")
    cv2.circle(mask, center, min(w, h) // 4, 255, -1)
    roi_img = cv2.bitwise_and(img_cv, img_cv, mask=mask)
    show_comparison("Bitwise AND (ROI Extraction)", img_cv, roi_img, "demo_roi.png")
    
    print("\n所有图像操作及可视化图片保存完毕！")

if __name__ == "__main__":
    main()