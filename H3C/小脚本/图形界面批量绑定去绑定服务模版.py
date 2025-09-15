import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice

def connect(access_name):
    finder = TopologyMap()
    ternl = Terminal()
    ternl.access_name = access_name
    ternl.open_window()
    dut = CCmwDevice()
    dut.add_terminal(ternl)
    dut.topofinder = finder

    return dut


class ACServiceTemplateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC服务模板绑定工具")
        self.root.geometry("750x900")

        # AC连接对象
        self.AC = None

        # 预定义设备名称列表
        self.device_names = ["3520h_1"]

        # 服务模板列表（可编辑）
        self.moban1 = ["hsh", "mac", "hsh1", "hshs", "ipad", "dot1x", "per-psk", "wpa3-h2e", "wpa3-hnp", "wpa3-psk", "wpa3-qiye", "wpa3-dot1x", "wpa2-persion", "wpa3-h2e-7538", "wpa3-h2e-7539", "wpa3-hnp-7539", "wpa3-both-7539"]
        self.moban2 = ["g15","g16","g17","g18","g19","g20","g21","g22","g23","g24","g25","g26","g27","g28","g29"]
        self.moban3 = ["g30","g31","g32","g33","g34","g35","g36","g37","g38","g39","g40","g41","g42","g43","g44"]

        # 自定义模板组
        self.custom_groups = {}

        # 当前选中的模板
        self.selected_templates = []

        # 先加载配置
        self.load_template_config()
        self.load_device_names()

        # 先创建界面组件
        self.create_widgets()

        # 然后加载自定义模板组
        self.load_custom_groups()

    def create_widgets(self):
        # AC连接区域
        connection_frame = ttk.LabelFrame(self.root, text="AC连接")
        connection_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(connection_frame, text="设备名称:").grid(row=0, column=0, padx=5, pady=5)
        # 使用Combobox替换Entry，支持下拉选择和手动输入
        self.device_name_var = tk.StringVar(value="3520h_1")
        self.device_combo = ttk.Combobox(connection_frame, textvariable=self.device_name_var, width=20, values=self.device_names)
        self.device_combo.grid(row=0, column=1, padx=5, pady=5)
        self.device_combo.bind('<Return>', lambda event: self.connect_ac())  # 回车连接

        # 添加设备管理按钮
        device_btn_frame = ttk.Frame(connection_frame)
        device_btn_frame.grid(row=0, column=2, padx=5, pady=5)

        self.connect_btn = ttk.Button(device_btn_frame, text="连接AC", command=self.connect_ac)
        self.connect_btn.pack(side="top", fill="x", pady=(0, 2))

        ttk.Button(device_btn_frame, text="添加设备", command=self.add_device, width=8).pack(side="left", padx=(0, 2))
        ttk.Button(device_btn_frame, text="删除设备", command=self.delete_device, width=8).pack(side="left")

        self.connection_status = ttk.Label(connection_frame, text="未连接")
        self.connection_status.grid(row=0, column=3, padx=5, pady=5)

        # 操作模式选择
        mode_frame = ttk.LabelFrame(self.root, text="操作模式")
        mode_frame.pack(fill="x", padx=10, pady=5)

        self.operation_mode = tk.IntVar(value=1)  # 1:绑定  2:取消绑定
        ttk.Radiobutton(mode_frame, text="绑定服务模板", variable=self.operation_mode, value=1).pack(side="left", padx=10, pady=5)
        ttk.Radiobutton(mode_frame, text="取消绑定服务模板", variable=self.operation_mode, value=2).pack(side="left", padx=10, pady=5)

        # 服务模板选择区域
        template_frame = ttk.LabelFrame(self.root, text="服务模板选择")
        template_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建选项卡
        self.template_notebook = ttk.Notebook(template_frame)
        self.template_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建各个模板组的选项卡
        self.create_template_tab("模板组1", self.moban1, "moban1")
        self.create_template_tab("模板组2", self.moban2, "moban2")
        self.create_template_tab("模板组3", self.moban3, "moban3")

        # 创建自定义模板组选项卡
        self.create_custom_groups_tabs()

        # 创建自定义模板组管理选项卡
        self.create_custom_group_management_tab()

        # 操作按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)

        self.execute_btn = ttk.Button(button_frame, text="执行操作", command=self.execute_operation, state="disabled")
        self.execute_btn.pack(side="left", padx=10, pady=5)

        self.exit_btn = ttk.Button(button_frame, text="退出", command=self.root.quit)
        self.exit_btn.pack(side="right", padx=10, pady=5)

        # 日志区域
        log_frame = ttk.LabelFrame(self.root, text="操作日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=15)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar_log = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar_log.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar_log.set)

    def create_template_tab(self, tab_name, template_list, list_name):
        frame = ttk.Frame(self.template_notebook)
        self.template_notebook.add(frame, text=tab_name)

        # 模板管理区域
        manage_frame = ttk.Frame(frame)
        manage_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(manage_frame, text="模板名称:").pack(side="left", padx=(5, 0))
        template_var = tk.StringVar()
        template_entry = ttk.Entry(manage_frame, textvariable=template_var, width=15)
        template_entry.pack(side="left", padx=5)

        # 创建列表框（提前定义，解决作用域问题）
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # 创建列表框
        listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        for template in template_list:
            listbox.insert(tk.END, template)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # 保存列表框引用
        setattr(self, f"{list_name}_listbox", listbox)
        setattr(self, f"{list_name}_entry", template_var)

        # 添加模板按钮
        add_btn = ttk.Button(manage_frame, text="添加",
                            command=lambda: self.add_template_to_list(template_var, template_list, listbox, list_name))
        add_btn.pack(side="left", padx=5)

        # 删除选中模板按钮
        del_btn = ttk.Button(manage_frame, text="删除选中",
                            command=lambda: self.delete_selected_templates_from_list(template_list, listbox, list_name))
        del_btn.pack(side="left", padx=5)

        # 按钮区域
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="全选",
                  command=lambda lb=listbox: lb.selection_set(0, tk.END)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空",
                  command=lambda lb=listbox: lb.selection_clear(0, tk.END)).pack(side="left", padx=5)

    def create_custom_groups_tabs(self):
        """创建自定义模板组选项卡"""
        for group_name, group_data in self.custom_groups.items():
            templates = group_data["templates"] if isinstance(group_data, dict) else group_data
            self.create_custom_group_tab(group_name, templates)

    def create_custom_group_tab(self, group_name, templates):
        frame = ttk.Frame(self.template_notebook)
        self.template_notebook.add(frame, text=group_name)
        frame.group_name = group_name  # 保存组名

        # 模板管理区域
        manage_frame = ttk.Frame(frame)
        manage_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(manage_frame, text="模板名称:").pack(side="left", padx=(5, 0))
        template_var = tk.StringVar()
        template_entry = ttk.Entry(manage_frame, textvariable=template_var, width=15)
        template_entry.pack(side="left", padx=5)

        # 模板选择区域（提前定义，解决作用域问题）
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # 创建列表框
        listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        for template in templates:
            listbox.insert(tk.END, template)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # 保存列表框引用
        listbox.group_name = group_name
        self.custom_groups[group_name] = {"templates": templates, "listbox": listbox, "entry": template_var}

        # 添加模板按钮
        add_btn = ttk.Button(manage_frame, text="添加",
                            command=lambda: self.add_template_to_custom_group(template_var, group_name))
        add_btn.pack(side="left", padx=5)

        # 删除选中模板按钮
        del_btn = ttk.Button(manage_frame, text="删除选中",
                            command=lambda: self.delete_selected_templates_from_custom_group(group_name))
        del_btn.pack(side="left", padx=5)

        # 删除组按钮
        del_group_btn = ttk.Button(manage_frame, text="删除组",
                                  command=lambda gn=group_name: self.delete_custom_group(gn))
        del_group_btn.pack(side="left", padx=5)

        # 按钮区域
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="全选",
                  command=lambda lb=listbox: lb.selection_set(0, tk.END)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空",
                  command=lambda lb=listbox: lb.selection_clear(0, tk.END)).pack(side="left", padx=5)

        # 保存引用
        self.custom_groups[group_name]["listbox"] = listbox
        self.custom_groups[group_name]["entry"] = template_var

    def create_custom_group_management_tab(self):
        """创建自定义模板组管理选项卡"""
        frame = ttk.Frame(self.template_notebook)
        self.template_notebook.add(frame, text="管理自定义组")

        # 创建自定义组区域
        create_frame = ttk.LabelFrame(frame, text="创建自定义模板组")
        create_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(create_frame, text="组名:").grid(row=0, column=0, padx=5, pady=5)
        self.new_group_name_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.new_group_name_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(create_frame, text="模板(逗号分隔):").grid(row=1, column=0, padx=5, pady=5)
        self.new_group_templates_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.new_group_templates_var, width=40).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(create_frame, text="创建组", command=self.create_custom_group).grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        # 现有自定义组列表
        existing_frame = ttk.LabelFrame(frame, text="现有自定义组")
        existing_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.existing_groups_listbox = tk.Listbox(existing_frame)
        self.existing_groups_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.update_existing_groups_list()

        # 操作按钮
        group_btn_frame = ttk.Frame(existing_frame)
        group_btn_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(group_btn_frame, text="刷新列表", command=self.update_existing_groups_list).pack(side="left", padx=5)
        ttk.Button(group_btn_frame, text="删除选中组", command=self.delete_selected_group).pack(side="left", padx=5)

    def add_template_to_list(self, template_var, template_list, listbox, list_name):
        """添加模板到预定义列表"""
        template_name = template_var.get().strip()
        if not template_name:
            messagebox.showwarning("输入错误", "请输入模板名称")
            return

        # 支持逗号分隔的多个模板
        templates = [t.strip() for t in template_name.split(",") if t.strip()]

        added_count = 0
        for template in templates:
            if template not in template_list:
                template_list.append(template)
                listbox.insert(tk.END, template)
                added_count += 1

        if added_count > 0:
            template_var.set("")
            self.log_message(f"已添加 {added_count} 个模板到 {list_name}")
            # 保存配置
            self.save_template_config()
        else:
            messagebox.showwarning("重复模板", "所有模板都已存在")

    def delete_selected_templates_from_list(self, template_list, listbox, list_name):
        """从预定义列表中删除选中的模板"""
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("删除错误", "请至少选择一个模板进行删除")
            return

        # 从后往前删除，避免索引变化问题
        for i in reversed(selected_indices):
            template_name = template_list[i]
            listbox.delete(i)
            del template_list[i]

        self.log_message(f"已从 {list_name} 删除 {len(selected_indices)} 个模板")
        # 保存配置
        self.save_template_config()

    def add_template_to_custom_group(self, template_var, group_name):
        """添加模板到自定义组"""
        template_name = template_var.get().strip()
        if not template_name:
            messagebox.showwarning("输入错误", "请输入模板名称")
            return

        if group_name not in self.custom_groups:
            messagebox.showwarning("错误", f"组 '{group_name}' 不存在")
            return

        # 支持逗号分隔的多个模板
        templates = [t.strip() for t in template_name.split(",") if t.strip()]

        group_data = self.custom_groups[group_name]
        group_templates = group_data["templates"]
        listbox = group_data["listbox"]

        added_count = 0
        for template in templates:
            if template not in group_templates:
                group_templates.append(template)
                listbox.insert(tk.END, template)
                added_count += 1

        if added_count > 0:
            template_var.set("")
            self.save_custom_groups()
            self.log_message(f"已添加 {added_count} 个模板到自定义组 '{group_name}'")
        else:
            messagebox.showwarning("重复模板", "所有模板都已存在")

    def delete_selected_templates_from_custom_group(self, group_name):
        """从自定义组中删除选中的模板"""
        if group_name not in self.custom_groups:
            messagebox.showwarning("错误", f"组 '{group_name}' 不存在")
            return

        group_data = self.custom_groups[group_name]
        listbox = group_data["listbox"]
        templates = group_data["templates"]

        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("删除错误", "请至少选择一个模板进行删除")
            return

        # 从后往前删除，避免索引变化问题
        for i in reversed(selected_indices):
            listbox.delete(i)
            del templates[i]

        self.save_custom_groups()
        self.log_message(f"已从自定义组 '{group_name}' 删除 {len(selected_indices)} 个模板")

    def create_custom_group(self):
        """创建自定义模板组"""
        group_name = self.new_group_name_var.get().strip()
        templates_str = self.new_group_templates_var.get().strip()

        if not group_name:
            messagebox.showwarning("输入错误", "请输入组名")
            return

        if not templates_str:
            messagebox.showwarning("输入错误", "请输入模板列表")
            return

        if group_name in ["模板组1", "模板组2", "模板组3", "管理自定义组"]:
            messagebox.showwarning("命名错误", "组名不能使用保留名称")
            return

        # 解析模板列表，支持逗号分隔
        templates = [t.strip() for t in templates_str.split(",") if t.strip()]

        if not templates:
            messagebox.showwarning("输入错误", "模板列表不能为空")
            return

        # 检查组名是否已存在
        if group_name in self.custom_groups or group_name in ["模板组1", "模板组2", "模板组3"]:
            if not messagebox.askyesno("重复组名", f"组 '{group_name}' 已存在，是否覆盖?"):
                return

        # 保存自定义组
        self.custom_groups[group_name] = {"templates": templates}
        self.save_custom_groups()

        # 如果选项卡已存在，先删除
        for i in range(self.template_notebook.index("end")):
            tab_text = self.template_notebook.tab(i, "text")
            if tab_text == group_name:
                self.template_notebook.forget(i)
                break

        # 创建新的选项卡
        self.create_custom_group_tab(group_name, templates)

        # 清空输入
        self.new_group_name_var.set("")
        self.new_group_templates_var.set("")

        # 更新现有组列表
        self.update_existing_groups_list()

        self.log_message(f"已创建自定义模板组: {group_name}")

    def delete_custom_group(self, group_name):
        """删除自定义模板组"""
        if group_name in self.custom_groups:
            del self.custom_groups[group_name]
            self.save_custom_groups()

            # 删除对应的选项卡
            for i in range(self.template_notebook.index("end")):
                tab_text = self.template_notebook.tab(i, "text")
                if tab_text == group_name:
                    self.template_notebook.forget(i)
                    break

            self.update_existing_groups_list()
            self.log_message(f"已删除自定义模板组: {group_name}")

    def delete_selected_group(self):
        """删除选中的自定义组"""
        selection = self.existing_groups_listbox.curselection()
        if not selection:
            messagebox.showwarning("删除错误", "请先选择要删除的组")
            return

        group_name = self.existing_groups_listbox.get(selection[0])
        self.delete_custom_group(group_name)

    def update_existing_groups_list(self):
        """更新现有自定义组列表"""
        self.existing_groups_listbox.delete(0, tk.END)
        for group_name in self.custom_groups:
            self.existing_groups_listbox.insert(tk.END, group_name)

    def connect_ac(self):
        try:
            device_name = self.device_name_var.get().strip()
            if not device_name:
                messagebox.showwarning("输入错误", "请输入设备名称")
                return

            # 如果输入的设备名不在列表中，添加到列表
            if device_name not in self.device_names:
                self.device_names.append(device_name)
                self.device_combo.config(values=self.device_names)
                self.log_message(f"已添加新设备到列表: {device_name}")
                # 保存设备配置
                self.save_device_names()

            self.AC = connect(device_name)
            self.connection_status.config(text="已连接", foreground="green")
            self.execute_btn.config(state="normal")
            self.log_message(f"成功连接到设备: {device_name}")
        except Exception as e:
            self.log_message(f"连接失败: {str(e)}")
            messagebox.showerror("连接错误", f"无法连接到设备: {str(e)}")

    def add_device(self):
        device_name = self.device_name_var.get().strip()
        if not device_name:
            messagebox.showwarning("输入错误", "请输入设备名称")
            return

        if device_name in self.device_names:
            messagebox.showwarning("重复设备", f"设备 '{device_name}' 已存在")
            return

        self.device_names.append(device_name)
        self.device_combo.config(values=self.device_names)
        self.log_message(f"已添加设备: {device_name}")
        # 保存设备配置
        self.save_device_names()

    def delete_device(self):
        device_name = self.device_name_var.get().strip()
        if not device_name:
            messagebox.showwarning("输入错误", "请输入要删除的设备名称")
            return

        if device_name not in self.device_names:
            messagebox.showwarning("设备不存在", f"设备 '{device_name}' 不在列表中")
            return

        if len(self.device_names) <= 1:
            messagebox.showwarning("删除错误", "至少需要保留一个设备")
            return

        self.device_names.remove(device_name)
        self.device_combo.config(values=self.device_names)
        self.log_message(f"已删除设备: {device_name}")
        # 保存设备配置
        self.save_device_names()

        # 如果删除的是当前选中项，清空输入框
        if self.device_name_var.get() == device_name:
            self.device_name_var.set("")

    def get_selected_templates(self):
        """获取所有选中的模板"""
        selected = []

        # 检查预定义组
        for list_name in ["moban1", "moban2", "moban3"]:
            listbox = getattr(self, f"{list_name}_listbox", None)
            if listbox:
                indices = listbox.curselection()
                template_list = getattr(self, list_name)
                for i in indices:
                    selected.append(template_list[i])

        # 检查自定义组
        for group_name, group_data in self.custom_groups.items():
            if "listbox" in group_data:
                listbox = group_data["listbox"]
                indices = listbox.curselection()
                templates = group_data["templates"]
                for i in indices:
                    selected.append(templates[i])

        return selected

    def execute_operation(self):
        if not self.AC:
            messagebox.showwarning("警告", "请先连接AC设备")
            return

        selected_templates = self.get_selected_templates()
        if not selected_templates:
            messagebox.showwarning("警告", "请选择至少一个服务模板")
            return

        mode = self.operation_mode.get()

        try:
            if mode == 1:  # 绑定
                for template in selected_templates:
                    self.AC.send(f'''
                                radio 1
                                service-template {template}
                                radio 2
                                service-template {template}
                                radio 3
                                service-template {template}
                               
                                ''')
                self.log_message(f"成功绑定模板: {', '.join(selected_templates)}")
            else:  # 取消绑定
                for template in selected_templates:
                    self.AC.send(f'''
                                radio 1
                                undo service-template {template}
                                
                                radio 2
                                undo service-template {template}
                                
                                radio 3
                                undo service-template {template}
                                
                                ''')
                self.log_message(f"成功取消绑定模板: {', '.join(selected_templates)}")

            messagebox.showinfo("操作完成", "命令已发送到设备")
        except Exception as e:
            self.log_message(f"操作失败: {str(e)}")
            messagebox.showerror("执行错误", f"操作失败: {str(e)}")

    def save_custom_groups(self):
        """保存自定义模板组到文件"""
        try:
            with open("custom_template_groups.json", "w", encoding="utf-8") as f:
                json.dump(self.custom_groups, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"保存自定义组失败: {str(e)}")

    def save_template_config(self):
        """保存模板配置到文件"""
        try:
            template_config = {
                "moban1": self.moban1,
                "moban2": self.moban2,
                "moban3": self.moban3
            }
            with open("template_config.json", "w", encoding="utf-8") as f:
                json.dump(template_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"保存模板配置失败: {str(e)}")

    def save_device_names(self):
        """保存设备名称列表到文件"""
        try:
            with open("device_names.json", "w", encoding="utf-8") as f:
                json.dump(self.device_names, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"保存设备名称失败: {str(e)}")

    def load_custom_groups(self):
        """从文件加载自定义模板组"""
        try:
            if os.path.exists("custom_template_groups.json"):
                with open("custom_template_groups.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # 检查文件是否为空
                        self.custom_groups = json.loads(content)
                        # 确保格式正确
                        for group_name in self.custom_groups:
                            if isinstance(self.custom_groups[group_name], list):
                                self.custom_groups[group_name] = {"templates": self.custom_groups[group_name]}
        except json.JSONDecodeError as e:
            # 如果JSON格式错误，删除损坏的文件
            if os.path.exists("custom_template_groups.json"):
                os.remove("custom_template_groups.json")
            print(f"JSON格式错误，已删除损坏的配置文件: {str(e)}")
        except Exception as e:
            print(f"加载自定义组失败: {str(e)}")

    def load_template_config(self):
        """从文件加载模板配置"""
        try:
            if os.path.exists("template_config.json"):
                with open("template_config.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # 检查文件是否为空
                        template_config = json.loads(content)
                        if "moban1" in template_config:
                            self.moban1 = template_config["moban1"]
                        if "moban2" in template_config:
                            self.moban2 = template_config["moban2"]
                        if "moban3" in template_config:
                            self.moban3 = template_config["moban3"]
        except json.JSONDecodeError as e:
            # 如果JSON格式错误，删除损坏的文件
            if os.path.exists("template_config.json"):
                os.remove("template_config.json")
            print(f"模板配置JSON格式错误，已删除损坏的配置文件: {str(e)}")
        except Exception as e:
            print(f"加载模板配置失败: {str(e)}")

    def load_device_names(self):
        """从文件加载设备名称列表"""
        try:
            if os.path.exists("device_names.json"):
                with open("device_names.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # 检查文件是否为空
                        self.device_names = json.loads(content)
        except json.JSONDecodeError as e:
            # 如果JSON格式错误，删除损坏的文件
            if os.path.exists("device_names.json"):
                os.remove("device_names.json")
            print(f"设备名称JSON格式错误，已删除损坏的配置文件: {str(e)}")
        except Exception as e:
            print(f"加载设备名称失败: {str(e)}")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ACServiceTemplateApp(root)
    root.mainloop()
