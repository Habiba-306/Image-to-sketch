import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label, Entry, messagebox

# Overlay the grid on the image
def overlay_grid(image, grid_width, grid_height):
    height, width = image.shape[:2]
    box_width, box_height = width // grid_width, height // grid_height

    for i in range(1, grid_width):
        cv2.line(image, (i * box_width, 0), (i * box_width, height), (0, 0, 255), 2)
    for j in range(1, grid_height):
        cv2.line(image, (0, j * box_height), (width, j * box_height), (0, 0, 255), 2)

# Sketch effect function
def create_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (111, 111), 0)
    inverted_blurred = 255 - blurred
    return cv2.divide(gray, inverted_blurred, scale=256.0)

# Load and process the image
def load_image():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.png")])
    if not image_path: return

    img = cv2.imread(image_path)
    if img is None: return

    # Resize image to a reasonable size (max width 800px)
    max_width = 800
    aspect_ratio = img.shape[1] / img.shape[0]
    img = cv2.resize(img, (max_width, int(max_width / aspect_ratio)))

    try:
        grid_width = int(grid_width_entry.get())
        grid_height = int(grid_height_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid grid dimensions.")
        return

    # Apply sketch effect
    sketch_img = create_sketch(img.copy())

    # Apply grid on sketch and original
    overlay_grid(img, grid_width, grid_height)
    overlay_grid(sketch_img, grid_width, grid_height)

    # Display and save images
    cv2.imshow("Original with Grid", img)
    cv2.imshow("Sketch with Grid", sketch_img)
    cv2.imwrite("original_with_grid.jpg", img)
    cv2.imwrite("sketch_with_grid.jpg", sketch_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Tkinter setup
root = Tk()
root.title("Image Grid and Sketch")

Button(root, text="Load Image", command=load_image).pack(pady=10)

Label(root, text="Grid Width (boxes)").pack()
grid_width_entry = Entry(root)
grid_width_entry.insert(0, "10")
grid_width_entry.pack(pady=5)

Label(root, text="Grid Height (boxes)").pack()
grid_height_entry = Entry(root)
grid_height_entry.insert(0, "8")
grid_height_entry.pack(pady=5)

root.mainloop()
