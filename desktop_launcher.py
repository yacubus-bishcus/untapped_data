import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app_config import get_configured_username, set_configured_username


APP_DIR = Path(__file__).resolve().parent
RUN_SCRIPT = APP_DIR / "run.py"
DEFAULT_OUTPUT = APP_DIR / "my_beers.csv"


class DesktopLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Untappd Beer History")
        self.geometry("760x560")
        self.minsize(720, 520)

        self.process = None
        self.log_queue = queue.Queue()
        self.username_var = tk.StringVar(value=get_configured_username(""))
        self.backstop_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(DEFAULT_OUTPUT))
        self.update_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()
        self.after(150, self._drain_log_queue)

    def _build_ui(self):
        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="Untappd Beer History", font=("Helvetica", 22, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            container,
            text="Refresh your beer export, then open the Streamlit dashboard from one desktop window.",
        )
        subtitle.pack(anchor="w", pady=(4, 16))

        form = ttk.Frame(container)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(form, textvariable=self.username_var).grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(form, text="Backstop Total").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)
        ttk.Entry(form, textvariable=self.backstop_var).grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(form, text="Output CSV").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)
        output_row = ttk.Frame(form)
        output_row.grid(row=2, column=1, sticky="ew", pady=6)
        output_row.columnconfigure(0, weight=1)
        ttk.Entry(output_row, textvariable=self.output_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(output_row, text="Browse", command=self._choose_output).grid(row=0, column=1, padx=(8, 0))

        ttk.Checkbutton(
            form,
            text="Force fresh download from Untappd",
            variable=self.update_var,
        ).grid(row=3, column=1, sticky="w", pady=(8, 0))

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(18, 12))
        actions.columnconfigure((0, 1, 2), weight=1)
        ttk.Button(actions, text="Open Dashboard", command=self.open_dashboard).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(actions, text="Refresh Data + Dashboard", command=self.refresh_and_open).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(actions, text="Refresh Data Only", command=self.refresh_only).grid(row=0, column=2, sticky="ew", padx=(8, 0))

        secondary = ttk.Frame(container)
        secondary.pack(fill="x", pady=(0, 12))
        secondary.columnconfigure((0, 1), weight=1)
        ttk.Button(secondary, text="Open Export Folder", command=self.open_export_folder).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(secondary, text="Stop Running Task", command=self.stop_process).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        ttk.Label(container, textvariable=self.status_var, foreground="#6b7280").pack(anchor="w", pady=(0, 8))

        self.log = tk.Text(container, wrap="word", height=18, bg="#101418", fg="#e5eef5", insertbackground="#e5eef5")
        self.log.pack(fill="both", expand=True)
        self.log.insert("end", "Launcher ready.\n")
        self.log.configure(state="disabled")

    def _choose_output(self):
        target = filedialog.asksaveasfilename(
            title="Choose output CSV",
            initialdir=str(APP_DIR),
            initialfile=Path(self.output_var.get()).name,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if target:
            self.output_var.set(target)

    def _append_log(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _drain_log_queue(self):
        while True:
            try:
                item = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self._append_log(item)
        self.after(150, self._drain_log_queue)

    def _collect_common_args(self):
        args = []
        username = self.username_var.get().strip()
        if username:
            set_configured_username(username)
            args.extend(["--username", username])
        else:
            raise ValueError("Please enter your Untappd username.")

        output = self.output_var.get().strip()
        if output:
            args.extend(["--output", output])

        backstop = self.backstop_var.get().strip()
        if backstop:
            if not backstop.isdigit():
                raise ValueError("Backstop Total must be a whole number.")
            args.extend(["--backstop-total", backstop])
        return args

    def _start_process(self, command, status_text: str):
        if self.process and self.process.poll() is None:
            messagebox.showinfo("Task Already Running", "Wait for the current task to finish or stop it first.")
            return

        self.status_var.set(status_text)
        self._append_log(f"\n$ {' '.join(command)}\n")

        def worker():
            try:
                self.process = subprocess.Popen(
                    command,
                    cwd=str(APP_DIR),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                assert self.process.stdout is not None
                for line in self.process.stdout:
                    self.log_queue.put(line)
                return_code = self.process.wait()
                self.log_queue.put(f"\nProcess finished with exit code {return_code}.\n")
                self.status_var.set("Ready")
            except Exception as exc:
                self.log_queue.put(f"\nLauncher error: {exc}\n")
                self.status_var.set("Ready")
            finally:
                self.process = None

        threading.Thread(target=worker, daemon=True).start()

    def open_dashboard(self):
        command = [sys.executable, str(RUN_SCRIPT), "streamlit"]
        self._start_process(command, "Opening dashboard...")

    def refresh_only(self):
        try:
            command = [sys.executable, str(RUN_SCRIPT), "selenium-fetch-beers", *self._collect_common_args()]
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        self._start_process(command, "Refreshing beer data...")

    def refresh_and_open(self):
        try:
            command = [sys.executable, str(RUN_SCRIPT), "run-default", *self._collect_common_args(), "--update"]
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return
        self._start_process(command, "Refreshing beer data and opening dashboard...")

    def open_export_folder(self):
        target = Path(self.output_var.get()).expanduser().resolve().parent
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(target)])
        elif sys.platform.startswith("win"):
            subprocess.Popen(["explorer", str(target)])
        else:
            subprocess.Popen(["xdg-open", str(target)])

    def stop_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.status_var.set("Stopping task...")
            self._append_log("\nRequested process stop.\n")
        else:
            messagebox.showinfo("Nothing Running", "There is no active task to stop.")


def main():
    app = DesktopLauncher()
    app.mainloop()


if __name__ == "__main__":
    main()
