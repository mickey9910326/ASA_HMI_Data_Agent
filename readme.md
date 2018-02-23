# ASA_HMI_Data_Agent

## 功能
- 與MCU進行ASA_HMI之封包傳輸 (完成)
- 燒錄ASA_M128
- ASA_M128_STK500 (已完成基本功能)


## TODO List

- HMI  
    1. Handle exception when sending error format.
- ASA_M128_STK500  
    1. 儲存設定功能
    -  signature 驗證功能
    -  Fuse & Lock 獨立讀寫功能
    -  Fuse & Lock BitSelector
- ASA_M128 燒錄
    1. 完成UI
    -  完成燒錄功能
    -  完成燒錄特定檔案功能

## 高 DPI 介面顯示問題
對ASA_HMI_Data_Agent.exe點選右鍵->內容->相容性  
勾選`覆蓋高DPI縮放行為`，並選擇`系統(增強)`
![](https://i.imgur.com/wIiLdOJ.png)
