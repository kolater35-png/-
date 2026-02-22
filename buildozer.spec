[app]
title = Nebula Master Ultra
package.name = nebula_master_ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 8.5.0

requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,certifi

orientation = portrait
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.meta_data = largeHeap=true,kivy.graphics.gles=2
android.window_layout_attribute = android:windowSoftInputMode="adjustResize"
