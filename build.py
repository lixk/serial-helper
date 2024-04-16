import os

print(os.getcwd())
# 编译UI文件
os.chdir('./ui')
os.system('npm run build')
# 打包Python文件
os.chdir('../')
os.system('pyinstaller ./main.py -F -w -n "串口小助手" -i "ui/dist/static/favicon.ico"  --add-data="ui/dist;./ui/dist" -y')
