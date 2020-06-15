加密数据查看器
=============

使用 PyQ55 开发

## 准备工作

```shell
pip3 install PyQt5 PyInstaller pycryptodome
```


## MacOS App 打包

Icon 制作

```shell
iconutil -c icns resources/Icon.iconset
```

打包

```shell
pyinstaller "Delos Data Viewer.spec" --workpath ../build --distpath ../dist  

```

制作 spec 并且打包

```shell

rm -rf ../dist
pyinstaller app.py \
-i resources/Icon.icns \
-w \
--osx-bundle-identifier com.delos.dataviewer \
--name "Delos Data Viewer" \
--add-data=resources:dataviewer/resources \
--distpath ../dist \
--workpath ../build \
--noupx \
--onedir
```
