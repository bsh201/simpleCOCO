import tkinter as tk
import tkinter.filedialog as fd

import json
import cv2

from PIL import Image, ImageTk

window = tk.Tk()

windows_width = window.winfo_screenwidth()
windows_height = window.winfo_screenheight()

app_width = 600
app_height = 600

center_width = (windows_width - app_width) // 2
center_height = (windows_height - app_height) // 2

window.title("Labeling Tool")
window.geometry(f"{app_width}x{app_height}+{center_width}+{center_height}")
window.resizable(False, False)

image = None
bounding_boxes = []
tk_image = None

#버튼 동작
def openFile():
    global image, bounding_boxes
    fpath = fd.askopenfilename()
    if fpath:
        image = cv2.imread(fpath)
        bounding_boxes = []
        draw_image(image)

def downFile() :
    global image
    if image is not None:
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, image)

def saveCOCO():
    global bounding_boxes
    if bounding_boxes:
        file_path = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            coco_format(file_path)

def closeCV():
    cv2.destroyAllWindows()
    show_image_in_tkinter(image, bounding_boxes)

#bbox 그리기
def draw_image(image):
    cv2.imshow("image", image)
    cv2.setMouseCallback("image", draw_rectangle)

def draw_rectangle(event, x, y, flags, param):
    global image, bounding_boxes
    if event == cv2.EVENT_LBUTTONDOWN:
        bounding_boxes.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        bounding_boxes[-1] = (bounding_boxes[-1], (x, y))
        draw_bounding_box(image, bounding_boxes)

def draw_bounding_box(image, bounding_boxes):
    image_copy = image.copy()
    for bbox in bounding_boxes:
        start_point, end_point = bbox
        cv2.rectangle(image_copy, start_point, end_point, (0, 255, 0), 2)
    cv2.imshow("image", image_copy)

def show_image_in_tkinter(image, bounding_boxes):
    global tk_image

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    tk_image = ImageTk.PhotoImage(pil_image)

    canvas = tk.Canvas(window, width=pil_image.width, height=pil_image.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.pack()

    for bbox in bounding_boxes:
        start_point, end_point = bbox
        canvas.create_rectangle(start_point[0], start_point[1], end_point[0], end_point[1], outline="red", width=2)

##코코 데이터셋
def coco_format(file_path):
    global bounding_boxes
    coco_data = {
        "info": {
            "description": "Simple COCO Face detection data",
        },
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "face"}]
    }

    for idx, bbox in enumerate(bounding_boxes):
        start_point, end_point = bbox
        width = end_point[0] - start_point[0]
        height = end_point[1] - start_point[1]
        annotation = {
            "id": idx + 1,
            "image_id": 1,
            "category_id": 1,
            "bbox": [start_point[0], start_point[1], width, height],
            "area": width * height,
            "iscrowd": 0
        }

        coco_data["annotations"].append(annotation)

    with open(file_path, "w") as json_file:
        json.dump(coco_data, json_file, indent=4)

getPhoto_btn = tk.Button(window, text="파일 불러오기", command=openFile, padx=10, pady=5)
downPhoto_btn = tk.Button(window, text="파일 다운하기", command=downFile, padx=10, pady=5)
closeCV_btn = tk.Button(window, text="B-Box 편집 완료", command = closeCV, padx=10, pady=5)
saveCOCO_btn = tk.Button(window, text="COCO 포맷으로 저장", command=saveCOCO, padx=10, pady=5)

getPhoto_btn.pack(side="top", anchor="nw", ipady=1)
downPhoto_btn.pack(side="top", anchor="nw", ipady=1)
saveCOCO_btn.pack(side="bottom", anchor="se", ipady=1)
closeCV_btn.pack(side="bottom", anchor="se", ipady=1)

window.mainloop()
