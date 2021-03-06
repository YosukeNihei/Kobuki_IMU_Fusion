Kobuki_IMU_Fusion
======================
ジャイロモジュール[R1350N][gyro]による角度情報と，Yujin Robotics社より発売されている移動ロボットkobukiのオドメトリを統合し，制御するRTC群です．  
動作には[KobukiAIST][aist]が必要です．  
[gyro]:http://www.switch-science.com/catalog/1016/
[aist]:http://openrtm.org/openrtm/zh-hans/node/273

動作環境
------
**OS:**  
Windows 7 32bit/64bit  
Windows 8 32bit/64bit  
Ubuntu12.04 LTS 32bit  

**RT-Middleware:**  
[OpenRTM-aist Python 1.1.0-RC1][py]  
[py]:http://openrtm.org/openrtm/ja/node/4526

ファイル構成
------

ファイル構成について，一部抜粋で説明します．  

GyroOdometry  
│―GyroOdometry  
│　　　│―cmake    
│　　　│―cmake_modules    
│　　　│―cpack_resources    
│　　　│―doc    
│　　　│―idl    
│　　　│―include    
│　　　│―src        
│　　　│―CMakeLists.txt    
│　　　│―COPYING    
│　　　│―COPYING.LESSER    
│　　　│―GyroOdometry.conf    
│　　　│―GyroOdometry.py   
│　　　│―README.GyroOdometry    
│　　　│―rtc.conf  
│　　　│―RTC.xml  
│　　　│―RTC.xml20131214130332  
│  
│―KobukiMobileControl    
│　　　│―cmake    
│　　　│―cmake_modules    
│　　　│―cpack_resources    
│　　　│―doc    
│　　　│―idl    
│　　　│―include    
│　　　│―src        
│　　　│―CMakeLists.txt    
│　　　│―COPYING    
│　　　│―COPYING.LESSER    
│　　　│―KobukiMobileControl.conf    
│　　　│―KobukiMobileControl.py  
│　　　│―README.KobukiMobileControl    
│　　　│―rtc.conf   
│　　　│―RTC.xml  
│	  
│―TestRTC    
│　　　│―PyTimedPose2DConsoleIn  
│　　　│―PyTimedPose2DConsoleOut  
│  
│―README.md    

  
* GyroOdometry.py  
R1350N用RTC（IMUR1350N）と，Kobukiのような車両ロボットのオドメトリを統合するRTCです．

* KobukiMobileControl.py  
Kobukiを座標指定により位置制御するコントローラRTCです．

* TestRTC   
本RTCの動作確認をするためのTest用RTCが収められています．

システムの概要
------
###1. IMUR1350NとkobukiAISTの統合###
<img src="http://farm8.staticflickr.com/7406/11402233815_454bde738b_o.png" width="400px" />    

kobukiAISTのX,Yオドメトリと，IMUR1350Nによる角度情報を統合します．  
より精度の高いオドメトリを実現します．  

###2. 座標指定によるkobukiの移動制御###
<img src="http://farm6.staticflickr.com/5525/11402230746_423c27ecb6_o.png" width="400px" />    

kobukiを座標指定のみで目標座標まで動かすことができます．  
また，前述のIMUR1350Nとの統合オドメトリを使用することで，位置制御の精度が上がります．
  
RTCの構成
------  
###1. GyroOdometry RTC###
<img src="http://farm3.staticflickr.com/2840/11401112486_5f96b8ac94_o.png" width="400px" />    
データポートは以下のようになっています  

* odometry port :InPort  
データ型; TimedPose2D
[kobukiAIST][kobuki]のような，TimedPose2D型のオドメトリ情報を入力します．
[kobuki]:http://svn.openrtm.org/components/trunk/mobile_robots/kobuki/

* angle port :InPort  
データ型; TimedDoubleSeq
[IMUR1350N][imu]の角度情報を入力します．
[imu]:https://github.com/HiroakiMatsuda/R1350N

* gyroOdometry port :OutPort  
データ型; TimedPose2D
車両ロボットのX,YオドメトリとIMUモジュールの角度情報を統合し，新しいオドメトリとして出力します．
※角度情報の単位はradianです．

###2. KobukiMobileControl RTC###
<img src="http://farm6.staticflickr.com/5528/11401112466_fbd899e9ec_o.png" width="400px" /> 
データポートは以下のようになっています     

* target_pose port :InPort  
データ型; TimedPose2D
目標座標を指定します．  
*現在Headingは指定できません．将来のバージョンで実装します．  

* kobuki_pose port :InPort  
データ型; TimedPose2D
オドメトリ情報を入力します．

* flag port :OutPort  
データ型; TimedBoolean
目標地点まで到達したときTrueを返します．

* kobuki_velocity port :OutPort  
kobukiの動作速度を指令します．  
*将来のバージョンで実装します．  
    
使い方
------

###1. ネームサーバーの起動###
ネームサーバーを起動します．  

Windows:  
Start Naming Serviceで起動します．  
Linux:  
以下のコマンドで起動します．2809はポート番号で任意で選んで構いません．  
$ rtm-naming 2809

###2. RTCの起動###
1. 必要なコンポーネントを起動します．  
・IMUR1350Nを起動します．  
Windows:  
GyroOdometry.pyをダブルクリックで起動します．    
Linux:  
以下のコマンドで起動します．  
$ python GyroOdometry.py  
・KobukiMobileControlを起動します．  
Windows:  
KobukiMobileControl.pyをダブルクリックで起動します．    
Linux:  
以下のコマンドで起動します．  
$ python KobukiMobileControl.py    
・IMUR1350Nを起動します．
詳しくは[こちら][imu]を参照してください．
[imu]:https://github.com/HiroakiMatsuda/R1350N
・KobukiAISTを起動します．
詳しくは[こちら][kobuki]を参照してください．
[kobuki]:http://svn.openrtm.org/components/trunk/mobile_robots/kobuki/

2. テストコンポーネントを起動します
・PyTimedPose2DConsoleIn.pyを起動します．
Windows:  
PyTimedPose2DConsoleIn.pyをダブルクリックで起動します．  
Linux:  
以下のコマンドで起動します．  
$ python PyTimedPose2DConsoleIn.py   
・PyTimedPose2DConsoleOut.pyを起動します．  
Windows:  
PyTimedPose2DConsoleOut.pyをダブルクリックで起動します．  
Linux:  
以下のコマンドで起動します．  
$ python PyTimedPose2DConsoleOut.py 

3. RTCの接続
RT System Editorを使用して，各RTCを接続します．  
<img src="http://farm3.staticflickr.com/2830/11392974476_1855854fc4_o.png" width="500px" />    


###3. 動作確認###
全てのRTCをActivateし，PyTimedPose2DConsoleIn.pyから目標座標を入力します．  
ロボットの座標は，PyTimedPose2DConsoleOut.pyより確認できます．

PyAcceleration3dConsoleOutの実行画面  
<img src="http://farm8.staticflickr.com/7422/11393048003_2b1e3a0ee4_o.png" width="400px" />    


PyTimedPose2DConsoleOutの実行画面   
<img src="http://farm8.staticflickr.com/7420/11392867614_e0083b754e_o.png" width="400px" />    


以上が本RTCの使い方となります.  

LICENSE
----------
* GyroOdometry  and PyTimedPose2DConsoleOut  
Copyright © 2013 Yosuke Nihei
Licensed under the [Apache License, Version 2.0][Apache].  
Distributed under the [MIT License][MIT].  
Dual licensed under the [MIT License][MIT] and [Apache License, Version 2.0][Apache].   


* KobukiMobileControl and PyTimedPose2DConsoleIn  
Copyright © 2013 Hiroaki Matsuda
Licensed under the [Apache License, Version 2.0][Apache].  
Distributed under the [MIT License][MIT].  
Dual licensed under the [MIT License][MIT] and [Apache License, Version 2.0][Apache]. 
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
