# ASA_HMI_Data_Agent ![doc status](https://readthedocs.org/projects/pyserial/badge/?version=latest)


### 功能
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


### TODO List

- HMI
    - Handle exception when sending error format.
- ASA_M128_STK500
    - Add part fuse and lock bits info to improve Bitsselector.
- ASA_M128 燒錄
    - 完成燒錄特定檔案功能

---

### 高 DPI 介面顯示問題
對ASA_HMI_Data_Agent.exe點選右鍵->內容->相容性
勾選`覆蓋高DPI縮放行為`，並選擇`系統(增強)`
![](https://i.imgur.com/wIiLdOJ.png)
