import os
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
SOURCE_IMAGE = ROOT_DIR / "2026-06-02" / "sample.png"


def ensure_source_image() -> Path:
    if SOURCE_IMAGE.exists():
        return SOURCE_IMAGE

    synthetic = np.zeros((320, 320, 3), dtype=np.uint8)
    for i in range(320):
        synthetic[i, :, :] = (40 + i // 3, 80 + i // 4, 140)
    cv2.circle(synthetic, (95, 110), 45, (0, 255, 255), -1)
    cv2.rectangle(synthetic, (185, 60), (285, 150), (255, 80, 80), -1)
    cv2.line(synthetic, (30, 270), (290, 240), (255, 255, 255), 3)
    cv2.putText(
        synthetic,
        "CV",
        (115, 265),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.7,
        (20, 20, 20),
        4,
        cv2.LINE_AA,
    )
    fallback = SCRIPT_DIR / "sample_generated.png"
    cv2.imwrite(str(fallback), synthetic)
    return fallback


def add_gaussian_noise(img: np.ndarray, sigma: float = 18.0) -> np.ndarray:
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    noisy = img.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_salt_pepper_noise(img: np.ndarray, ratio: float = 0.02) -> np.ndarray:
    noisy = img.copy()
    h, w = noisy.shape[:2]
    total = int(h * w * ratio)
    ys = np.random.randint(0, h, total)
    xs = np.random.randint(0, w, total)
    half = total // 2
    noisy[ys[:half], xs[:half]] = 255
    noisy[ys[half:], xs[half:]] = 0
    return noisy


def save_four_panel(title: str, images: list[tuple[str, np.ndarray]], save_path: Path) -> None:
    plt.figure(figsize=(14, 8))
    plt.suptitle(title, fontsize=16)

    for idx, (name, img) in enumerate(images, start=1):
        plt.subplot(2, 2, idx)
        if img.ndim == 2:
            plt.imshow(img, cmap="gray")
        else:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(name)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", dpi=180)
    plt.close()


def save_five_panel(title: str, images: list[tuple[str, np.ndarray]], save_path: Path) -> None:
    plt.figure(figsize=(18, 4.8))
    plt.suptitle(title, fontsize=16)

    for idx, (name, img) in enumerate(images, start=1):
        plt.subplot(1, 5, idx)
        if img.ndim == 2:
            plt.imshow(img, cmap="gray")
        else:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(name)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", dpi=180)
    plt.close()


def normalize_to_uint8(img: np.ndarray) -> np.ndarray:
    normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return normalized.astype(np.uint8)


def non_maximum_suppression(grad_mag: np.ndarray, grad_dir: np.ndarray) -> np.ndarray:
    h, w = grad_mag.shape
    output = np.zeros((h, w), dtype=np.float32)
    angle = np.rad2deg(grad_dir) % 180

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            q = 0.0
            r = 0.0
            a = angle[y, x]

            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                q = grad_mag[y, x + 1]
                r = grad_mag[y, x - 1]
            elif 22.5 <= a < 67.5:
                q = grad_mag[y + 1, x - 1]
                r = grad_mag[y - 1, x + 1]
            elif 67.5 <= a < 112.5:
                q = grad_mag[y + 1, x]
                r = grad_mag[y - 1, x]
            elif 112.5 <= a < 157.5:
                q = grad_mag[y - 1, x - 1]
                r = grad_mag[y + 1, x + 1]

            if grad_mag[y, x] >= q and grad_mag[y, x] >= r:
                output[y, x] = grad_mag[y, x]

    return output


def generate_smoothing_comparison(img_bgr: np.ndarray) -> None:
    noisy = add_gaussian_noise(img_bgr, sigma=16.0)
    noisy = add_salt_pepper_noise(noisy, ratio=0.015)

    mean = cv2.blur(noisy, (5, 5))
    gaussian = cv2.GaussianBlur(noisy, (5, 5), 1.0)
    median = cv2.medianBlur(noisy, 5)

    save_four_panel(
        "Smoothing Filter Comparison",
        [
            ("Noisy Image", noisy),
            ("Mean Blur", mean),
            ("Gaussian Blur", gaussian),
            ("Median Blur", median),
        ],
        SCRIPT_DIR / "filter_smoothing_comparison.png",
    )


def generate_sobel_visualization(img_bgr: np.ndarray) -> None:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0.8)

    grad_x = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)
    grad_mag = cv2.magnitude(grad_x, grad_y)

    save_four_panel(
        "Sobel and Gradient Visualization",
        [
            ("Original Gray", gray),
            ("Gradient X", normalize_to_uint8(np.abs(grad_x))),
            ("Gradient Y", normalize_to_uint8(np.abs(grad_y))),
            ("Gradient Magnitude", normalize_to_uint8(grad_mag)),
        ],
        SCRIPT_DIR / "sobel_gradient_visualization.png",
    )


def generate_canny_pipeline(img_bgr: np.ndarray) -> None:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1.2)

    grad_x = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)
    grad_mag = cv2.magnitude(grad_x, grad_y)
    grad_dir = cv2.phase(grad_x, grad_y, angleInDegrees=False)
    nms = non_maximum_suppression(grad_mag, grad_dir)
    edges = cv2.Canny(gray, 80, 160)

    save_five_panel(
        "Canny Pipeline Visualization",
        [
            ("Original Gray", gray),
            ("Gaussian Blur", blur),
            ("Gradient Magnitude", normalize_to_uint8(grad_mag)),
            ("After NMS", normalize_to_uint8(nms)),
            ("Final Canny", edges),
        ],
        SCRIPT_DIR / "canny_pipeline_visualization.png",
    )


def main() -> None:
    np.random.seed(42)
    source_path = ensure_source_image()
    img_bgr = cv2.imread(str(source_path))
    if img_bgr is None:
        raise RuntimeError(f"Failed to read image: {source_path}")

    generate_smoothing_comparison(img_bgr)
    generate_sobel_visualization(img_bgr)
    generate_canny_pipeline(img_bgr)
    print("Generated filter_smoothing_comparison.png")
    print("Generated sobel_gradient_visualization.png")
    print("Generated canny_pipeline_visualization.png")


if __name__ == "__main__":
    main()
