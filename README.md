# DeleteOnTime
a GUI software to delete the specified files as you planned

用法（英文）：
1. 把你的图标放在同一个文件夹下，并重命名为icon.ico，运行ico.py，会出现一个qq.py，保留即可。
2. 通过Pyinstaller将py程序(ui.py,DeleteOverdue.py)打包为exe程序，不要更改DeleteOverdue.pyd的名称(包括打包后的exe)。
3. 将 winSW-x64.exe 和 winSW-x64.xml 保存在您的文件夹中（如果您的电脑是 x86 或其他电脑，您应该访问项目 Winsw/Releases WinSW v2.12.0 下载您的版本并将其放在同一文件夹中，然后更改 名字和以前一样）
4. 运行ui.exe并按照计划选择要清理的路径，设置扫描指定文件夹的时间间隔，然后设置要删除多久之前的文件时间（以秒为单位）。
5. 然后点击检查服务状态以确认其已卸载。 然后单击“安装为服务”按钮。 稍等一下，服务就会被安装并启动。
6. 然后你可以关闭ui.exe，记住不要删除文件夹中的任何内容。

usage（English）:
1. put your icon in the same folder, and rename it to icon.ico, run the ico.py, and a qq.py will appear then keep it.
2. pack the py program(ui.py,DeleteOverdue.py) to exe program by Pyinstaller, don't change the name of DeleteOverdue.py.
3. keep the winSW-x64.exe and winSW-x64.xml in your folder(if your pc is x86 or others, your should access to project Winsw/Releases WinSW v2.12.0 download your version and put it on same folder then change the name same as before)
4. run ui.exe and choose the path that you want Clean up as you planned, set the time interval to scan the specified folder, and then Set how long before the time of the file that you want to delete.
5. then check the service status to confirm it's uninstalled. then click the button Install to service. wait a second, the service will be installed and started.
6. then you can close the ui.exe and just enjoy, remember that don't delete anything in the folder. 
