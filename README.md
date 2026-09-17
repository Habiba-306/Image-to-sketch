# 🎨 Painter's Grid Assistant

Precision image grid overlay & pencil sketch generator for artists and painters.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-FFE165?style=flat&logo=python&logoColor=black)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat)

---

## 🎮 Overview

Painter's Grid Assistant overlays customizable grids and cell coordinates (A1, B2...) onto reference photos and pencil sketches. It enables quick, accurate scaling and transfer of reference artwork onto physical canvases.

---

## ✨ Features

- 📏 **Custom Grid System:** Adjust columns/rows (1–50), line thickness, opacity, and color.
- 🔤 **Smart Cell Labels:** High-contrast alphanumeric headers (Top columns A–Z, Left rows 1–N).
- ✏️ **Pencil Sketch View:** Instant sketch generator with adjustable blur strength.
- 🖼️ **Aspect-Ratio Fitting:** Clean canvas scaling with zero image cropping or distortion.
- 💾 **Export PNG & PDF:** Save full-resolution images or multi-page PDF documents.
- 🎛️ **Modern Dark UI:** Dynamic Tkinter desktop interface (#1a1a2e).

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
|-----------|----------|-------------|
| `apply_grid` | Grid Engine | Draws grid matrix & contrast text labels (A1, B2) |
| `create_sketch` | Sketch Engine | Inverted Gaussian blur division for pencil sketch effect |
| `fit_image` | Aspect Scaler | Fits image to display window preserving aspect ratio |
| `export_pdf` | PDF Exporter | Bundles processed images into multi-page PDF files |

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **GUI Framework:** Tkinter (ttk)
- **Computer Vision:** OpenCV (cv2) & NumPy
- **Image & PDF Export:** Pillow (PIL)

---

## 📝 License

Developed for artistic & educational projects. Free to use and modify.

---

⭐ **If you found this project helpful, consider giving it a star!**

---

## 📫 Connect

- **GitHub:** [Habiba-306](https://github.com/Habiba-306)
- **LinkedIn:** [habiba-javed](https://linkedin.com/in/habiba-javed)
- **Email:** [habibajaved150@gmail.com](mailto:habibajaved150@gmail.com)
