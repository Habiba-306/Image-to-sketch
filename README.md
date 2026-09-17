# 🎨 Painter's Grid Assistant

> **Precision image grid overlay & pencil sketch generator for artists and painters.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F61?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-28A745?style=for-the-badge)

---

## 🎮 Overview

**Painter's Grid Assistant** overlays customizable grids and cell coordinates (**A1, B2...**) onto reference photos and pencil sketches. It enables quick, accurate scaling and transfer of reference artwork onto physical canvases.

---

## ✨ Features

- 📏 **Custom Grid System**: Adjust columns/rows (1–50), line thickness, opacity, and color.
- 🔤 **Smart Cell Labels**: High-contrast alphanumeric headers (Top columns A–Z, Left rows 1–N).
- ✏️ **Pencil Sketch View**: Instant sketch generator with adjustable blur strength.
- 🖼️ **Aspect-Ratio Fitting**: Clean canvas scaling with zero image cropping or distortion.
- 💾 **Export PNG & PDF**: Save full-resolution images or multi-page PDF documents.
- 🎛️ **Modern Dark UI**: Dynamic Tkinter desktop interface (`#1a1a2e`).

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install opencv-python numpy pillow
```

### 2. Run Application
```bash
python image_sketch.py
```

### 3. Simple Workflow
```
[ Load Image ] ➔ [ Set Grid & Sketch ] ➔ [ Process ] ➔ [ Save PNG / Export PDF ]
```

---

## 📁 Project Structure

```
image_to_sketch/
├── image_sketch.py         # Main Tkinter app & processing engine
├── original_with_grid.png  # Export sample: Photo with grid
├── sketch_with_grid.png    # Export sample: Sketch with grid
└── README.md               # Project documentation
```

---

## ⚙️ Core Architecture

| Component | Function | Description |
| :--- | :--- | :--- |
| [`apply_grid`](file:///c:/Users/PMYLS/OneDrive%20-%20Higher%20Education%20Commission/Desktop/habibaa/project%20AI/venv/image_to_sketch/image_sketch.py#L18-L65) | Grid Engine | Draws grid matrix & contrast text labels (`A1`, `B2`) |
| [`create_sketch`](file:///c:/Users/PMYLS/OneDrive%20-%20Higher%20Education%20Commission/Desktop/habibaa/project%20AI/venv/image_to_sketch/image_sketch.py#L76-L82) | Sketch Engine | Inverted Gaussian blur division for pencil sketch effect |
| [`fit_image`](file:///c:/Users/PMYLS/OneDrive%20-%20Higher%20Education%20Commission/Desktop/habibaa/project%20AI/venv/image_to_sketch/image_sketch.py#L68-L73) | Aspect Scaler | Fits image to display window preserving aspect ratio |
| [`export_pdf`](file:///c:/Users/PMYLS/OneDrive%20-%20Higher%20Education%20Commission/Desktop/habibaa/project%20AI/venv/image_to_sketch/image_sketch.py#L85-L89) | PDF Exporter | Bundles processed images into multi-page PDF files |

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (`ttk`)
- **Computer Vision**: OpenCV (`cv2`) & NumPy
- **Image & PDF Export**: Pillow (`PIL`)

---

## 📝 License

Developed for artistic & educational projects. Free to use and modify.
