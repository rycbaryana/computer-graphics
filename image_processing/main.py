import cv2
import tkinter as tk
from tkinter import Tk, Button, filedialog, Canvas, Menu
from PIL import Image, ImageTk


def blur(image):
    return cv2.blur(image, (5, 5))


def median_blur(image):
    return cv2.medianBlur(image, 5)


def bilateral_filter(image):
    return cv2.bilateralFilter(image, 9, 75, 75)


def linear_contrast(image):
    alpha = 1.75
    beta = 0
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def histogram_equalization(image):
    return cv2.merge(tuple(map(lambda x: cv2.equalizeHist(x), cv2.split(image))))


def hsv_histogram_equalization(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v_eq = cv2.equalizeHist(v)
    hsv_eq = cv2.merge((h, s, v_eq))
    return cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)


class ImageProcessor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing Application")

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image)
        self.file_menu.add_command(label="Reset", command=self.reset)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.column = 0

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.button_row = tk.Frame(self.frame)
        self.button_row.grid(row=0, column=0, columnspan=3, pady=10)

        self.add_button("Blur", self.process(blur))
        self.add_button("Median Blur", self.process(median_blur))
        self.add_button("Bilateral Filter", self.process(bilateral_filter))
        self.add_button("Linear Contrast", self.process(linear_contrast))
        self.add_button("Histogram Equalization", self.process(histogram_equalization))
        self.add_button("HSV Histogram Equalization", self.process(hsv_histogram_equalization))

        self.image = None
        self.processed_image = None
        self.filepath = None

        self.original_canvas = Canvas(self.frame, bg="lightgray", width=380, height=300)
        self.original_canvas.grid(row=1, column=0, rowspan=5, padx=10, pady=10)

        self.processed_canvas = Canvas(self.frame, bg="lightgray", width=380, height=300)
        self.processed_canvas.grid(row=1, column=1, rowspan=5, padx=10, pady=10)

    def add_button(self, text, func):
        button = Button(self.button_row, text=text, command=func)
        button.grid(row=0, column=self.column, padx=10, pady=10, sticky="ew")
        self.column += 1

    def reset(self):
        self.processed_image = None
        self.processed_canvas.delete('all')

    def open_image(self):
        self.filepath = filedialog.askopenfilename()
        self.image = cv2.imread(self.filepath)
        if self.image is not None:
            self.show_image(self.image, self.original_canvas)
            self.reset()

    def save_image(self):
        if self.processed_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if save_path:
                cv2.imwrite(save_path, self.processed_image)

    def show_image(self, img, canvas):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        img_pil = img_pil.resize((canvas_width, canvas_height))
        img_tk = ImageTk.PhotoImage(img_pil)

        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk

    def process(self, func):
        def inner():
            if self.processed_image is not None:
                self.processed_image = func(self.processed_image)
                self.show_image(self.processed_image, self.processed_canvas)
            elif self.image is not None:
                self.processed_image = func(self.image)
                self.show_image(self.processed_image, self.processed_canvas)

        return inner


if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x400")
    root.resizable(False, False)
    app = ImageProcessor(root)
    root.mainloop()
