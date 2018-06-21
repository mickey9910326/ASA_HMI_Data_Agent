HMI
---

.. image:: _static/image/mainwindow_hmi.png

與ASA_M128進行文字溝通
=====================

STEP 0. ASA_M128程式
````````````````````
本區範例燒錄進ASA_M128之程式碼如下：

.. code-block:: c

    #include "ASA_Lib.h"

    int main() {
        char s[20];
        ASA_M128_set();

        // send message to ASA_HMI_Data_Agent
        printf("hello ASA_HMI_Data_Agent, i am asa_m128.\n");

        // receive message from ASA_HMI_Data_Agent
        scanf("%s", s);

        printf("hello ASA_HMI_Data_Agent, i received %s\n", s);

        return 0;
    }

SETP 1. 開啟串列埠
``````````````````
在串埠設定區塊中之下拉選單選擇當前ASA_M128連接的串列埠，並點選開啟串列埠。

若下拉選單中無選項，請點選更新串列埠按鈕，以更新選單中串列埠。

.. image:: _static/image/hmi/serial_group.png

SETP 2. 接收ASA_M128傳送之文字
`````````````````````````````
將ASA_M128指撥開關撥到RUN模式。

按一下重置鍵RESET，讓ASA_M128開始執行程式

當ASA_M128執行 :code:`printf("hello ASA_HMI_Data_Agent, i am asa_m128.\n");` 後，
文字人機會在文字對話區顯示以">>"加之文字，表示從ASA_M128接收之文字訊息。

.. image:: _static/image/hmi/text_receive.png

SETP 3. 傳送文字給ASA_M128
``````````````````````````
在文字對話區最下方橫條中，輸入欲發送之文字，並點選"Send"之按鈕，將會把文字傳送給
ASA_M128。

.. image:: _static/image/hmi/text_send.png

在此範例中，會接收到ASA_M128的回覆訊息，如下：

文字人機會在文字對話區顯示以"<<"加上文字，表示已發送給ASA_M28之文字訊息。

.. image:: _static/image/hmi/text_receive2.png

接收矩陣資料
===========

STEP 0. ASA_M128程式
````````````````````

本區範例燒錄進ASA_M128之程式碼如下：

.. code-block:: c

    #include "ASA_Lib.h"

    #define HMI_TYPE_I8   0
    #define HMI_TYPE_I16  1
    #define HMI_TYPE_I32  2
    #define HMI_TYPE_I64  3
    #define HMI_TYPE_UI8  4
    #define HMI_TYPE_UI16 5
    #define HMI_TYPE_UI32 6
    #define HMI_TYPE_UI64 7
    #define HMI_TYPE_F32  8
    #define HMI_TYPE_F64  9

    int main() {
        ASA_M128_set();

        float data[5] = {1.1, -1, 0,1, -2.1};
        char s[20];
        char num = 5;

        int bytes = num*sizeof(float); // float is 4 bytes => bytes = 20
        // NOTE float and double both are 4 bytes (32 bits)
        // This is the only supported floating point format in AVR-GCC

        // 傳送文字給文字人機，並等待文字人機回覆OK，再進行矩陣資料傳送
        printf("is HMI ready?\n");
        scanf("%s", s); // wait for HMI response

        // 矩陣資料傳送
        M128_HMI_put(bytes, HMI_TYPE_F32, data); // send data

        return 0;
    }

SETP 1. 開啟串列埠、並執行程式
````````````````````````````
在串埠設定區塊中之下拉選單選擇當前ASA_M128連接的串列埠，並點選開啟串列埠。

若下拉選單中無選項，請點選更新串列埠按鈕，以更新選單中串列埠。

.. image:: _static\image\hmi\serial_group.png

將ASA_M128指撥開關撥到RUN模式。

按一下重置鍵RESET，讓ASA_M128開始執行程式。


SETP 2. 通知ASA_M128準備接收資料
```````````````````````````````
