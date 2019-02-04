# ASA_HMI_Data_Agent (asa develop tools)

![doc status](https://readthedocs.org/projects/asa-hmi-data-agent/badge/?version=latest)

文件(未完成)：  
https://asa-hmi-data-agent.readthedocs.io/en/latest/?badge=latestt

## 簡介

包含許多開法ASA系列周邊會用到的工具，稱作asa develop tools，簡寫為adt。

## 功能

1. 終端與資料傳輸  
    - 作為終端與ASA_M128對話  
    - 透過HMI封包格式，與ASA_M128傳輸大量資料  

2. 燒錄ASA_M128  
    - 利用 [py_asa_loader](https://github.com/mickey9910326/py_asa_loader) 進行燒錄 ASA_M128  
    - 提供GUI方便使用者使用

3. 透過ASA_M128燒錄AVR系列晶片  
    - 利用 [avrdude](http://savannah.nongnu.org/projects/avrdude) 透過 ASA_M128 燒錄AVR系列晶片  
    - 提供GUI讓使用者不用了解avrdude也可以燒錄AVR系列晶片  
    - 提供儲存設定的功能
    - 相關專案 [AVR_SPI_SerialProgramming](https://github.com/mickey9910326/AVR_SPI_SerialProgramming)
      ：在M128上實現的STK500 DEVICE
    - 相關專案 [rev bootloader](https://github.com/nuclear-refugee/bootloader)
      ：提供支援ASAPROG及STK500的botloader，讓ASA_M128在prog模式下可以進行載入執行程式，也可以當作STK500 DEVICE

4. CLI 工具
    - adt_term : 透過CLI介面去控制 adt 的 terminal
    - adt_loader : 透過CLI介面去控制 adt 的ASA燒錄器

## 安裝方法

1. 透過 PYPI 安裝

    ``` shell
    pip install asa-hmi-data-agent
    ```

    可用指令有：
        - asa_hmi_data_agent : 開啟文字人機
        - adt : 開啟文字人機
        - adt_term : 略
        - adt_loader : 略


2. 到發佈頁面下載打包好的執行檔

    發佈頁面： https://github.com/mickey9910326/ASA_HMI_Data_Agent/releases

    可用執行檔有：
        - asa_hmi_data_agent : 開啟文字人機
        - adt_term : 略
        - adt_loader : 略

## CLI工具使用

CLI工具會占用 tcp:\\*:8787 ，請確認TCP埠8787未被占用

1. adt-term

    - `adt-term open [-h] -P PORT [-b BAUDRATE] [-i ID]` 開啟終端機  
        id 預設為1，可用為1及2，若要開啟兩個終端機請到設定調整

    - `adt-term close [-h] [-i ID]` 關閉終端機

    - `adt-term clear [-h] [-i ID]` 清空終端機

2. adt-loader

        usage: adt-loader [-h] [-H HEXFILE] [-P PORT] [-s SET]

        tell adt to load hex into asa-series board

        optional arguments:
        -h, --help            show this help message and exit
        -H HEXFILE, --hex HEXFILE
                                assign hex file to be load
        -P PORT, -p PORT, --port PORT
                                assign the port to load
        -s SET, -S SET, --set SET
                                use existing set (1~N)

## 協助開發

1. 回報程式問題

    直接到 ISSUE 頁面開新 ISSUE，並描述問題發生狀況

2. 新功能需求

    直接到 ISSUE 頁面開新 ISSUE，描述新功能需求

3. 協助程式及文件開發

    像這份readma若有不清楚的地方，可以fork出去並commit後再發PR回來


---
### Q&A

#### Q.桌面高DPI，文字太小
A. 對ASA_HMI_Data_Agent.exe點選右鍵->內容->相容性
勾選`覆蓋高DPI縮放行為`，並選擇`系統(增強)`
![](https://i.imgur.com/wIiLdOJ.png)
