# 🎨 Pencil Sketch & Grid Overlay Tool

A lightweight Python desktop application built with **OpenCV** and **Tkinter** that converts your photos into beautiful pencil sketches and overlays a customizable drawing grid. Perfect for artists, hobbyists, and portrait sketchers who use the grid method to scale and draw references manually!

---

## ✨ Features

* **Instant Pencil Sketch:** Uses grayscale conversion, image inversion, Gaussian blurring, and color division to generate clean, authentic-looking pencil sketches from your digital photos.
* **Custom Reference Grids:** Specify exactly how many columns and rows you want to split your canvas into.
* **Side-by-Side Comparison:** Renders both your original photo (with grid) and the pencil sketch output (with grid) simultaneously.
* **Auto-Resizing & Exporting:** Automatically scales large images down to a manageable 800px width while preserving aspect ratios, and instantly saves your outputs to your local directory.

---

## 🛠️ Prerequisites & Installation

Ensure you have **Python 3.8+** installed on your machine.

### 1. Setup Your Environment

Create your project directory and save the script inside it as `image_sketch.py`.

### 2. Install Dependencies

Install the required computer vision and numerical libraries via `pip`:

```bash
pip install opencv-python numpy

```

*(Note: `tkinter` is built directly into the standard Python library and does not require manual installation).*

---

## 🚀 Usage

Launch the GUI interface directly from your command line:

```bash
python image_sketch.py

```

### Modes of Operation:

1. **Set Grid Dimensions:** Enter your target **Grid Width** (columns) and **Grid Height** (rows) into the input fields. *(Defaults are set to 10x8)*.
2. **Load Image:** Click the **Load Image** button to open your native file explorer. Select any `.jpg` or `.png` file.
3. **View & Export:** The app automatically generates and displays two new preview windows. Close the preview windows (or press any key while focused on them) to finish. Outputs are automatically saved to your folder as:
* `original_with_grid.jpg`
* `sketch_with_grid.jpg`



---

## 📂 Code Structure

* **`overlay_grid(image, grid_width, grid_height)`**: Computes cell spacing dynamically based on canvas bounds and draws proportional red reference dividers.
* **`create_sketch(img)`**: Applies the mathematical image processing pipeline (Grayscale $\rightarrow$ Invert $\rightarrow$ GaussianBlur $\rightarrow$ Color Dodge / Divide) to generate the line art effect.
* **`load_image()`**: Handles dynamic resizing logic, validation checks, GUI popup bindings, and auto-export handlers.

---

## 📝 License

This project is developed for academic purposes at the University of Haripur.
All rights reserved © .
