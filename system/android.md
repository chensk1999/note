# adb

可以下载[Android SDK平台工具](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn)获取，安卓模拟器基本也自带有。完整文档参考[Android Debug Bridge](https://developer.android.com/tools/adb?hl=zh-cn)

## 连接adb

1. 启用USB调试：在设置的“关于本机”界面找到版本号，连续点击若干次进入开发者模式。在开发者选项中打开USB调试
2. 用USB线连接到电脑。若调试模拟器，则在模拟器设置找到端口号，并运行`adb connect 127.0.0.1:port`
3. `adb devices`，如果显示设备名则成功连接

## 常用指令

```shell
# 设备连接
adb devices           # 查看已连接设备
adb connect $ip:$port # 通过网络连接

# 文件传输
adb push $src $dest   # 传文件给手机
adb pull $src $dest   # 从手机下载文件

# 执行指令
adb shell ls /sdcard
adb shell             # 进入手机操作系统的shell

# 应用管理
adb install app.apk            # 安装应用
adb uninstall com.example.app  # 卸载应用
adb shell pm list packages     # 查看已安装应用
adb shell pm list packages -3  # 查看已安装的第三方应用
adb shell am monitor           # 进入监控模式，启动应用就会显示包名
```

# 刷机

## 安卓系统分区

- bootloader：相当于电脑的BIOS，可以选择下一步加载boot / recovery分区
- boot：引导进入系统的分区，包含kernel和ramdisk。此分区出错将导致手机无法进入系统，卡在bootloader、无限重启等
- system：安卓操作系统、系统应用程序
- data：用户数据
- cache：缓存
- recovery：正常分区损坏时，可以从bootloader加载此分区，用于恢复其他分区的数据

Android 7.0开始支持A/B分区，系统分区都有“两份”，比如`system_a`和`system_b`。此技术保证无论何时都有一个可用系统，系统更新不会影响用户使用。而自Android 12开始，引入了虚拟A/B分区机制，用动态分区代替了本来的第二个分区

## 刷机方式

### recovery

Recovery模式（恢复模式）是厂商设计的刷机模式，通常功能单一，且具有较严格的签名验证。俗称卡刷，因为从手机存储卡写入系统

- 进入方法：部分机型在在关机界面可以直接选择“高级重启”或“恢复模式”进入；部分机型开机时按特定组合键进入；也可用`adb reboot recovery`命令进入
- 退出方法：长按电源键；Recovery界面内选择系统 - 退出；执行`adb reboot`命令

### fastboot

俗称线刷，因为需要从USB线写入系统。fastboot是安卓系统安装工具（也是安卓启动的引导分区，两者同名）。Android SDK平台工具中包括了fastboot

1. **安装adb**，并连接到手机
2. **进入fastboot模式**：在开发者选项打开OEM解锁，运行`adb reboot fastboot`（或者关机后长按电源+音量加进入，不同机型有所不同）
     - 运行`fastboot device`，能找到设备则成功
     - 若`fastboot device`没有结果，但`fastboot --version`正常，可能是缺少驱动。下载[Google USB驱动](https://developer.android.com/studio/run/win-usb)，并[从计算机上的可用驱动程序列表中安装](https://blog.csdn.net/qq_44281591/article/details/134844247)
3. **解开Bootloader Lock**：俗称BL锁，必须解锁才能用fastboot写入文件。大多厂商限制用户解锁，先确认机型能否解锁Bootloader Lock
     - 解锁时会抹掉用户数据，而且解锁后就没有保修了。解锁之后每次开机都会显示几秒的警告信息
     - `fastboot flashing unlock`指令解锁（手机厂商未限制解锁才能成功）
4. **下载操作系统ROM**：也叫做刷机包、卡刷包、ota映像、固件包（固件包文件格式不同，且比其他几个多了底层映像，需要额外操作）。最好找厂商有没有放出，也可以在[XDA](https://xdaforums.com/c/oneplus.11993/)等网站找。一般是zip压缩包，里面包含系统文件`payload.bin`和一些元数据
5. **提取`.img`映像**：用[OTA Pyload Extractor](https://github.com/tobyxdd/android-ota-payload-extractor)提取`.img`映像文件
6. **刷机**：进入fastboot模式，运行`fastboot flash boot boot.img`（这个示例将`boot.img`映像刷入boot分区。按需刷入要更改的分区）
7. **重启**：`fastboot reboot`

### 高通9008

高通芯片可以通过9008端口直接将固件写入手机。这种刷机方式比fastboot更底层，不需要解开bootloader锁，并且即使无法开机也能使用。不过仅限使用高通芯片的手机可用，下面的方法仅供参考

1. 安装刷机工具、配套驱动和固件包。三者是配套的，找不到成套工具就几乎可以放弃了
2. 手机进入9008模式并连接电脑
   - 长按音量加&音量减，或者音量减&电源。不同型号方法不同。若能开机也可以用`adb reboot edl`，`fastboot oem edl`
   - 若电脑设备管理器有“Qualcomm HS-USB QDLoader 9008”设备，且刷机工具能连接手机则成功。如果显示其他设备名称，或者刷机工具连不上手机，则大概率是驱动问题
3. 使用刷机工具刷入固件包

## root

获取root权限后可以进行许多不安全的操作。网上也有许多伪装成正常Root工具 / 插件的恶意工具，**不要在root过的设备上进行敏感操作**，尤其是存储隐私信息、进行支付

目前（2026）主流的Root方式是Magisk

**原理**

Magisk通过修改启动镜像`boot.img`，挂载覆盖部分系统文件，允许某些进程切换到root权限（可以简单理解为注入了一个`su`程序）。系统启动后，Magisk核心进程以root权限运行，其他APP尝试`su`时，Magisk会弹出窗口询问用户授权

**流程**

1. 前置准备：解开Bootloader锁，并准备好系统ROM的`payload.bin`文件。操作方法详见[fastboot刷机](#fastboot)
2. 安装[Magisk](https://github.com/topjohnwu/Magisk)；将`payload.bin`文件复制到手机
3. 破解boot映像：Magisk - 安装 - 选择并修补一个文件 - 选择`payload.bin` - 开始。操作完成后，将生成的`magisk_patched.img`文件（默认放在`/sdcard/Download`）复制到电脑上
4. 将破解的映像写入boot分区：`fastboot flash boot magisk_patched.img`，然后`fastboot reboot`重启
5. 再次打开Magisk，若“当前”显示版本号、超级用户和模块界面不再是灰色，则root成功

**隐藏root环境**

root之后可以进行大量不安全的操作，因此许多会检测手机是否root，并拒绝在root环境中运行。参考[Magisk隐藏](https://magiskcn.com/hide-the-magisk-app.html)

1. 更改包名：设置 - 隐藏Magisk，随便输入一个名称，Magisk就会把应用名改为此名称
2. 在zygote中运行：设置 - 勾选Zygisk，然后重启手机
3. 使用shamiko隐藏root：下载[shamiko](https://github.com/LSPosed/LSPosed.github.io/releases/tag/shamiko-383)，模块 - 从本地安装，安装完成后重启
   - 配置黑名单：在设置 - 配置排除列表选择应用。排除列表内的应用无法直接看到root环境
   - 配置白名单：创建`/data/adb/shamiko/whitelist`文件，若模块界面中显示"shamiko is working as whitelist mode"则成功。只有白名单内的应用可以看到root环境

# APP抓包

## CA证书

- **Android 7前**：用户证书和系统证书有相同权限，直接安装为用户证书即可
- **Android 7-13**：用户证书和系统证书分开，系统证书存储于`/system/etc/security/cacerts`。但是普通用户没有访问system目录的权限，root用户也可能没有写system目录的权限。有的软件会信任用户证书，直接安装用户证书即可；若软件不信任用户证书，则需要用后文的方法安装 / 挂载系统证书
- **Android 14后**：系统证书除了system盘，还安装在`/apex/com.android.conscrypt/cacerts`，由apex机制管理
- 部分应用程序会使用**证书锁定**（SSL/TLS Pinning），即只信任程序内置的证书，需要逆向或者用[Frida](https://github.com/frida/frida) Hook

以下方法适用于Android 7-13（均需要root权限）

**前置准备**：首先准备好CA证书，用`openssl x509 -in cert.pem -inform PEM -subject_hash_old -noout`计算哈希值，重命名为`哈希值.0`

**方法1**：获取root权限，直接写入系统证书目录。若无法获取写权限（如：显示`Read-only file system`），说明system盘使用了只读文件系统，要用其他方法

```shell
# 获取super user权限。可能需要在手机上点确认。若shell的$变为#说明成功
su
# 获取写系统分区权限。不同系统需要的命令不同，建议逐一尝试
mount -o rw,remount /system
mount -o rw,remount /
chmod 777 /system
# 将证书复制到系统证书目录
cp /sdcard/Download/9a5ba575.0 /system/etc/security/cacerts/
```

**方法2**：magisk加载模块：首先安装magisk，安装[MoveCertificate模块](https://github.com/ys1231/MoveCertificate)，将重命名为`hash值.0`的证书复制到`/data/local/tmp/cert`，重启手机即可生效

**其他**：没有测试过，上面的方法都用不了的时候可以考虑

- DNA修改system.img：使用安卓固件解包打包工具[DNA](https://github.com/ColdWindScholar/D.N.A3)，修改system.img映像并重新刷入
- [HTTP Toolkit](https://httptoolkit.com/docs/guides/android/)工具抓包，原理似乎是挂载了一个内存文件系统，参考[这篇文章](http://91fans.com.cn/post/certificate/)。其中使用的命令如下

```shell
# 将系统证书复制到临时文件夹
mkdir -m 700 /data/local/tmp/htk-ca-copy
cp /system/etc/security/cacerts/* /data/local/tmp/htk-ca-copy/
# Create the in-memory mount on top of the system certs folder
mount -t tmpfs tmpfs /system/etc/security/cacerts
# 将系统证书、要添加的证书复制到内存文件系统
mv /data/local/tmp/htk-ca-copy/* /system/etc/security/cacerts/
cp /data/local/tmp/c88f7ed0.0 /system/etc/security/cacerts/
# Update the perms & selinux context labels, so everything is as readable as before
chown root:root /system/etc/security/cacerts/*
chmod 644 /system/etc/security/cacerts/*
chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*
```

# Frida

## 安装

**前置条件**：root

**电脑端**：安装Objection框架，`pip install objection`

**手机端**：

1. 下载[frida-server](https://github.com/frida/frida/releases)并解压，得到`frida-server-<版本号>-<适用硬件>`。若不确定手机硬件，可进入`adb shell`后运行`getprop ro.product.cpu.abi`
2. 复制到手机`/data/local/tmp`目录并`chmod 755`
3. 在手机上运行`frida-server`；然后在电脑上运行`frida-ps -U`，若打印出手机上的进程则说明安装成功
4. 有些教程说需要配置端口转发：`adb forward tcp:27042 tcp:27042`

```bash
# 复制frida-server到手机（还没有root权限，因此先随便复制到一个普通目录）
adb push "frida-server" "/sdcard/Download/frida-server"

# 进入Shell并获得root权限
adb shell
su

# 复制到/data/local/tmp目录，并授予运行权限
mv /sdcard/Download/frida-server /data/local/tmp
chmod 755 /data/local/tmp/frida-server
cd /data/local/tmp

# 运行frida-server
./frida-server &
```

## Objection框架使用

Objection框架是基于Frida的框架，封装了常用操作并提供了较好用的用户界面

```bash
# 进入交互式界面
objection --name com.tencent.mm start
objection -g com.tencent.mm explore  # 旧版本的启动方式

# 解除SSL Pinning
android sslpinning disable
```

备注：查第三方包名`adb shell pm list packages -3`

> 老版本Frida使用包名，新版本Frida使用APP名。APP名必须是点开app后，frida-ps -U显示的那个app名字。

## Frida使用

```bash
# attach模式
frida -U -n com.xxx.app

# spawn模式
frida -U -f com.xxx.app -l script.js
```

参数说明：

- `-U, --usb`：通过usb连接到手机
- attach模式：向正在运行的进程注入代码。只能Hook未来要执行的代码，无法Hook初始化流程，且更容易被检测。通常用于分析UI行为（如按钮点击），或者抓接口参数
  - `-n, --attach-name`：使用attach模式注入到指定的APP
  - `-p, --attach-pid`：使用attach模式注入到指定的PID
- spawn模式：重启进程并注入代码。可以控制整个生命周期，常用于分析或者绕过初始化流程、登录流程
  - `-f, --file`：使用spawn模式注入到指定的APP
- `-l, --load`：加载脚本文件



看到一半的教程：https://www.raingray.com/archives/5070.html#2%20frida-tools

# Xposed

持久化hook

# 其他

本节的操作基本需要root权限（但也不完全如此，比如停用第三方app不需要root，停用系统应用才需要）。进入adb后先用su指令获取超级用户权限：

```shell
su  # 获取超级用户权限。可能需要在手机上点确认。若shell的$变为#说明成功
```

## 备份系统映像

硬盘分区通过symlink挂载在文件系统中，查看`/dev/block/platform/*/by-name`（星号的部分因机型而不同，需要看实际情况调整）便可得知每个分区对应的路径，比如`system_a -> /dev/block/sda13`表示`/dev/block/sda13`目录下是`system_a`分区

```shell
# 查看分区路径
cd /dev/block/platform/"根据机型有所不同"/by-name
ls -l

# 导出为img文件
dd if=/dev/block/sda13 of=/sdcard/Download/system_a.img
```

## 管理权限

第一步需要**找到应用程序的包名**

```shell
# 通过关键词寻找
pm list packages | grep "update"   # 寻找包名带有update的包

# 通过其他信息寻找。dumpsys导出的有包的路径、权限、版本等信息，可以在手机上找到版本号用于搜索
dumpsys package > /sdcard/Download/pkg.txt  # 导出所有包的信息，adb pull到电脑上分析
```

然后就可以**停用应用程序**，或是**管理应用程序权限**

```shell
pm disable $pkg       # 停用
set $perm=android.permission.NOTIFICATION_DURING_SETUP
pm revoke $pkg $perm  # 撤销权限
```

## 杂项

```shell
# 寻找应用的activity名称，其格式为pkg_name/activity_name
# 如com.android.htmlviewer/.HTMLViewerActivity
dumpsys package $pkg | grep $pkg/
# 启动应用
am start -n $pkg/$activity -a android.intent.action.VIEW
```
