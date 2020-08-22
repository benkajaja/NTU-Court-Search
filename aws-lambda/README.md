# NTU-Court-Search #aws-lambda

使用aws educate的帳戶，創建一個Lambda function，定期去爬球場的資訊，並推播到Telegram Channel

## Development

總計會用到三個AWS服務(Lambda, IAM, DynamoDB)，且已經向TG**申請一個bot和channel**，屆時會使用這隻bot在channel裡面推播訊息

### Lambda
* Create layer: 
因這個function會使用到額外的package，因此需要額外打包成zip上傳，讓程式可以在執行的時候引入該套件
```
$ sudo apt install python3-venv
$ python3 -m venv requests
$ source requests/bin/activate
$ pip3 install requests -t ./python
$ zip -r requestsLayer python ## upload requestLayer.zip
```
* Create function:
填入基本資訊，執行時間(runtime)選擇**python3.8**，執行角色選擇**建立具備基本Lambda許可的新角色**，接下來會進入編輯器的畫面，主程式請參考lambda_function.py，接下來新增三個環境變數(TOKEN, CHANNEL, WEBURL)，分別對應到**TG Bot Token**, **TG Channel name**, **Django Website URL**，layer的部分，選擇上一個步驟上傳的layer即可

### IAM(Identity and Access Management)
* 新增政策:
找到之前Lambda創建的角色，並新增政策**AWSLambdaInvocation-DynamoDB**，如果沒有新增這個政策，則Dynamo無法觸發Lambda function

### DynamoDB
本來用EventBridge就可以輕鬆搞定觸發事件，但因AWS educate沒有開放使用EventBridge，所以只好繞道而行，這裡使用的是DynamoDB TTL來觸發Lambda，當TTL時間到的時候就會刪除該筆資料，進而觸發Lambda。
* 新增資料表:
新增一張資料表後，需在**存留時間屬性**將TTL這個功能打開，接下來到**項目**的標籤頁新增資料，每筆資料都需含有TTL欄位，注意該欄位必須是number屬性，且使用epoch time(好用的epoch time converter👉[傳送門](https://www.epochconverter.com/))，總而言之，就是將TTL設定成你想要觸發Lambda的時間即可
* 設定觸發器:
到**觸發**的標籤頁，建立觸發器，並選用現有的Lambda function

以上三個部分設定大致完成，需注意的是TTL有時間延遲性，目前幾次測試的結果，大概都會比原本設定的時間**晚十分鐘**，另外，雖然都是使用免費服務，但是個人的帳戶到目前為止被扣了2塊多美金，扣款原因還需要查證
