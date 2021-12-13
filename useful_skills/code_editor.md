vscode的设置都存储在settings.json中，每个键值对对应一项设置

```json
{
    "workbench.colorTheme": "Default Dark+",
    "editor.rulers": [
        79,
        120
    ]
}
```

部分文件位置：

设置：`%APPDATA%\Code\User\settings.json`（`%APPDATA% = C:\Users\current user\AppData\Roaming`）

扩展：`%USERPROFILE%\.vscode\extensions`（`%USERPROFILE% = C:\Users\current user`）

# language-specific settings

```json
"[verilog]": {
    "files.autoGuessEncoding": true
}
```



