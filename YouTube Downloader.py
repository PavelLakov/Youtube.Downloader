import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import threading


def browse_directory():
    folder_selected = filedialog.askdirectory()
    download_location_entry.delete(0, tk.END)
    download_location_entry.insert(0, folder_selected)


def start_download_threaded():
    thread = threading.Thread(target=start_download)
    thread.start()


def progress_bar(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    bytes_downloaded = file_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / file_size * 100
    progress['value'] = percentage_of_completion
    root.update_idletasks()


def start_download():
    try:
        status_text.delete(1.0, tk.END)
        link = youtube_link_entry.get()
        quality = quality_var.get()
        file_format = format_var.get()
        download_path = download_location_entry.get()

        if not link or not quality or not file_format or not download_path:
            status_text.insert(tk.END, "Please ensure all fields are filled correctly.\\n")
            return

        yt = YouTube(link, on_progress_callback=progress_bar)
        if file_format == "mp4":
            video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by(
                'resolution').desc().first()
        else:
            video_stream = yt.streams.filter(only_audio=True).first()

        video_stream.download(output_path=download_path)
        status_text.insert(tk.END, f"Downloaded {yt.title} successfully!\\n")
    except Exception as e:
        status_text.insert(tk.END, f"Error: {str(e)}\\n")


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("YouTube Downloader")

# Prohibit maximizing the window
root.resizable(False, False)

# GUI layout and structure

label1 = ttk.Label(root, text="Enter the YouTube link below:")
label1.grid(row=0, column=0, sticky="w", padx=10, pady=10)

youtube_link_entry = ttk.Entry(root, width=50)
youtube_link_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

download_video_button = ttk.Button(root, text="Download Video")
download_video_button.grid(row=2, column=0, padx=10, pady=10)

quality_options = ["High", "Medium", "Low"]
quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(root, textvariable=quality_var, values=quality_options)
quality_dropdown.set("Select Quality")
quality_dropdown.grid(row=2, column=1, padx=10, pady=10)

format_options = ["mp3", "mp4"]
format_var = tk.StringVar()
format_dropdown = ttk.Combobox(root, textvariable=format_var, values=format_options)
format_dropdown.set("Select Format")
format_dropdown.grid(row=2, column=2, padx=10, pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

label2 = ttk.Label(root, text="Download Location:")
label2.grid(row=4, column=0, sticky="w", padx=10, pady=10)

download_location_entry = ttk.Entry(root, width=40)
download_location_entry.grid(row=5, column=0, padx=10, pady=10)

browse_button = ttk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=5, column=1, padx=10, pady=10)

start_download_button = ttk.Button(root, text="Start Download", command=start_download_threaded)
start_download_button.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

status_label = ttk.Label(root, text="Download Status:")
status_label.grid(row=7, column=0, sticky="w", padx=10, pady=10)

status_text = tk.Text(root, height=5, width=40)
status_text.grid(row=8, column=0, padx=10, pady=10, columnspan=3)

# Exit button
exit_button = ttk.Button(root, text="Exit", command=exit_app)
exit_button.grid(row=9, column=0, padx=10, pady=10, columnspan=3)

root.geometry('600x500')
root.mainloop()
