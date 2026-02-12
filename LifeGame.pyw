import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import copy
import json
import os
Version = 2.2
# 调整参数：适配普通屏幕，避免窗口过大
ROWS = 40  # 网格行数
COLS = 40  # 网格列数
SPACE = 20  # 格子边长
root = tk.Tk() 
root.title('生命游戏（Turbo版）')

# 全局变量调整
list_live = [[0 for _ in range(COLS)] for _ in range(ROWS)] 
is_running = False  # 游戏是否正在运行
current_delay = 500  # 当前帧率对应的延迟时间（毫秒），默认500ms（2帧/秒）
SAVE_DIR = "saves"  # 保存文件夹名称（替代原单个保存文件）

# 自动创建saves文件夹（不存在则创建）
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# ---------------------- 控制器面板搭建（优化保存/加载功能） ----------------------
control_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# 1. 启动/暂停按钮（直接控制）
def toggle_running():
    global is_running
    is_running = not is_running
    btn_start['text'] = "暂停" if is_running else "启动"

btn_start = tk.Button(control_frame, text="启动", command=toggle_running, width=10)
btn_start.pack(side=tk.LEFT, padx=5, pady=3)

# 2. 帧率调节（通过延迟时间控制，延迟越小帧率越高）
def adjust_fps():
    global current_delay
    new_delay = simpledialog.askinteger("帧率调节", "请输入每帧延迟时间（毫秒，100-1000）：",
                                        initialvalue=current_delay, minvalue=100, maxvalue=1000)
    if new_delay is not None:  # 用户未点击取消
        current_delay = new_delay
        lbl_fps['text'] = f"当前帧率：≈{int(1000/current_delay)}帧/秒"

tk.Label(control_frame, text="帧率调节：").pack(side=tk.LEFT, padx=2)
btn_fps = tk.Button(control_frame, text="设置延迟", command=adjust_fps, width=10)
btn_fps.pack(side=tk.LEFT, padx=5, pady=3)
lbl_fps = tk.Label(control_frame, text=f"当前帧率：≈{int(1000/current_delay)}帧/秒")
lbl_fps.pack(side=tk.LEFT, padx=2)

# 3. 保存当前状态（支持用户自定义文件名，存储到saves文件夹）
def save_game():
    global list_live, ROWS, COLS, current_delay
    # 第一步：让用户输入自定义文件名
    file_name = simpledialog.askstring("自定义文件名", "请输入保存文件名（无需加.json后缀）：",
                                       initialvalue="life_game_state")
    if not file_name:  # 用户取消或输入为空
        return
    # 拼接完整文件路径（saves/文件名.json）
    save_path = os.path.join(SAVE_DIR, f"{file_name}.json")
    
    # 检查文件是否已存在，避免覆盖
    if os.path.exists(save_path):
        if not messagebox.askyesno("文件已存在", f"{file_name}.json 已存在，是否覆盖？"):
            return
    
    # 准备保存数据
    game_data = {
        "list_live": list_live,
        "ROWS": ROWS,
        "COLS": COLS,
        "current_delay": current_delay
    }
    
    try:
        # 写入JSON文件
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(game_data, f, indent=4)
        messagebox.showinfo("保存成功", f"游戏状态已保存到：\n{save_path}")
    except Exception as e:
        messagebox.showerror("保存失败", f"出现错误：{str(e)}")

btn_save = tk.Button(control_frame, text="保存状态", command=save_game, width=10)
btn_save.pack(side=tk.LEFT, padx=5, pady=3)

# 4. 加载保存的状态（文件选择器，仅显示saves文件夹下的JSON文件）
def load_game():
    global list_live, ROWS, COLS, current_delay, lbl_fps
    # 打开文件选择器，仅筛选JSON文件，默认路径为saves
    load_path = filedialog.askopenfilename(
        title="选择要加载的游戏存档",
        initialdir=SAVE_DIR,  # 默认打开saves文件夹
        filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
    )
    
    if not load_path:  # 用户取消选择
        return
    
    try:
        # 读取JSON文件
        with open(load_path, "r", encoding="utf-8") as f:
            game_data = json.load(f)
        
        # 验证数据完整性
        required_keys = ["list_live", "ROWS", "COLS", "current_delay"]
        if not all(key in game_data for key in required_keys):
            messagebox.showerror("加载失败", "存档文件格式损坏，缺少必要数据！")
            return
        
        # 恢复全局变量
        ROWS = game_data["ROWS"]
        COLS = game_data["COLS"]
        current_delay = game_data["current_delay"]
        list_live = game_data["list_live"]
        
        # 更新界面和绘图
        lbl_fps['text'] = f"当前帧率：≈{int(1000/current_delay)}帧/秒"
        drawMap()
        messagebox.showinfo("加载成功", f"已成功加载存档：\n{os.path.basename(load_path)}")
    except Exception as e:
        messagebox.showerror("加载失败", f"出现错误：{str(e)}")

btn_load = tk.Button(control_frame, text="加载状态", command=load_game, width=10)
btn_load.pack(side=tk.LEFT, padx=5, pady=3)

# 5. 重置游戏
def reset_game():
    global list_live, is_running, current_delay, ROWS, COLS
    if messagebox.askyesno("确认重置", "是否要重置游戏到初始状态？"):
        # 恢复初始状态
        list_live = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        is_running = False
        current_delay = 500
        # 更新界面控件
        btn_start['text'] = "启动"
        lbl_fps['text'] = f"当前帧率：≈{int(1000/current_delay)}帧/秒"
        # 重绘初始空白网格
        drawMap()

btn_reset = tk.Button(control_frame, text="重置游戏", command=reset_game, width=10)
btn_reset.pack(side=tk.LEFT, padx=5, pady=3)

# ---------------------- 游戏逻辑（新增删除元胞机制） ----------------------
# 修正Canvas尺寸：匹配格子尺寸
a1 = tk.Canvas(root, width=ROWS*SPACE, height=COLS*SPACE)

def drawMap():
    """根据元胞状态绘图，先清除旧图形，再绘制新图形"""
    global list_live, a1, ROWS, COLS
    a1.delete("all")
    for i in range(ROWS):
        for j in range(COLS):
            fill_color = 'white' if list_live[i][j] == 1 else 'black'
            a1.create_rectangle(
                i*SPACE, j*SPACE,
                i*SPACE+SPACE, j*SPACE+SPACE,
                fill=fill_color,
                outline='grey',
                width=1
            )

def callback(event):
    """鼠标左键回调：第一次单击创建元胞，第二次单击删除元胞（暂停状态下）"""
    global list_live, is_running
    # 游戏运行中不允许修改
    if is_running:
        messagebox.showwarning("提示", "游戏正在运行，请先暂停再修改细胞状态！")
        return
    # 计算点击的网格索引
    i = int(event.x // SPACE)
    j = int(event.y // SPACE)
    # 边界判断
    if i >= ROWS or j >= COLS:
        return
    
    # 核心：切换元胞状态（1→0，0→1），实现「创建/删除」切换
    if list_live[i][j] == 1:
        # 第二次单击（当前已存活）：删除元胞（置0，绘黑色）
        list_live[i][j] = 0
        fill_color = 'black'
    else:
        # 第一次单击（当前已死亡）：创建元胞（置1，绘白色）
        list_live[i][j] = 1
        fill_color = 'white'
    
    # 实时更新点击位置的图形（无需重绘全部）
    a1.create_rectangle(
        i*SPACE, j*SPACE,
        i*SPACE+SPACE, j*SPACE+SPACE,
        fill=fill_color,
        outline='grey',
        width=1
    )

a1.bind("<Button-1>", callback)  # 绑定鼠标左键点击事件

def getRoundLive(i, j):
    """获取该细胞周围8个邻居的存活数量"""
    global list_live, ROWS, COLS
    num = 0
    directions = [(-1,-1), (-1,0), (-1,1),
                  (0,-1),          (0,1),
                  (1,-1),  (1,0), (1,1)]
    for dx, dy in directions:
        ni, nj = i + dx, j + dy
        if 0 <= ni < ROWS and 0 <= nj < COLS:
            if list_live[ni][nj] == 1:
                num += 1
    return num

def life_week():
    """计算下一周期的细胞存活状态"""
    global list_live, ROWS, COLS
    list_now = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            neighbor_num = getRoundLive(i, j)
            # 康威生命游戏核心规则
            if neighbor_num == 3:
                list_now[i][j] = 1
            elif neighbor_num == 2:
                list_now[i][j] = list_live[i][j]
            else:
                list_now[i][j] = 0
    list_live = copy.deepcopy(list_now)

def my_mainloop():
    """循环执行：生命迭代 + 绘图（仅当游戏运行中）"""
    if is_running:
        life_week()
        drawMap()
    root.after(current_delay, my_mainloop)

# ---------------------- 初始化界面 ----------------------
drawMap()
# 提示信息（更新新增功能说明）
messagebox.showinfo(
    '提示',
    "规则1：如果细胞周围有3个存活的细胞，存活\n"
    "规则2：如果细胞周围有2个存活的细胞，维持不变\n"
    "规则3：其他情况，死亡\n"
    "操作1：暂停状态下，单击网格创建元胞，再次单击同一网格删除元胞\n"
    "操作2：保存/加载存档存储在saves文件夹，支持自定义文件名\n"
    "操作3：通过上方控制器进行启动/暂停、帧率调节、保存/加载、重置操作"
)

a1.pack()
root.after(100, my_mainloop)
root.mainloop()
