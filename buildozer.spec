[app]
title = Voice Cloning App
package.name = voicecloningapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,m4a,ogg,txt,md,pth
version = 0.1
requirements = python3,kivy
orientation = portrait
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b

# DER ENTSCHEIDENDE FIX: Explizit die Build-Tools Version angeben
android.build_tools_version = 33.0.0

android.arch = armeabi-v7a
android.release_artifact = apk
android.enable_androidx = True
android.gradle_parameters = --no-daemon, -Dorg.gradle.jvmargs=-Xmx4G

[buildozer]
log_level = 2
warn_on_deprecated = 1
