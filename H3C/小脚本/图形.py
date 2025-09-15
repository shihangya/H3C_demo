import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import csv

try:
    import openpyxl  # Excel 导入支持
except ImportError:
    openpyxl = None

from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice


# --------------------------------
# 工具函数：JSON存取
# --------------------------------
def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存 {filename} 失败: {e}")


def load_json(filename, default=None):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except json.JSONDecodeError:
        os.remove(filename)
        print(f"文件 {filename} 格式有误，已删除")
    except Exception as e:
        print(f"读取 {filename} 失败: {e}")
    return default if default is not None else {}


# --------------------------------
# 数据管理类
# --------------------------------
class DataManager:
    def __init__(self):
        self.template_file = "template_config.json"
        self.custom_file = "custom_template_groups.json"
        self.device_file = "device_names.json"

        # 默认数据
        self.moban = {
            "moban1": ["hsh", "mac", "hsh1", "hshs", "ipad", "dot1x", "per-psk", "wpa3-h2e", "wpa3-hnp", "wpa3-psk", "wpa3-qiye", "wpa3-dot1x", "wpa2-persion", "wpa3-h2e-7538", "wpa3-h2e-7539", "wpa3-hnp-7539", "wpa3-both-7539"],
            "moban2": [f"g{i}" for i in range(15, 30)],
            "moban3": [f"g{i}" for i in range(30, 45)]
        }
        self.custom_groups = {}
        self.device_names = ["3520h_1"]

        self.load_all()

    def load_all(self):
        self.moban.update(load_json(self.template_file, self.moban))
        self.custom_groups = load_json(self.custom_file, self.custom_groups)
        self.device_names = load_json(self.device_file, self.device_names)

    def save_moban(self):
        save_json(self.template_file, self.moban)

    def save_custom(self):
        save_json(self.custom_file, self.custom_groups)

    def save_devices(self):
        save_json(self.device_file, self.device_names)


# --------------------------------
# AC 连接管理
# --------------------------------
def connect_ac_device(access_name):
    finder = TopologyMap()
    ternl = Terminal()
    ternl.access_name = access_name
    ternl.open_window()
    dut = CCmwDevice()
    dut.add_terminal(ternl)
    dut.topofinder = finder
    return dut


# --------------------------------
# 主应用
# --------------------------------
class ACServiceTemplateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC服务模板绑定工具")
        self.root.geometry("750x900")

        self.data = DataManager()
        self.AC = None
        self.radios = [1, 2, 3]  # radio 范围可改
        self.operation_mode = tk.IntVar(value=1)

        self.create_widgets()

    # ------------- UI 创建 -------------
    def create_widgets(self):
        # AC连接
        conn_frame = ttk.LabelFrame(self.root, text="AC连接")
        conn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(conn_frame, text="设备名称:").grid(row=0, column=0, padx=5, pady=5)
        self.device_var = tk.StringVar(value=self.data.device_names[0])
        self.device_combo = ttk.Combobox(conn_frame, textvariable=self.device_var, values=self.data.device_names, width=20)
        self.device_combo.grid(row=0, column=1, padx=5, pady=5)
        self.device_combo.bind("<Return>", lambda e: self.connect_ac())

        btnf = ttk.Frame(conn_frame)
        btnf.grid(row=0, column=2, padx=5)
        ttk.Button(btnf, text="连接AC", command=self.connect_ac).pack(side="top", fill="x", pady=1)
        ttk.Button(btnf, text="添加设备", command=self.add_device).pack(side="left", padx=1)
        ttk.Button(btnf, text="删除设备", command=self.del_device).pack(side="left", padx=1)

        self.conn_status = ttk.Label(conn_frame, text="未连接")
        self.conn_status.grid(row=0, column=3, padx=5)

        # 操作模式
        mode_frame = ttk.LabelFrame(self.root, text="操作模式")
        mode_frame.pack(fill="x", padx=10, pady=5)
        ttk.Radiobutton(mode_frame, text="绑定服务模板", variable=self.operation_mode, value=1).pack(side="left", padx=10)
        ttk.Radiobutton(mode_frame, text="取消绑定服务模板", variable=self.operation_mode, value=2).pack(side="left", padx=10)

        # 模板选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        for k, v in self.data.moban.items():
            self.create_template_tab(k, v, predefined=True)
        for k, v in self.data.custom_groups.items():
            self.create_template_tab(k, v["templates"], predefined=False)
        self.create_custom_management_tab()

        # 按钮 & 日志
        bf = ttk.Frame(self.root)
        bf.pack(fill="x", padx=10, pady=5)
        ttk.Button(bf, text="命令预览", command=self.preview_commands).pack(side="left", padx=5)
        self.exec_btn = ttk.Button(bf, text="执行操作", command=self.execute, state="disabled")
        self.exec_btn.pack(side="left", padx=5)
        ttk.Button(bf, text="清空日志", command=lambda: self.log_text.delete(1.0, tk.END)).pack(side="left", padx=5)
        ttk.Button(bf, text="退出", command=self.root.quit).pack(side="right", padx=5)

        logf = ttk.LabelFrame(self.root, text="操作日志")
        logf.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text = tk.Text(logf, height=12)
        self.log_text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(logf, command=self.log_text.yview)
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

    # 模板tab
    def create_template_tab(self, name, items, predefined=True):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)

        var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=var, width=15)
        entry.pack(side="top", padx=5, pady=5)

        lb = tk.Listbox(frame, selectmode=tk.MULTIPLE)
        lb.pack(fill="both", expand=True, padx=5, pady=5)
        for item in items:
            lb.insert(tk.END, item)

        btnf = ttk.Frame(frame)
        btnf.pack(fill="x")
        ttk.Button(btnf, text="添加", command=lambda: self.add_item(var, lb, name, predefined)).pack(side="left", padx=2)
        ttk.Button(btnf, text="删除选中", command=lambda: self.del_item(lb, name, predefined)).pack(side="left", padx=2)
        ttk.Button(btnf, text="批量导入", command=lambda: self.import_templates(lb, name, predefined)).pack(side="left", padx=2)
        ttk.Button(btnf, text="全选", command=lambda: lb.selection_set(0, tk.END)).pack(side="left", padx=2)
        ttk.Button(btnf, text="清空选择", command=lambda: lb.selection_clear(0, tk.END)).pack(side="left", padx=2)
        if not predefined:
            ttk.Button(btnf, text="删除组", command=lambda: self.del_group(name)).pack(side="left", padx=2)

        self.data.custom_groups[name] = self.data.custom_groups.get(name, {"templates": items})
        self.data.custom_groups[name]["listbox"] = lb

    # 模板操作
    def add_item(self, var, lb, name, predefined):
        tpls = [t.strip() for t in var.get().split(",") if t.strip()]
        if not tpls:
            return
        target_list = self.data.moban[name] if predefined else self.data.custom_groups[name]["templates"]
        added = 0
        for t in tpls:
            if t not in target_list:
                target_list.append(t)
                lb.insert(tk.END, t)
                added += 1
        if added:
            var.set("")
            (self.data.save_moban() if predefined else self.data.save_custom())
            self.log(f"已添加 {added} 个模板到 {name}")

    def del_item(self, lb, name, predefined):
        sel = lb.curselection()
        if not sel:
            return
        target_list = self.data.moban[name] if predefined else self.data.custom_groups[name]["templates"]
        for i in reversed(sel):
            del target_list[i]
            lb.delete(i)
        (self.data.save_moban() if predefined else self.data.save_custom())
        self.log(f"已删除 {len(sel)} 个模板从 {name}")

    def import_templates(self, lb, name, predefined):
        filepath = filedialog.askopenfilename(filetypes=[("CSV 文件", "*.csv"), ("Excel 文件", "*.xlsx")])
        if not filepath:
            return
        imported = []
        try:
            if filepath.lower().endswith(".csv"):
                with open(filepath, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    imported = [row[0].strip() for row in reader if row]
            elif filepath.lower().endswith(".xlsx") and openpyxl:
                wb = openpyxl.load_workbook(filepath)
                ws = wb.active
                imported = [str(row[0].value).strip() for row in ws.iter_rows(min_row=1) if row[0].value]
                wb.close()
            else:
                messagebox.showwarning("格式不支持", "请选择 CSV 或 Excel 文件（需安装 openpyxl）")
                return
        except Exception as e:
            messagebox.showerror("导入失败", str(e))
            return

        target_list = self.data.moban[name] if predefined else self.data.custom_groups[name]["templates"]
        count = 0
        for t in imported:
            if t and t not in target_list:
                target_list.append(t)
                lb.insert(tk.END, t)
                count += 1
        if count:
            (self.data.save_moban() if predefined else self.data.save_custom())
            self.log(f"批量导入 {count} 个模板到 {name}")

    # 自定义组
    def create_custom_management_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="管理自定义组")
        name_var = tk.StringVar()
        tpl_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=15).pack(side="left", padx=5)
        ttk.Entry(frame, textvariable=tpl_var, width=30).pack(side="left", padx=5)
        ttk.Button(frame, text="创建组", command=lambda: self.create_group(name_var, tpl_var)).pack(side="left", padx=5)

    def create_group(self, name_var, tpl_var):
        name = name_var.get().strip()
        tpls = [t.strip() for t in tpl_var.get().split(",") if t.strip()]
        if not name or not tpls:
            return
        self.data.custom_groups[name] = {"templates": tpls}
        self.data.save_custom()
        self.create_template_tab(name, tpls, predefined=False)
        name_var.set("")
        tpl_var.set("")
        self.log(f"已创建自定义组 {name}")

    def del_group(self, name):
        if name in self.data.custom_groups:
            del self.data.custom_groups[name]
            self.data.save_custom()
            idx = [i for i in range(self.notebook.index("end")) if self.notebook.tab(i, "text") == name]
            if idx:
                self.notebook.forget(idx[0])
            self.log(f"已删除组 {name}")

    # 设备管理
    def connect_ac(self):
        dev = self.device_var.get().strip()
        if not dev:
            return
        if dev not in self.data.device_names:
            self.data.device_names.append(dev)
            self.data.save_devices()
        try:
            self.AC = connect_ac_device(dev)
            self.conn_status.config(text="已连接", foreground="green")
            self.exec_btn.config(state="normal")
            self.log(f"已连接设备 {dev}")
        except Exception as e:
            messagebox.showerror("连接失败", str(e))

    def add_device(self):
        dev = self.device_var.get().strip()
        if dev and dev not in self.data.device_names:
            self.data.device_names.append(dev)
            self.data.save_devices()
            self.device_combo.config(values=self.data.device_names)
            self.log(f"已添加设备 {dev}")

    def del_device(self):
        dev = self.device_var.get().strip()
        if dev in self.data.device_names and len(self.data.device_names) > 1:
            self.data.device_names.remove(dev)
            self.data.save_devices()
            self.device_combo.config(values=self.data.device_names)
            self.device_var.set(self.data.device_names[0])
            self.log(f"已删除设备 {dev}")

    # 命令预览
    def preview_commands(self):
        selected = self.get_selected_templates()
        if not selected:
            messagebox.showinfo("提示", "请选择要操作的模板")
            return
        bind = (self.operation_mode.get() == 1)
        cmds = []
        for t in selected:
            for r in self.radios:
                cmds.append(f"radio {r}\n{'service-template' if bind else 'undo service-template'} {t}")
        preview_win = tk.Toplevel(self.root)
        preview_win.title("命令预览")
        text = tk.Text(preview_win, width=60, height=20)
        text.pack(fill="both", expand=True)
        text.insert("1.0", "\n".join(cmds))
        text.config(state="disabled")

    def get_selected_templates(self):
        selected = []
        for name, data in {**self.data.moban, **{k: v["templates"] for k, v in self.data.custom_groups.items()}}.items():
            lb = self.data.custom_groups.get(name, {}).get("listbox")
            if not lb:
                continue
            for i in lb.curselection():
                selected.append(data[i])
        return selected

    # 执行
    def execute(self):
        if not self.AC:
            return
        selected = self.get_selected_templates()
        if not selected:
            return
        bind = (self.operation_mode.get() == 1)
        for t in selected:
            cmds = []
            for r in self.radios:
                cmd = f"radio {r}\n{'service-template' if bind else 'undo service-template'} {t}"
                cmds.append(cmd)
            output = self.AC.send("\n".join(cmds))
            self.log(("绑定" if bind else "取消绑定") + f"模板: {t}")
            if output:
                self.log("设备返回:\n" + str(output))

        messagebox.showinfo("完成", "命令已发送")

    # 日志
    def log(self, msg):
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ACServiceTemplateApp(root)
    root.mainloop()