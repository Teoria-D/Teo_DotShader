# Teo_DotShader
Maya(Arnold)においてドット絵風の表現ができるシェーダーです。
使用するにあたって注意点が2つあります。

1.Arnold SettingsからFilterをContourに設定すること(設定しないとトゥーンのアウトラインが出ません)

2.レンダリング解像度を低め(320x180や200x150)に設定し、Rampに繋がっているRepeatUを横解像度÷2,RepeatVを縦解像度÷2に設定すること
