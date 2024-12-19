test

本文件夹的项目作用是爬取文献【期刊 和 论文 分别】的基本信息 获取文献列表

结果以xlsx的行书输出到output文件夹

针对的文献网站：[中国地质图书馆远程访问服务系统 (cgl.org.cn)](https://vpn.cgl.org.cn/login)

1.1_info_qikan.py 期刊类型

1.2_info_lunwen.py 论文类型

不同类型html元素标签不同

---

others其中的download_caj.py，为了从地质图书馆直接下载pdf但是不好用，弃用 具体从cnki下，见2.0_cnki_download：

参考：[关于python的selenium控制已经打开的edge浏览器_python selenium edge-CSDN博客](https://blog.csdn.net/weixin_47420059/article/details/132135409?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-132135409-blog-130642826.235%5Ev43%5Econtrol&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-132135409-blog-130642826.235%5Ev43%5Econtrol&utm_relevant_index=2)

在edge和edgedriver[这两个放一起 为了在已经打开的edge浏览器进行操作 保留登录状态]的exe目录下[打开cmd](https://so.csdn.net/so/search?q=%E6%89%93%E5%BC%80cmd&spm=1001.2101.3001.7020) 。

在cmd中输入

msedge.exe --remote-debugging-port=9222 --user-data-dir="D:\python\seleniumEdge"

* [ ] edge的exe目录：C:\Program Files (x86)\Microsoft\Edge\Application    【在这个cmd】
* [ ] edgedriver的目录：D:\b_installenv\edgedriver_win64

执行命令后在打开的edge浏览器登录中国地质图书馆 保留登陆状态 执行download_caj.py开始下载操作

---

caj2pdf非常好用的工具：[sainnhe/caj2pdf-qt: CAJ 转 PDF 转换器（GUI 版本）](https://github.com/sainnhe/caj2pdf-qt)
