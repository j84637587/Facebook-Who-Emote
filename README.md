# Facebook-Who-Emote
此專案目的在把FB(Facebook)指定之文章中，有做出表情符號的人紀錄其名稱、主頁連結、帳號ID，並以Json格式保存。

保存的檔名為文章的`TargetID`(FB API使用)。

每次請求以500毫秒為間隔來避免造成封包攻擊。


FB API 使用的變數：
- cursor   為資料請求點, API會回傳從此值開始的資料
- TargetID 文章的辨識ID

## 需求
- Python >= 3.9

## 使用方式

1. 取得 Cookie
    1. 前往任一FB網頁並按`F12`開啟`DevTool`
    2. 在`DevTool`切換到`Network`頁面
    3. 在FB網頁隨意瀏覽直到`Network`頁面`Name清單`出現`graphql/`的請求
    4. 瀏覽該請求的`Headers`，並下拉複製`cookie`的值
    5. 將複製的`cookie`值貼製`main.py`的`__COOKIE`
2. 修改 `main.py` 中的文章網址`post_url`。
3. 開始執行嵌入，執行指令 ``` python main.py ``` 。

## DEMO

以 `疾病管制署 - 1922防疫達人`的[此文章](https://www.facebook.com/TWCDC/posts/pfbid0tqufrb9h2BUZyPb7LwF2tBwMSt4q3UAwawmCPFUxW1mWgbsVC6DsKKhRHUSYLK5Al) 為範例之產生部分結果如下圖:
