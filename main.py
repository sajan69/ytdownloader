import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import threading

def create_progress_bar_popup():
    global popup
    popup = tk.Toplevel(root)
    popup.title("Download Progress")
    popup.config(bg="red")
    popup.geometry("300x120")
    popup.resizable(False, False)

    global pb
    pb = ttk.Progressbar(
        popup,
        orient='horizontal',
        mode='determinate',
        length=280
    )
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

    def update_progress_label():
        return f"Current Progress: {pb['value']}%"

    def progress():
        if pb['value'] < 100:
            pb['value'] += 10
            value_label['text'] = update_progress_label()
            popup.after(1000, progress) 
        else:
            pb.stop()
            messagebox.showinfo(message='The progress completed!')
            popup.destroy()

    
    value_label = ttk.Label(popup, text=update_progress_label())
    value_label.grid(column=0, row=1, columnspan=2)

    progress()

def Widgets():
    head_label = tk.Label(root, text="YouTube Video Downloader", padx=15, pady=15, font="Arial 16 bold", bg="red", fg="white")
    head_label.grid(row=0, column=0, columnspan=3, pady=10)

    link_label = tk.Label(root, text="YouTube Link:", bg="red", fg="white", pady=5, padx=5, font="Arial 12")
    link_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")

    destination_label = tk.Label(root, text="Destination:", bg="red", fg="white", pady=5, padx=5, font="Arial 12")
    destination_label.grid(row=2, column=0, pady=5, padx=5, sticky="e")

    quality_label = tk.Label(root, text="Video Quality:", bg="red", fg="white", pady=5, padx=5, font="Arial 12")
    quality_label.grid(row=3, column=0, pady=5, padx=5, sticky="e")

    root.linkText = tk.Entry(root, width=35, textvariable=video_Link, font="Arial 12")
    root.linkText.grid(row=1, column=1, pady=5, padx=5, columnspan=2, sticky="w")

    root.destinationText = tk.Entry(root, width=27, textvariable=download_Path, font="Arial 12")
    root.destinationText.grid(row=2, column=1, pady=5, padx=5, sticky="w")

    global quality_menu
    quality_menu = ttk.Combobox(root, font="Arial 12", state="readonly")
    quality_menu.grid(row=3, column=1, pady=5, padx=5, sticky="w")

    browse_B = tk.Button(root, text="Browse", command=Browse, width=10, bg="#FFA07A", fg="white", relief=tk.GROOVE)
    browse_B.grid(row=2, column=2, pady=1, padx=1, sticky="w")

    global download_B
    download_B = tk.Button(root, text="Download Video", command=Download, width=20, bg="#4682B4", fg="white", relief=tk.GROOVE, font=("Arial", 12, "bold"))
    download_B.grid(row=4, column=0, columnspan=3, pady=10)

def Browse():
    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
    download_Path.set(download_Directory)

def get_quality_options(yt_link):
    try:
        yt = YouTube(yt_link)
        streams = yt.streams.filter(progressive=True)
        qualities = [stream.resolution for stream in streams]
        return qualities
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return []

def Download():
    yt_link = video_Link.get()
    download_Folder = download_Path.get()
    selected_quality = quality_menu.get()  # Get the selected quality

    # Create a thread for downloading
    download_thread = threading.Thread(target=download_video, args=(yt_link, download_Folder, selected_quality))
    download_thread.start()

def download_video(yt_link, download_Folder, selected_quality):
    try:
        yt = YouTube(yt_link)
        
        video = yt.streams.filter(progressive=True, resolution=selected_quality).first()
        video.download(download_Folder)
        messagebox.showinfo("Success", "Video Downloaded Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

   
    pb.stop()
    popup.destroy()

    
    pb['value'] = 0

def update_quality_options(*args):
    yt_link = video_Link.get()
    qualities = get_quality_options(yt_link)
    quality_menu['values'] = qualities
    if qualities:
        quality_menu.set(qualities[0])

root = tk.Tk()
root.geometry("500x350")
root.title("YouTube Video Downloader")
root.config(bg="red")  

video_Link = tk.StringVar()
download_Path = tk.StringVar()

quality_menu = None

Widgets()


video_Link.trace_add("write", update_quality_options)

root.eval('tk::PlaceWindow . center')

root.mainloop()
