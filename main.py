
import json 
import os
import uuid
from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox


# ============================================================
# تنظیمات
# ============================================================

APP_NAME = "مدیریت کارها"

# مسیر اصلی پروژه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# پوشه data
DATA_DIR = os.path.join(BASE_DIR, "data")

# فایل ذخیره تسک‌ها
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")


# ============================================================
# مدیریت فایل و اطلاعات
# ============================================================

def ensure_data_file():
    """
    اگر پوشه data یا فایل tasks.json وجود نداشته باشد،
    آن‌ها را ایجاد می‌کند.
    """

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TASKS_FILE):
        save_tasks([])


def load_tasks():
    """
    تمام تسک‌ها را از فایل JSON می‌خواند.
    """

    try:
        if not os.path.exists(TASKS_FILE):
            return []

        with open(
            TASKS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except json.JSONDecodeError:

        messagebox.showerror(
            "خطا",
            "فایل tasks.json خراب یا نامعتبر است."
        )

        return []

    except OSError as error:

        messagebox.showerror(
            "خطا",
            f"خواندن فایل انجام نشد:\n\n{error}"
        )

        return []


def save_tasks(tasks):
    """
    ذخیره تمام تسک‌ها در فایل JSON.
    """

    try:

        os.makedirs(DATA_DIR, exist_ok=True)

        # ابتدا در فایل موقت ذخیره می‌کنیم
        # تا احتمال خراب شدن فایل اصلی کمتر شود.
        temp_file = TASKS_FILE + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                tasks,
                file,
                ensure_ascii=False,
                indent=4
            )

        # جایگزینی فایل اصلی
        os.replace(
            temp_file,
            TASKS_FILE
        )

        return True

    except OSError as error:

        messagebox.showerror(
            "خطا",
            f"ذخیره اطلاعات انجام نشد:\n\n{error}"
        )

        return False


def get_current_time():
    """
    زمان فعلی را برمی‌گرداند.
    """

    return datetime.now().isoformat(
        timespec="seconds"
    )


def create_task(title):
    """
    یک تسک جدید ایجاد می‌کند.
    """

    now = get_current_time()

    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "completed": False,
        "created_at": now,
        "updated_at": now
    }


# ============================================================
# کلاس اصلی برنامه
# ============================================================

class TodoApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # -----------------------------
        # تنظیمات پنجره
        # -----------------------------

        self.title(APP_NAME)

        self.geometry("850x650")

        self.minsize(
            700,
            500
        )

        # -----------------------------
        # تنظیم ظاهر
        # -----------------------------

        ctk.set_appearance_mode("System")

        ctk.set_default_color_theme("blue")

        # -----------------------------
        # آماده‌سازی داده‌ها
        # -----------------------------

        ensure_data_file()

        self.tasks = load_tasks()

        # -----------------------------
        # ساخت رابط
        # -----------------------------

        self.create_ui()

        # نمایش تسک‌ها
        self.refresh_tasks()


    # ========================================================
    # ساخت رابط کاربری
    # ========================================================

    def create_ui(self):

        # تنظیم ستون اصلی
        self.grid_columnconfigure(
            0,
            weight=1
        )

        # تنظیم ردیف لیست
        self.grid_rowconfigure(
            2,
            weight=1
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title_label = ctk.CTkLabel(
            header,
            text="مدیریت کارها",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title_label.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        subtitle_label = ctk.CTkLabel(
            header,
            text="لیست کارهای روزانه شما",
            font=ctk.CTkFont(
                size=14
            )
        )

        subtitle_label.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # قسمت افزودن تسک
        # ----------------------------------------------------

        add_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        add_frame.grid(
            row=1,
            column=0,
            padx=25,
            pady=15,
            sticky="ew"
        )

        add_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.task_entry = ctk.CTkEntry(
            add_frame,
            height=42,
            placeholder_text="تسک جدید را وارد کنید..."
        )

        self.task_entry.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew"
        )

        self.add_button = ctk.CTkButton(
            add_frame,
            text="افزودن",
            width=100,
            height=42,
            command=self.add_task
        )

        self.add_button.grid(
            row=0,
            column=1
        )

        # با Enter هم تسک اضافه شود
        self.task_entry.bind(
            "<Return>",
            lambda event: self.add_task()
        )

        # ----------------------------------------------------
        # عنوان لیست
        # ----------------------------------------------------

        list_header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        list_header.grid(
            row=2,
            column=0,
            padx=25,
            pady=(0, 5),
            sticky="new"
        )

        list_header.grid_columnconfigure(
            0,
            weight=1
        )

        self.list_title = ctk.CTkLabel(
            list_header,
            text="تسک‌ها",
            anchor="w",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.list_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.count_label = ctk.CTkLabel(
            list_header,
            text="0 تسک",
            anchor="e"
        )

        self.count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ----------------------------------------------------
        # لیست قابل اسکرول
        # ----------------------------------------------------

        self.task_list_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )

        self.task_list_frame.grid(
            row=3,
            column=0,
            padx=25,
            pady=5,
            sticky="nsew"
        )

        self.task_list_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            3,
            weight=1
        )

        # ----------------------------------------------------
        # پایین برنامه
        # ----------------------------------------------------

        bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom_frame.grid(
            row=4,
            column=0,
            padx=25,
            pady=(10, 20),
            sticky="ew"
        )

        bottom_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.clear_completed_button = ctk.CTkButton(
            bottom_frame,
            text="حذف کارهای انجام‌شده",
            width=170,
            command=self.clear_completed_tasks
        )

        self.clear_completed_button.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.theme_menu = ctk.CTkOptionMenu(
            bottom_frame,
            values=[
                "سیستم",
                "روشن",
                "تاریک"
            ],
            width=120,
            command=self.change_theme
        )

        self.theme_menu.set("سیستم")

        self.theme_menu.grid(
            row=0,
            column=1,
            sticky="e"
        )


    # ========================================================
    # افزودن تسک
    # ========================================================

    def add_task(self):

        title = self.task_entry.get().strip()

        # جلوگیری از تسک خالی
        if not title:

            messagebox.showwarning(
                "توجه",
                "لطفاً متن تسک را وارد کنید."
            )

            self.task_entry.focus()

            return

        # ایجاد تسک
        task = create_task(title)

        # اضافه کردن به لیست
        self.tasks.append(task)

        # ذخیره
        if save_tasks(self.tasks):

            # خالی کردن ورودی
            self.task_entry.delete(
                0,
                "end"
            )

            # بروزرسانی نمایش
            self.refresh_tasks()

            self.task_entry.focus()


    # ========================================================
    # تغییر وضعیت تسک
    # ========================================================

    def toggle_task(self, task_id):

        for task in self.tasks:

            if task["id"] == task_id:

                task["completed"] = not task["completed"]

                task["updated_at"] = get_current_time()

                break

        save_tasks(self.tasks)

        self.refresh_tasks()


    # ========================================================
    # حذف تسک
    # ========================================================

    def delete_task(self, task_id):

        confirmed = messagebox.askyesno(
            "تأیید حذف",
            "آیا مطمئن هستید که می‌خواهید این تسک را حذف کنید؟"
        )

        if not confirmed:
            return

        self.tasks = [
            task
            for task in self.tasks
            if task["id"] != task_id
        ]

        save_tasks(self.tasks)

        self.refresh_tasks()


    # ========================================================
    # ویرایش تسک
    # ========================================================

    def edit_task(self, task_id):

        selected_task = None

        for task in self.tasks:

            if task["id"] == task_id:

                selected_task = task

                break

        if selected_task is None:
            return

        # پنجره ویرایش
        dialog = ctk.CTkToplevel(self)

        dialog.title("ویرایش تسک")

        dialog.geometry("450x180")

        dialog.resizable(
            False,
            False
        )

        dialog.transient(self)

        dialog.grab_set()

        dialog.grid_columnconfigure(
            0,
            weight=1
        )

        label = ctk.CTkLabel(
            dialog,
            text="عنوان جدید تسک:"
        )

        label.grid(
            row=0,
            column=0,
            padx=25,
            pady=(25, 10)
        )

        entry = ctk.CTkEntry(
            dialog,
            height=40
        )

        entry.grid(
            row=1,
            column=0,
            padx=25,
            sticky="ew"
        )

        entry.insert(
            0,
            selected_task["title"]
        )

        entry.focus()

        def save_edit():

            new_title = entry.get().strip()

            if not new_title:

                messagebox.showwarning(
                    "توجه",
                    "عنوان تسک نمی‌تواند خالی باشد.",
                    parent=dialog
                )

                return

            selected_task["title"] = new_title

            selected_task["updated_at"] = get_current_time()

            save_tasks(self.tasks)

            dialog.destroy()

            self.refresh_tasks()

        save_button = ctk.CTkButton(
            dialog,
            text="ذخیره",
            command=save_edit
        )

        save_button.grid(
            row=2,
            column=0,
            padx=25,
            pady=15
        )

        entry.bind(
            "<Return>",
            lambda event: save_edit()
        )


    # ========================================================
    # حذف تسک‌های انجام‌شده
    # ========================================================

    def clear_completed_tasks(self):

        completed_tasks = [
            task
            for task in self.tasks
            if task.get("completed", False)
        ]

        if not completed_tasks:

            messagebox.showinfo(
                "اطلاع",
                "هیچ تسک انجام‌شده‌ای وجود ندارد."
            )

            return

        confirmed = messagebox.askyesno(
            "تأیید",
            f"{len(completed_tasks)} تسک انجام‌شده حذف شود؟"
        )

        if not confirmed:
            return

        self.tasks = [
            task
            for task in self.tasks
            if not task.get("completed", False)
        ]

        save_tasks(self.tasks)

        self.refresh_tasks()


    # ========================================================
    # تغییر حالت تاریک / روشن
    # ========================================================

    def change_theme(self, choice):

        if choice == "تاریک":

            ctk.set_appearance_mode("Dark")

        elif choice == "روشن":

            ctk.set_appearance_mode("Light")

        else:

            ctk.set_appearance_mode("System")


    # ========================================================
    # بروزرسانی لیست
    # ========================================================

    def refresh_tasks(self):

        # پاک کردن ویجت‌های قبلی
        for widget in self.task_list_frame.winfo_children():

            widget.destroy()

        # اگر لیست خالی است
        if not self.tasks:

            empty_label = ctk.CTkLabel(
                self.task_list_frame,
                text="هنوز هیچ کاری اضافه نشده است.",
                text_color="gray",
                font=ctk.CTkFont(
                    size=15
                )
            )

            empty_label.grid(
                row=0,
                column=0,
                pady=50
            )

        else:

            # ساخت آیتم‌های لیست
            for index, task in enumerate(self.tasks):

                self.create_task_widget(
                    task,
                    index
                )

        # بروزرسانی تعداد
        total = len(self.tasks)

        completed = sum(
            1
            for task in self.tasks
            if task.get("completed", False)
        )

        self.count_label.configure(
            text=f"{total} تسک | {completed} انجام‌شده"
        )


    # ========================================================
    # ساخت آیتم تسک
    # ========================================================

    def create_task_widget(
        self,
        task,
        index
    ):

        completed = task.get(
            "completed",
            False
        )

        # قاب تسک
        task_frame = ctk.CTkFrame(
            self.task_list_frame,
            corner_radius=10
        )

        task_frame.grid(
            row=index,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        task_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # Checkbox
        # ----------------------------------------------------

        checkbox = ctk.CTkCheckBox(
            task_frame,
            text=""
        )

        checkbox.grid(
            row=0,
            column=0,
            padx=(12, 5),
            pady=12
        )

        if completed:

            checkbox.select()

        checkbox.configure(
            command=lambda: self.toggle_task(
                task["id"]
            )
        )

        # ----------------------------------------------------
        # عنوان
        # ----------------------------------------------------

        title = task["title"]

        if completed:

            title = "✓ " + title

        title_label = ctk.CTkLabel(
            task_frame,
            text=title,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=15
            )
        )

        title_label.grid(
            row=0,
            column=1,
            padx=8,
            pady=12,
            sticky="ew"
        )

        # ----------------------------------------------------
        # دکمه ویرایش
        # ----------------------------------------------------

        edit_button = ctk.CTkButton(
            task_frame,
            text="ویرایش",
            width=70,
            height=32,
            command=lambda: self.edit_task(
                task["id"]
            )
        )

        edit_button.grid(
            row=0,
            column=2,
            padx=4
        )

        # ----------------------------------------------------
        # دکمه حذف
        # ----------------------------------------------------

        delete_button = ctk.CTkButton(
            task_frame,
            text="حذف",
            width=60,
            height=32,
            fg_color="#c0392b",
            hover_color="#922b21",
            command=lambda: self.delete_task(
                task["id"]
            )
        )

        delete_button.grid(
            row=0,
            column=3,
            padx=(4, 10)
        )


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":

    app = TodoApp()

    app.mainloop()
