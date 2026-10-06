#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, shlex, subprocess, threading, queue, sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

HERE=Path(__file__).resolve().parent
MASTER=HERE/'abaqus_postprocess_master.py'

class PostGUI(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('ODB2VTU-S CPFEM Postprocessor — Linux'); self.geometry('820x500'); self.minsize(720,440)
        self.abaqus=tk.StringVar(value=os.environ.get('ABAQUS_CMD','abaqus')); self.odb=tk.StringVar(); self.out=tk.StringVar(); self.status=tk.StringVar(value='状态：等待选择')
        self.q=queue.Queue(); self.running=False; self.current_op=None
        self.build(); self.after(100,self.drain)
    def build(self):
        main=ttk.Frame(self,padding=15);main.pack(fill='both',expand=True)
        rr=ttk.Frame(main);rr.pack(fill='x',pady=4);ttk.Label(rr,text='Abaqus command',width=16).pack(side='left');ttk.Entry(rr,textvariable=self.abaqus).pack(side='left',fill='x',expand=True);ttk.Label(rr,text='例如 abaqus / abq2024').pack(side='left',padx=6)
        rr=ttk.Frame(main);rr.pack(fill='x',pady=4);ttk.Label(rr,text='ODB 文件',width=16).pack(side='left');ttk.Entry(rr,textvariable=self.odb).pack(side='left',fill='x',expand=True);ttk.Button(rr,text='选择 ODB',command=self.pick_odb).pack(side='left',padx=6)
        rr=ttk.Frame(main);rr.pack(fill='x',pady=4);ttk.Label(rr,text='输出目录',width=16).pack(side='left');ttk.Entry(rr,textvariable=self.out).pack(side='left',fill='x',expand=True);ttk.Button(rr,text='选择目录',command=self.pick_out).pack(side='left',padx=6)
        ttk.Label(main,text='PEEQCP目标帧：下压首/末帧；每个摩擦循环按 StepTime 取 T0/T25/T50/T75/T100。计算仍遍历全部帧。').pack(anchor='w',pady=(8,10))
        grid=ttk.Frame(main);grid.pack(fill='x')
        ttk.Button(grid,text='① 导出 U / RF / CF / COF',command=lambda:self.run('history')).grid(row=0,column=0,sticky='ew',padx=5,pady=5)
        ttk.Button(grid,text='② 计算 PEEQCP（全帧累积/目标帧保存）',command=lambda:self.run('peeq_export')).grid(row=0,column=1,sticky='ew',padx=5,pady=5)
        ttk.Button(grid,text='③ 写回 PEEQCP 到目标帧',command=self.inject).grid(row=1,column=0,sticky='ew',padx=5,pady=5)
        ttk.Button(grid,text='④ 检查目标帧 PEEQCP',command=lambda:self.run('peeq_check')).grid(row=1,column=1,sticky='ew',padx=5,pady=5)
        grid.columnconfigure(0,weight=1);grid.columnconfigure(1,weight=1)
        ttk.Label(main,textvariable=self.status).pack(anchor='w',pady=(10,4))
        self.log=tk.Text(main,height=10,wrap='none');self.log.pack(fill='both',expand=True)
    def pick_odb(self):
        p=filedialog.askopenfilename(filetypes=[('Abaqus ODB','*.odb'),('All files','*')]);
        if p:self.odb.set(p);self.out.set(self.out.get() or str(Path(p).parent));self.status.set('状态：已选择 ODB')
    def pick_out(self):
        d=filedialog.askdirectory();
        if d:self.out.set(d);self.status.set('状态：已选择输出目录')
    def validate(self):
        if not Path(self.odb.get()).exists():messagebox.showerror('提示','请先选择有效 ODB。');return False
        if not self.out.get():messagebox.showerror('提示','请选择输出目录。');return False
        Path(self.out.get()).mkdir(parents=True,exist_ok=True)
        if not MASTER.exists():messagebox.showerror('错误','找不到 abaqus_postprocess_master.py');return False
        return True
    def prefix(self):
        c=self.abaqus.get().strip()
        if not c:raise ValueError('Abaqus command is empty')
        return shlex.split(c)+['python']
    def inject(self):
        if not self.validate():return
        if messagebox.askyesno('写回确认','写回 PEEQCP 前必须关闭 Abaqus/Viewer。\n\n确认继续？'):self.run('peeq_inject')
    def run(self,op):
        if not self.validate() or self.running:return
        cmd=self.prefix()+[str(MASTER),'--operation',op,'--odb',self.odb.get(),'--outroot',self.out.get()]
        self.log.insert('end','$ '+' '.join(shlex.quote(x) for x in cmd)+'\n')
        if op == 'peeq_export':
            self.log.insert('end','提示：oneAPI 初始化完成后将进入 ODB/Q5/PEEQCP 计算；新版会实时刷新后端进度。\n')
        self.log.see('end');self.status.set('状态：运行 '+op);self.running=True;self.current_op=op
        def worker():
            rc=-1
            try:
                env = os.environ.copy()
                env['PYTHONUNBUFFERED'] = '1'
                p=subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                    env=env
                )
                for line in p.stdout:
                    self.q.put(('log',line))
                rc=p.wait()
            except Exception as e:self.q.put(('log','ERROR: %s\n'%e))
            self.q.put(('done',rc))
        threading.Thread(target=worker,daemon=True).start()
    def drain(self):
        try:
            while True:
                t=self.q.get_nowait()
                if t[0]=='log':self.log.insert('end',t[1]);self.log.see('end')
                else:
                    rc=t[1]
                    op=self.current_op
                    self.running=False
                    self.current_op=None
                    self.status.set('状态：完成，返回码 %s'%rc)
                    if rc == 0 and op == 'peeq_export':
                        messagebox.showinfo(
                            'PEEQCP 计算完成',
                            'PEEQCP 计算完成。\n\n已完成全帧累积，并保存下压首/末帧以及每个摩擦循环 T0/T25/T50/T75/T100 的目标帧结果。\n\n可以继续执行：③ 写回 PEEQCP 到目标帧。'
                        )
                    elif rc == 0 and op == 'peeq_inject':
                        messagebox.showinfo(
                            'PEEQCP 写回完成',
                            'PEEQCP 已成功写回 ODB 的目标帧。\n\n请重新打开 Abaqus/Viewer，或点击 ④ 检查目标帧 PEEQCP。'
                        )
                    elif rc != 0 and op in ('peeq_export','peeq_inject'):
                        messagebox.showerror(
                            '运行失败',
                            '%s 未正常完成。\n返回码：%s\n\n请查看窗口中的日志输出。' % (op, rc)
                        )
        except queue.Empty:pass
        self.after(100,self.drain)

if __name__=='__main__':
    try:PostGUI().mainloop()
    except tk.TclError as e:
        sys.stderr.write('GUI startup failed: %s\nUse X11/VNC or run abaqus_postprocess_master.py from CLI.\n'%e);sys.exit(2)
