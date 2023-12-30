import customtkinter as ctk
import tkinter as tk
import json
import os

from PIL import Image

ctk.set_appearance_mode('Light')
ctk.set_default_color_theme('green')

app = ctk.CTk()
app.geometry("1300x850")

popup = True

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

LARGE_LABEL_FONT = ctk.CTkFont(size=60)
MID_LABEL_FONT = ctk.CTkFont(size=42)
SMALL_LABEL_FONT = ctk.CTkFont(size=28)
BUTTON_FONT = ctk.CTkFont(size=24)
BIG_BUTTON_FONT = ctk.CTkFont(size=36)

QUESTION_COLOR = '#EE8888'
ANSWER_COLOR = '#2CC985'

def load_questions(datapath):
    with open(datapath, 'r') as f:
        data = json.load(f)
    data = dict(data)
    categories = list(data.keys())
    for cat in categories:
        for qu in data[cat]:
            data[cat][qu]['done'] = False
    return data, categories

data, categories = load_questions('./game.json')

# print(data)
num_cats = len(categories)

mainframe = ctk.CTkFrame(master=app)
mainframe.pack(pady=20, padx=20, fill='both', expand=True)

frames = []
labels = []
qs = []
for i in range(num_cats):
    qs.append([])

def main_view():
    global mainframe
    mainframe.destroy()
    mainframe = ctk.CTkFrame(master=app)
    mainframe.pack(pady=20, padx=20, fill='both', expand=True)

    frames = []
    labels = []
    qs = []
    for i in range(num_cats):
        qs.append([])

    for i in range(num_cats):
        frames.append(ctk.CTkFrame(master=mainframe))
        frames[i].pack(padx=15, pady=15, side='left', expand = True, fill = 'both')

        labels.append(ctk.CTkLabel(master=frames[i], justify=tk.LEFT, text = categories[i], font=SMALL_LABEL_FONT))
        labels[i].pack(padx=10, pady=20)

        for j in range(len(data[categories[i]].keys())):
            if not data[categories[i]][str((j+1)*100)]["done"]:
                qs[i].append(ctk.CTkButton(master=frames[i], 
                                            state=tk.NORMAL, 
                                            text=str((j+1)*100), 
                                            font=BIG_BUTTON_FONT, 
                                            width = 170, 
                                            height = 75))
            else:
                qs[i].append(ctk.CTkButton(master=frames[i], 
                                            state=tk.DISABLED, 
                                            text=str((j+1)*100), 
                                            font=BIG_BUTTON_FONT, 
                                            width = 170, 
                                            height = 75, 
                                            fg_color='#EE8888'))
            qs[i][j].bind("<Button-1>", show_q)
            qs[i][j].pack(padx=10, pady=28)
            info = {
                'cat': categories[i],
                'q': data[categories[i]][str((j+1)*100)]['question'],
                'a': data[categories[i]][str((j+1)*100)]['answer'],
                'val': str((j+1)*100),
                'img': data[categories[i]][str((j+1)*100)]['images'],
                'type': data[categories[i]][str((j+1)*100)]['type'],
                'audio': data[categories[i]][str((j+1)*100)]['type']
            }
            qs[i][j].info = info
            qs[i][j]._canvas.info = info
            qs[i][j]._text_label.info = info

def show_q(event):
    if data[event.widget.info['cat']][event.widget.info['val']]['done']:
        return
    # print(event.widget.info['type'])
    if event.widget.info['type'] == 'image':
        image_question(event.widget.info)
    elif event.widget.info['type'] == 'audio':
        pass
        # audio_question()
    else:
        global mainframe
        mainframe.destroy()
        mainframe = ctk.CTkFrame(master=app)
        mainframe.pack(pady=20, padx=20, fill='both', expand=True)

        frame_around_label = ctk.CTkFrame(master=mainframe)
        frame_around_label.pack(pady = 15)

        cat_label = ctk.CTkLabel(master = frame_around_label, 
                                justify=tk.CENTER, 
                                text = event.widget.info['cat'] + ' - ' + event.widget.info['val'], 
                                font=SMALL_LABEL_FONT)
        cat_label.pack(padx = 5, pady = 5)

        q_label = ctk.CTkLabel(master = mainframe, 
        justify=tk.CENTER, 
        text = event.widget.info['q'], 
        font=MID_LABEL_FONT,
        text_color=QUESTION_COLOR)
        q_label.pack(padx = 20, pady = 10)

        cont = ctk.CTkButton(master=mainframe, text = 'Antwort', font = BUTTON_FONT)
        cont.pack(padx = 20, pady = 40)
        cont.bind('<Button-1>', show_ans)
        cont.info = event.widget.info
        cont._canvas.info = event.widget.info
        cont._text_label.info = event.widget.info
        

def image_question(info):

    global mainframe
    mainframe.destroy()
    mainframe = ctk.CTkFrame(master=app)
    mainframe.pack(pady=20, padx=20, fill='both', expand=True)

    frame_around_label = ctk.CTkFrame(master=mainframe)
    frame_around_label.pack(pady = 15)

    cat_label = ctk.CTkLabel(master = frame_around_label, justify=tk.CENTER, text = info['cat'] + ' - ' + info['val'], font=SMALL_LABEL_FONT)
    cat_label.pack(padx = 20, pady = 15)

    q_label = ctk.CTkLabel(master = mainframe, justify=tk.CENTER, text = info['q'], font=MID_LABEL_FONT, text_color=QUESTION_COLOR)
    q_label.pack(padx = 20, pady = 10)


    q_image = ctk.CTkImage(Image.open(os.path.join(info['img'], 'crop.jpg')), size=(350, 350))
    img_canvas = ctk.CTkLabel(master = mainframe, text = '', image = q_image)

    img_canvas.pack(padx=15, pady=15)

    cont = ctk.CTkButton(master=mainframe, text = 'Antwort', font=BUTTON_FONT)
    cont.pack(padx = 20, pady = 40)
    cont.bind('<Button-1>', show_ans_image)
    cont.info = info
    cont._canvas.info = info
    cont._text_label.info = info

def show_ans(event):
    info = event.widget.info
    data[info['cat']][info['val']]['done'] = True
    global mainframe
    mainframe.destroy()
    mainframe = ctk.CTkFrame(master=app)
    mainframe.pack(pady=20, padx=20, fill='both', expand=True)

    frame_around_label = ctk.CTkFrame(master=mainframe)
    frame_around_label.pack(pady = 15)

    cat_label = ctk.CTkLabel(master = frame_around_label, justify=tk.CENTER, text = info['cat'] + ' - ' + info['val'], font=SMALL_LABEL_FONT)
    cat_label.pack(padx = 20, pady = 15)

    q_label = ctk.CTkLabel(master = mainframe, justify=tk.CENTER, text = info['q'], font=MID_LABEL_FONT, text_color=QUESTION_COLOR)
    q_label.pack(padx = 20, pady = 10)

    frame_around_ans = ctk.CTkFrame(master=mainframe)
    frame_around_ans.pack(pady = 15)

    ans_label = ctk.CTkLabel(master = frame_around_ans, justify=tk.CENTER, text = 'Antwort: ', font=LARGE_LABEL_FONT)
    ans_label.pack(padx = 20, pady = 20)

    a_label = ctk.CTkLabel(master = mainframe, justify=tk.CENTER, text = info['a'], font=MID_LABEL_FONT, text_color=ANSWER_COLOR)
    a_label.pack(padx = 10, pady = 20)

    ret_button = ctk.CTkButton(master=mainframe, text = 'Weiter', font = BUTTON_FONT)
    ret_button.pack(pady = 30)
    ret_button.bind('<Button-1>', main_view_call)

def main_view_call(event):
    main_view()

def show_ans_image(event):
    info = event.widget.info
    data[info['cat']][info['val']]['done'] = True
    global mainframe
    mainframe.destroy()
    mainframe = ctk.CTkFrame(master=app)
    mainframe.pack(pady=20, padx=20, fill='both', expand=True)

    frame_around_label = ctk.CTkFrame(master=mainframe)
    frame_around_label.pack(pady = 15)

    cat_label = ctk.CTkLabel(master = frame_around_label, justify=tk.CENTER, text = info['cat'] + ' - ' + info['val'], font=SMALL_LABEL_FONT)
    cat_label.pack(padx = 20, pady = 15)

    q_label = ctk.CTkLabel(master = mainframe, justify=tk.CENTER, text = info['q'], font=MID_LABEL_FONT, text_color=QUESTION_COLOR)
    q_label.pack(padx = 20, pady = 10)

    frame_around_ans = ctk.CTkFrame(master=mainframe)
    frame_around_ans.pack(pady = 15)

    ans_label = ctk.CTkLabel(master = frame_around_ans, justify=tk.CENTER, text = 'Antwort: ', font=LARGE_LABEL_FONT)
    ans_label.pack(padx = 20, pady = 20)

    frame_around_images = ctk.CTkFrame(master=mainframe)
    frame_around_images.pack(pady = 15)

    q_image = ctk.CTkImage(Image.open(os.path.join(info['img'], 'crop.jpg')), size=(350, 350))
    a_image = ctk.CTkImage(Image.open(os.path.join(info['img'], 'full.jpg')), size=(350, 350))

    q_label = ctk.CTkLabel(master = frame_around_images, justify=tk.CENTER, text = ' ', font=MID_LABEL_FONT, image=q_image, text_color=ANSWER_COLOR)
    q_label.pack(padx = 10, pady = 10, side='left')

    a_label = ctk.CTkLabel(master = frame_around_images, justify=tk.CENTER, text = info['a'], font=MID_LABEL_FONT, image=a_image, text_color=ANSWER_COLOR)
    a_label.pack(padx = 10, pady = 10)

    ret_button = ctk.CTkButton(master=mainframe, text = 'Weiter', font = BUTTON_FONT)
    ret_button.pack(pady = 30)
    ret_button.bind('<Button-1>', main_view_call)

    if popup:

        full_frame = ctk.CTkToplevel()

        a_image2 = ctk.CTkImage(Image.open(os.path.join(info['img'], 'full.jpg')), size = (screen_width-400, screen_height-250))

        a_label2 = ctk.CTkLabel(master = full_frame, justify=tk.CENTER, text = '', font=MID_LABEL_FONT, image=a_image2, text_color=ANSWER_COLOR)
        a_label2.pack(padx = 10, pady = 20)



main_view()


app.mainloop()

