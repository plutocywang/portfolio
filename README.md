# PLUTO SIGNAL — Pluto Wang Portfolio

Chung-Yi Wang (Pluto) 的導演與影像藝術作品集。黑底、暖白、珊瑚橘（#F28C6F），包含 32 件作品（原有 31 件，加上 Lalamove 廣告）。

## 本機預覽

只需要 Python 3.9 以上，不需要 Node、npm 或第三方套件。

```sh
python3 build.py
python3 -m http.server 8765 --directory dist
```

開啟 http://localhost:8765 。所有正式頁面都在 `dist/`，請勿直接用檔案方式開啟根目錄 `index.html`。

## 修改內容

- `content.json`：作品片名、分類、YouTube ID、說明、首頁主視覺與精選排序。
- `pluto-wordmark.svg`：依原 PLUTO SIGNAL 概念圖重建的專屬向量字標，保留厚筆畫、方形輪廓與窄留白。首頁使用圖片替代文字維持可讀的標題，按比例縮放。
- `styles.css`：版面、字型、色彩與響應式設計。
- `site.js`：作品篩選、影片按需載入、手機選單與 Email 複製。
- `build.py`：首頁、個人介紹、獎項、經歷及作品頁模板。
- `cover-*.jpg`：既有 YouTube 作品封面。檔名與影片 ID 對應。
- `*.ttf`、`*-LICENSE.txt`：本機字型與 OFL 授權。

修改後重新執行 `python3 build.py`。新增作品時，加入作品資料和對應封面；依顯示順序設定連續的 `number`。作品總數與各分類數量會自動更新。以 `slug` 建立 `/projects/slug/` 靜態網址。

## Netlify

現有網站：https://plutowang.netlify.app/

`netlify.toml` 指定建置指令 `python3 build.py` 和發布目錄 `dist`。推送到已連結的部署分支後，由 Netlify 自動建置。根目錄 `index.html` 是首頁快照；正式發布使用生成的 `dist/index.html`。

## 內容與媒體

影片 ID、Email、獎項和工作經歷沿用舊版。未推測逐案職務、客戶成果或新增獎項。首頁主視覺為〈Daughter K Babbling〉，Lambda Film Showreel 清楚標記為公司 Showreel。封面來源為相應 YouTube 影片，影片著作權歸各權利人。

本站無追蹤程式、無聯絡表單後端。封面和字型由本站提供；使用者點擊播放後才載入 YouTube 隱私增強模式播放器。每件作品保留 YouTube 外連，供嵌入受限時使用。

## 驗證

已檢查 34 個 HTML 頁面、731 個內部引用，保留全部 31 個原影片 ID，另新增 Lalamove（cENHOJclU8E）。瀏覽器測試包含分類計數、重新整理後的分類保留、手機選單、Escape 關閉、作品返回連結，以及 320/390/768/1024/1440/1920 像素寬度。首頁代表影片已實際播放；其餘影片未逐一完整播放。
