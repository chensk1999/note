# adb

可以下载[Android SDK平台工具](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn)获取，安卓模拟器基本也自带有。完整文档参考[Android Debug Bridge](https://developer.android.com/tools/adb?hl=zh-cn)

## 连接adb

1. 启用USB调试：在设置的“关于本机”界面找到版本号，连续点击若干次进入开发者模式。在开发者选项中打开USB调试
2. 用USB线连接到电脑。若调试模拟器，则在模拟器设置找到端口号，并运行`adb connect 127.0.0.1:port`
3. `adb devices`，如果显示设备名则成功连接

## 常用指令

```shell
adb push $src $dest   # 传文件给手机
adb pull $src $dest   # 从手机下载文件
adb shell             # 进入手机操作系统的shell
```

# 安卓系统分区

- bootloader：相当于电脑的BIOS，可以选择下一步加载boot / recovery分区
- boot：引导进入系统的分区，包含kernel和ramdisk。此分区出错将导致手机无法进入系统，卡在bootloader、无限重启等
- system：安卓操作系统、系统应用程序
- data：用户数据
- cache：缓存
- recovery：正常分区损坏时，可以从bootloader加载此分区，用于恢复其他分区的数据

Android 7.0开始支持A/B分区，系统分区都有“两份”，比如`system_a`和`system_b`。此技术保证无论何时都有一个可用系统，系统更新不会映像用户使用。而自Android 12开始，引入了虚拟A/B分区机制，用动态分区代替了本来的第二个分区

# 刷机

## recovery

俗称卡刷，因为从手机存储卡写入系统

## fastboot

俗称线刷，因为需要从USB线写入系统。fastboot是安卓系统安装工具（安卓启动的引导分区也叫fastboot，两者同名）。Android SDK平台工具中也包括了fastboot，安装adb时一并安装了

- **安装fastboot**：详见[adb](#adb)
- **进入fastboot模式**：在开发者选项打开OEM解锁，运行`adb reboot fastboot`（或者关机后长安电源+音量加进入，不同机型有所不同）
  - 运行`fastboot device`，能找到设备则成功
  - 若`fastboot device`没有结果，但`fastboot --version`正常，可能是缺少驱动。下载[Google USB驱动](https://developer.android.com/studio/run/win-usb)，并[从计算机上的可用驱动程序列表中安装](https://blog.csdn.net/qq_44281591/article/details/134844247)

- **解开Bootloader Lock**：俗称BL锁，必须解锁才能用fastboot写入文件。大多厂商限制用户解锁，先确认机型能否解锁Bootloader Lock
  - 解锁时会抹掉用户数据，而且解锁后就没有保修了。解锁之后每次开机都会显示几秒的警告信息
  - `fastboot flashing unlock`指令解锁（手机厂商未限制解锁才能成功）
- **下载操作系统ROM**：也叫做刷机包、卡刷包、ota映像、固件包（固件包文件格式不同，且比其他几个多了底层映像，需要额外操作）。最好找厂商有没有放出，也可以在[XDA](https://xdaforums.com/c/oneplus.11993/)等网站找。一般是zip压缩包，里面包含系统文件`payload.bin`和一些元数据

- **提取`.img`映像**：用[OTA Pyload Extractor](https://github.com/tobyxdd/android-ota-payload-extractor)提取`.img`映像文件
- **刷机**：进入fastboot模式，运行`fastboot flash boot boot.img`（这个示例将`boot.img`映像刷入boot分区。按需刷入要更改的分区）
- **重启**：`fastboot reboot`

## 高通9008

高通芯片可以通过9008端口直接将固件写入手机。这种刷机方式比fastboot更底层，不需要解开bootloader锁，并且即使无法开机也能使用。不过仅限使用高通芯片的手机可用，下面的方法仅供参考

1. 安装刷机工具、配套驱动和固件包。三者是配套的，找不到成套工具就几乎可以放弃了
2. 手机进入9008模式并连接电脑
   - 长按音量加&音量减，或者音量减&电源。不同型号方法不同。若能开机也可以用`adb reboot edl`，`fastboot oem edl`
   - 若电脑设备管理器有“Qualcomm HS-USB QDLoader 9008”设备，且刷机工具能连接手机则成功。如果显示其他设备名称，或者刷机工具连不上手机，则大概率是驱动问题
3. 使用刷机工具刷入固件包

# root

获取root权限后可以进行许多不安全的操作，网上也有许多伪装成正常工具的恶意工具。不要在root过的设备上进行敏感操作，尤其是存储隐私信息、进行支付

## magisk

用magisk获取root权限之前，需要解开Bootloader锁，并准备好系统ROM的`payload.bin`文件。这两个如何操作详见[fastboot刷机](#fastboot)

1. 安装[Magisk](https://github.com/topjohnwu/Magisk)；将`payload.bin`文件复制到手机
2. 破解boot映像：Magisk - 安装 - 选择并修补一个文件 - 选择`payload.bin` - 开始。操作完成后，将生成的`magisk_patched.img`文件（默认放在`/sdcard/Download`）复制到电脑上
3. 将破解的映像写入boot分区：`fastboot flash boot magisk_patched.img`，然后`fastboot reboot`重启
4. 再次打开Magisk，若“当前”显示版本号、超级用户和模块界面不再是灰色，则root成功

**隐藏root环境**

root之后可以进行大量不安全的操作，因此许多会检测手机是否root，并拒绝在root环境中运行。参考[Magisk隐藏](https://magiskcn.com/hide-the-magisk-app.html)

1. 更改包名：设置 - 隐藏Magisk，随便输入一个名称，Magisk就会把应用名改为此名称
2. 在zygote中运行：设置 - 勾选Zygisk，然后重启手机
3. 使用shamiko隐藏root：下载[shamiko](https://github.com/LSPosed/LSPosed.github.io/releases/tag/shamiko-383)，模块 - 从本地安装，安装完成后重启
   - 配置黑名单：在设置 - 配置排除列表选择应用。排除列表内的应用无法直接看到root环境
   - 配置白名单：创建`/data/adb/shamiko/whitelist`文件，若模块界面中显示"shamiko is working as whitelist mode"则成功。只有白名单内的应用可以看到root环境

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

