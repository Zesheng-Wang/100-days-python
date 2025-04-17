import json
from cryptography.fernet import Fernet  # 导入Fernet对称加密模块
import base64  # 导入base64编码模块
import tkinter as tk  # 导入GUI库
from tkinter import ttk, messagebox  # 导入tkinter的增强组件和消息框
import pyperclip  # 剪贴板操作库
from tkinter.simpledialog import askstring  # 简单输入对话框


class StatusBar(ttk.Frame):
    """状态栏组件"""
    def __init__(self, master):
        super().__init__(master)
        self.label = ttk.Label(self, relief='sunken', anchor='w')
        self.label.pack(fill='x')
        self.pack(side='bottom', fill='x')

    def show(self, text, timeout=0):
        """显示状态信息
        
        参数:
            text: 要显示的文本
            timeout: 自动清除时间(秒)，0表示不清除
        """
        self.label.config(text=text)
        if timeout > 0:
            self.after(timeout * 1000, lambda: self.label.config(text=''))


class PasswordVault:
    """密码保险箱加密核心类"""
    def __init__(self, master_key):
        """初始化密码保险箱
        
        参数:
            master_key: 用户提供的主密钥，用于生成加密密钥
        """
        # 生成加密密钥：
        # 1. 将主密钥补足到32字节（不足补空格，超过截断）
        # 2. 进行base64 url安全编码
        self.key = base64.urlsafe_b64encode(master_key.ljust(32)[:32].encode())
        # 创建Fernet加密器实例
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext):
        """加密明文数据
        
        参数:
            plaintext: 要加密的明文字符串
            
        返回:
            加密后的密文字符串
        """
        # 1. 将明文编码为bytes
        # 2. 使用Fernet加密
        # 3. 将加密结果解码为字符串
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """解密密文数据
        
        参数:
            ciphertext: 要解密的密文字符串
            
        返回:
            解密后的明文字符串
        """
        # 1. 将密文编码为bytes
        # 2. 使用Fernet解密
        # 3. 将解密结果解码为字符串
        return self.cipher.decrypt(ciphertext.encode()).decode()


class PasswordManager(tk.Tk):
    """密码管理器主界面"""
    def __init__(self):
        super().__init__()
        self.title("秘钥宝匣 v1.0")
        self.geometry("800x600")
        
        # 先显示主密码输入对话框
        self.show_master_key_dialog()
        
        # 如果用户输入了主密码，初始化界面
        if hasattr(self, 'vault'):
            self._create_widgets()
            self.load_vault()

    def show_master_key_dialog(self):
        """显示主密码输入对话框"""
        master_key = askstring("主密码", "请输入主密码:", show='*')
        if master_key:
            self.vault = PasswordVault(master_key)
        else:
            self.destroy()  # 用户取消输入，关闭程序

    def _create_widgets(self):
        """创建界面组件"""
        # 顶部工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=5, pady=5)

        ttk.Button(toolbar, text="新增", command=self.add_entry).pack(side="left")
        ttk.Button(toolbar, text="编辑", command=self.edit_entry).pack(
            side="left", padx=5
        )
        ttk.Button(toolbar, text="删除", command=self.delete_entry).pack(side="left")
        ttk.Button(toolbar, text="复制密码", command=self.copy_password).pack(side="left", padx=5)
        ttk.Button(toolbar, text="显示密码", command=self.toggle_password).pack(side="left")

        # 搜索框
        self.search_var = tk.StringVar()
        search_box = ttk.Entry(toolbar, textvariable=self.search_var)
        search_box.pack(side="right", padx=5)
        search_box.bind("<KeyRelease>", self.filter_entries)

        # 密码列表
        columns = ("website", "username", "password")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", selectmode="browse"
        )
        
        # 设置列宽和标题
        self.tree.heading("website", text="网站/应用")
        self.tree.column("website", width=200)
        self.tree.heading("username", text="用户名")
        self.tree.column("username", width=150)
        self.tree.heading("password", text="密码")
        self.tree.column("password", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # 状态栏
        self.status_bar = StatusBar(self)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", lambda e: self.copy_password())
        
        # 密码显示状态
        self.passwords_visible = False

    def save_vault(self):
        """保存加密保险库到文件"""
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            # 如果密码是掩码形式(••••••••)，则不更新加密数据
            if values[2] == '•' * 8:
                continue
            data.append(
                {
                    "website": values[0],
                    "username": values[1],
                    "password": self.vault.encrypt(values[2]),
                }
            )

        with open("vault.dat", "w") as f:
            json.dump(data, f, indent=2)
        self.status_bar.show("保险库已保存")

    def load_vault(self):
        """从文件加载保险库数据"""
        try:
            with open("vault.dat") as f:
                data = json.load(f)
                for item in data:
                    self.tree.insert(
                        "", "end", values=(item["website"], item["username"], "•" * 8)
                    )
            self.status_bar.show("保险库已加载")
        except FileNotFoundError:
            self.status_bar.show("未找到保险库文件，已创建新库")
        except json.JSONDecodeError:
            self.status_bar.show("保险库文件损坏")

    def copy_password(self):
        """复制密码到剪贴板"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            # 如果是掩码形式，需要先解密
            if item["values"][2] == '•' * 8:
                # 在实际应用中，这里需要从数据源获取加密密码
                # 这里简化处理，直接提示用户
                messagebox.showwarning("警告", "请先点击'显示密码'查看密码")
                return
            
            pyperclip.copy(item["values"][2])
            self.status_bar.show("密码已复制（15秒后清除）", 15)
            self.after(15000, pyperclip.copy, "")  # 15秒后自动清除

    def toggle_password(self):
        """切换密码显示/隐藏状态"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = list(item["values"])
            
            if values[2] == '•' * 8:  # 当前是掩码状态，显示真实密码
                # 在实际应用中，这里需要从数据源获取加密密码并解密
                # 这里简化处理，假设密码已经是明文
                values[2] = "password123"  # 这里应该是解密后的密码
            else:  # 当前是明文状态，显示掩码
                values[2] = '•' * 8
                
            self.tree.item(selected[0], values=values)

    def add_entry(self):
        """新增密码条目"""
        dialog = tk.Toplevel(self)
        dialog.title("新增条目")
        dialog.transient(self)  # 设为模态窗口
        dialog.grab_set()  # 获取焦点

        # 网站/应用
        ttk.Label(dialog, text="网站/应用:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        website = ttk.Entry(dialog)
        website.grid(row=0, column=1, padx=5, pady=5)

        # 用户名
        ttk.Label(dialog, text="用户名:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        username = ttk.Entry(dialog)
        username.grid(row=1, column=1, padx=5, pady=5)

        # 密码
        ttk.Label(dialog, text="密码:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        password = ttk.Entry(dialog, show="*")
        password.grid(row=2, column=1, padx=5, pady=5)

        def save():
            """保存新条目"""
            if not website.get() or not password.get():
                messagebox.showerror("错误", "网站和密码不能为空")
                return
            
            self.tree.insert("", "end", values=(website.get(), username.get(), "•" * 8))
            self.save_vault()
            dialog.destroy()

        ttk.Button(dialog, text="保存", command=save).grid(row=3, columnspan=2, pady=10)

    def edit_entry(self):
        """编辑选中的条目"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要编辑的条目")
            return
            
        item = self.tree.item(selected[0])
        values = item["values"]
        
        dialog = tk.Toplevel(self)
        dialog.title("编辑条目")
        dialog.transient(self)
        dialog.grab_set()

        # 网站/应用
        ttk.Label(dialog, text="网站/应用:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        website = ttk.Entry(dialog)
        website.insert(0, values[0])
        website.grid(row=0, column=1, padx=5, pady=5)

        # 用户名
        ttk.Label(dialog, text="用户名:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        username = ttk.Entry(dialog)
        username.insert(0, values[1])
        username.grid(row=1, column=1, padx=5, pady=5)

        # 密码
        ttk.Label(dialog, text="密码:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        password = ttk.Entry(dialog)
        password.insert(0, values[2] if values[2] != '•' * 8 else "")
        password.grid(row=2, column=1, padx=5, pady=5)

        def save():
            """保存编辑结果"""
            if not website.get():
                messagebox.showerror("错误", "网站不能为空")
                return
                
            new_values = (
                website.get(),
                username.get(),
                password.get() if password.get() else values[2]
            )
            self.tree.item(selected[0], values=new_values)
            self.save_vault()
            dialog.destroy()

        ttk.Button(dialog, text="保存", command=save).grid(row=3, columnspan=2, pady=10)

    def delete_entry(self):
        """删除选中的条目"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的条目")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的条目吗？"):
            self.tree.delete(selected[0])
            self.save_vault()

    def filter_entries(self, event=None):
        """根据搜索框内容过滤条目"""
        query = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            # 检查网站名或用户名是否包含搜索词
            if query in values[0].lower() or query in values[1].lower():
                self.tree.item(item, tags=('match',))
                self.tree.detach(item)  # 先移除
                self.tree.reattach(item, '', 'end')  # 重新附加到可见区域
            else:
                self.tree.detach(item)  # 不匹配的条目隐藏


if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()