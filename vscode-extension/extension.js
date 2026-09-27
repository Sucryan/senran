const vscode = require('vscode');

// 森蚺典律對照庫 (Senran Lexicon Database)
// 以繁體中文、注音與西邦原語為導向，禁絕漢語拼音
const LEXICON = [
  // 核心內建：几案與度量
  {
    name: '書',
    zh_tw: '印出 列印 輸出 寫 打印 終端 書',
    zhuyin: 'ㄕㄨ',
    en: 'print write stdout',
    kind: vscode.CompletionItemKind.Function,
    py: 'print(*values, sep=" ", end="\\n")',
    desc: '【几案】印出內容於几案之上 (sys.stdout)。',
    example: '書("問天地好在！")'
  },
  {
    name: '問',
    zh_tw: '輸入 詢問 提問 垂詢 問',
    zhuyin: 'ㄨㄣ',
    en: 'input ask prompt',
    kind: vscode.CompletionItemKind.Function,
    py: 'input(prompt="")',
    desc: '【几案】垂詢使用者，收納應對 (input)。',
    example: '名號 = 問("敢問壯士尊姓大名？")'
  },
  {
    name: '計',
    zh_tw: '長度 算長度 數量 大小 容量 計',
    zhuyin: 'ㄐㄧ',
    en: 'len count length size',
    kind: vscode.CompletionItemKind.Function,
    py: 'len(obj)',
    desc: '【度量】度量事物長度或容量 (len)。',
    example: '門徒數 = 計(門生名錄)'
  },
  {
    name: '疇',
    zh_tw: '範圍 區間 循環 輪迴 疆界 疇',
    zhuyin: 'ㄔㄡ',
    en: 'range loop interval',
    kind: vscode.CompletionItemKind.Function,
    py: 'range(start, stop, step)',
    desc: '【度量】劃定數之疆界以供巡覽 (range)。',
    example: 'for 數 in 疇(1, 10):'
  },
  {
    name: '總',
    zh_tw: '總和 加總 合計 累加 總',
    zhuyin: 'ㄗㄨㄥ',
    en: 'sum total add',
    kind: vscode.CompletionItemKind.Function,
    py: 'sum(iterable, start=0)',
    desc: '【度量】薈萃總和 (sum)。',
    example: '全軍總數 = 總([10, 20, 30])'
  },
  {
    name: '枚',
    zh_tw: '列舉 逐項 序號 計數 逐一 走訪 枚',
    zhuyin: 'ㄇㄟ',
    en: 'enumerate iter index count',
    kind: vscode.CompletionItemKind.Function,
    py: 'enumerate(iterable, start=0)',
    desc: '【度量】逐一條列數算，得序號與值 (enumerate)。',
    example: 'for 序號, 物 in 枚(清單):'
  },
  {
    name: '序',
    zh_tw: '排序 排列 等第 順序 序',
    zhuyin: 'ㄒㄩ',
    en: 'sorted sort order',
    kind: vscode.CompletionItemKind.Function,
    py: 'sorted(iterable, reverse=False)',
    desc: '【度量】依理排序 (sorted)。',
    example: '等第 = 序(功名, 逆序=真)'
  },
  {
    name: '反',
    zh_tw: '反轉 倒序 倒轉 逆序 反',
    zhuyin: 'ㄈㄢ',
    en: 'reversed reverse backward',
    kind: vscode.CompletionItemKind.Function,
    py: 'reversed(sequence)',
    desc: '【度量】溯源倒轉 (reversed)。',
    example: '倒序 = 錄(反(隊伍))'
  },
  {
    name: '並',
    zh_tw: '打包 配對 並列 齊行 並',
    zhuyin: 'ㄅㄧㄥ',
    en: 'zip pair together',
    kind: vscode.CompletionItemKind.Function,
    py: 'zip(*iterables)',
    desc: '【度量】兩兩齊行，並轡前馳 (zip)。',
    example: 'for 甲, 乙 in 並(名冊, 功名):'
  },
  {
    name: '審',
    zh_tw: '型態 類型 類別 檢查型態 審',
    zhuyin: 'ㄕㄣ',
    en: 'type typeof class',
    kind: vscode.CompletionItemKind.Function,
    py: 'type(object)',
    desc: '【几案】審視事物根底門類 (type)。',
    example: '門類 = 審(物)'
  },
  {
    name: '係',
    zh_tw: '檢查類別 是否為 是否屬於 係',
    zhuyin: 'ㄒㄧ',
    en: 'isinstance is',
    kind: vscode.CompletionItemKind.Function,
    py: 'isinstance(object, classinfo)',
    desc: '【几案】查核是否屬某門類 (isinstance)。',
    example: '定(係(數, 整), "當為整數")'
  },

  // 核心內建：容器與型別
  {
    name: '錄',
    zh_tw: '清單 列表 陣列 串列 數列 陣 錄',
    zhuyin: 'ㄌㄨ',
    en: 'list array sequence',
    kind: vscode.CompletionItemKind.Class,
    py: 'list([iterable])',
    desc: '【容器】編纂名錄，動態清單 (list)。',
    example: '名錄 = 錄([1, 2, 3])'
  },
  {
    name: '列',
    zh_tw: '隊列 排列 清單 列表 列',
    zhuyin: 'ㄌㄧㄝ',
    en: 'list array queue',
    kind: vscode.CompletionItemKind.Class,
    py: 'list([iterable])',
    desc: '【容器】排配列陣，動態隊伍 (list)。',
    example: '隊伍 = 列(["甲", "乙", "丙"])'
  },
  {
    name: '譜',
    zh_tw: '字典 雜湊 映射 鍵值 對照 譜',
    zhuyin: 'ㄆㄨ',
    en: 'dict dictionary map hash json',
    kind: vscode.CompletionItemKind.Class,
    py: 'dict(**kwargs)',
    desc: '【容器】記敘鍵值譜牒 (dict / JSON)。',
    example: '案底 = 譜({"名": "李白", "歲": 30})'
  },
  {
    name: '集',
    zh_tw: '集合 去重 不重複 集',
    zhuyin: 'ㄐㄧ',
    en: 'set unique collection',
    kind: vscode.CompletionItemKind.Class,
    py: 'set([iterable])',
    desc: '【容器】物以類聚，去重之集 (set)。',
    example: '群生 = 集([1, 2, 2, 3])'
  },
  {
    name: '偶',
    zh_tw: '元組 數對 雙偶 不可變 偶',
    zhuyin: 'ㄡ',
    en: 'tuple pair',
    kind: vscode.CompletionItemKind.Class,
    py: 'tuple([iterable])',
    desc: '【容器】成雙配對，不可變之偶 (tuple)。',
    example: '雙生 = 偶((1, 2))'
  },
  {
    name: '整',
    zh_tw: '整數 整',
    zhuyin: 'ㄓㄥ',
    en: 'int integer',
    kind: vscode.CompletionItemKind.Class,
    py: 'int(x, [base])',
    desc: '【型別】整數之質 (int)。',
    example: '數 = 整("42")'
  },
  {
    name: '浮',
    zh_tw: '浮點數 小數 實數 浮',
    zhuyin: 'ㄈㄨ',
    en: 'float decimal',
    kind: vscode.CompletionItemKind.Class,
    py: 'float(x)',
    desc: '【型別】浮點盈縮之數 (float)。',
    example: '盈虛 = 浮("3.14")'
  },
  {
    name: '文',
    zh_tw: '字串 文字 文章 字 文',
    zhuyin: 'ㄨㄣ',
    en: 'str string text',
    kind: vscode.CompletionItemKind.Class,
    py: 'str(object)',
    desc: '【型別】篇章文字 (str)。',
    example: '章句 = 文(100)'
  },
  {
    name: '字',
    zh_tw: '字元 字符 隻字 字串 字',
    zhuyin: 'ㄗ',
    en: 'str string char',
    kind: vscode.CompletionItemKind.Class,
    py: 'str(object)',
    desc: '【型別】隻字片語 (str)。',
    example: '字符 = 字("道")'
  },

  // 核心常數與語法糖
  {
    name: '真',
    zh_tw: '真 是 對 成立 真是 真',
    zhuyin: 'ㄓㄣ',
    en: 'True bool',
    kind: vscode.CompletionItemKind.Constant,
    py: 'True',
    desc: '【元常】真確不爽 (True)。',
    example: '若(真).則(...)'
  },
  {
    name: '假',
    zh_tw: '假 否 錯 不成立 虛偽 假',
    zhuyin: 'ㄐㄧㄚ',
    en: 'False bool',
    kind: vscode.CompletionItemKind.Constant,
    py: 'False',
    desc: '【元常】偽妄不實 (False)。',
    example: '若(假).否則(...)'
  },
  {
    name: '空',
    zh_tw: '空 無 空值 無值 沒有 空',
    zhuyin: 'ㄎㄨㄥ',
    en: 'None null nil',
    kind: vscode.CompletionItemKind.Constant,
    py: 'None',
    desc: '【元常】太虛虛無 (None)。',
    example: '物 = 空'
  },
  {
    name: '無',
    zh_tw: '無 空 沒有 空值 無',
    zhuyin: 'ㄨ',
    en: 'None null nil',
    kind: vscode.CompletionItemKind.Constant,
    py: 'None',
    desc: '【元常】無中生有 (None)。',
    example: '物 = 無'
  },
  {
    name: '引入',
    zh_tw: '導入 引用 載入 引進 模組 引入',
    zhuyin: 'ㄧㄣ ㄖㄨ',
    en: 'import require load',
    kind: vscode.CompletionItemKind.Keyword,
    py: 'importlib.import_module(name)',
    desc: '【萬象】引進外邦庫卷並賦予萬象森羅動態代理。',
    example: '求 = 引入("requests")\n算矩 = 引入("numpy")'
  },
  {
    name: '啟',
    zh_tw: '開啟 打開 讀檔 寫檔 檔案 開 啟',
    zhuyin: 'ㄑㄧ',
    en: 'open with file',
    kind: vscode.CompletionItemKind.Function,
    py: 'open(file, mode="r", ...)',
    desc: '【案牘】啟開卷宗檔案，支援 with 語句上下文管理。',
    example: 'with 啟("碑銘.txt", "w") as 牘:\n    牘.書("天下大事，必作於細。")'
  },
  {
    name: '定',
    zh_tw: '斷言 驗證 確保 判定 確信 定',
    zhuyin: 'ㄉㄧㄥ',
    en: 'assert check verify',
    kind: vscode.CompletionItemKind.Function,
    py: 'assert condition, message',
    desc: '【明斷】若所思非是則鳴警斷言 (assert)。',
    example: '定(1 + 1 == 2, "一加一當為二")'
  },
  {
    name: '若',
    zh_tw: '如果 條件 假若 若 則 否則',
    zhuyin: 'ㄖㄨㄛ',
    en: 'if condition then else',
    kind: vscode.CompletionItemKind.Class,
    py: 'if-else conditional sugar',
    desc: '【若則】古風條件判斷流程控制 (若.則.否則)。',
    example: '若(功名 >= 60).則(lambda: 書("及格")).否則(lambda: 書("重修"))'
  },

  // 網絡與傳輸
  {
    name: '得',
    zh_tw: '取得 探問 接收 索取 得',
    zhuyin: 'ㄉㄜ',
    en: 'get fetch request',
    kind: vscode.CompletionItemKind.Method,
    py: '.get(url, **kwargs)',
    desc: '【均輸】遣驛使往訪探問，取得回報 (requests.get)。',
    example: '報 = 求.得("https://httpbin.org/get")'
  },
  {
    name: '投',
    zh_tw: '投遞 發送 傳遞 寄送 投',
    zhuyin: 'ㄊㄡ',
    en: 'post send transmit',
    kind: vscode.CompletionItemKind.Method,
    py: '.post(url, data=None, json=None)',
    desc: '【均輸】投遞文卷至太虛伺服端 (requests.post)。',
    example: '報 = 求.投("https://httpbin.org/post", json=材料)'
  },
  {
    name: '格',
    zh_tw: '狀態碼 狀態 狀態格 品格 格',
    zhuyin: 'ㄍㄜ',
    en: 'status_code status code',
    kind: vscode.CompletionItemKind.Property,
    py: '.status_code',
    desc: '【驛報】回報狀態格品（如 200 表吉，404 表未尋得）。',
    example: '若(報.格 == 200).則(lambda: 書("吉"))'
  },
  {
    name: '文',
    zh_tw: '本文 內容 文字 內文 文',
    zhuyin: 'ㄨㄣ',
    en: 'text content body',
    kind: vscode.CompletionItemKind.Property,
    py: '.text',
    desc: '【驛報】由通訊所攜回之文章正文。',
    example: '書("所得之文：", 報.文)'
  },
  {
    name: '譜',
    zh_tw: '解析字典 轉為字典 剖析 譜',
    zhuyin: 'ㄆㄨ',
    en: 'json dict parse',
    kind: vscode.CompletionItemKind.Method,
    py: '.json()',
    desc: '【驛報】剖析為鍵值譜牒 (dict / JSON)。',
    example: '資料 = 報.譜()'
  },

  // 算學與矩陣
  {
    name: '陣',
    zh_tw: '陣列 矩陣 方陣 向量 陣',
    zhuyin: 'ㄓㄣ',
    en: 'array matrix ndarray',
    kind: vscode.CompletionItemKind.Method,
    py: 'numpy.array(object)',
    desc: '【勾股】布列多維算數方陣 (array)。',
    example: '方陣 = 算矩.陣([[1, 2], [3, 4]])'
  },
  {
    name: '形',
    zh_tw: '維度 形狀 尺寸 規格 形',
    zhuyin: 'ㄒㄧㄥ',
    en: 'shape dimension size',
    kind: vscode.CompletionItemKind.Property,
    py: '.shape',
    desc: '【勾股】方陣或張量之幾何形貌尺寸。',
    example: '書("陣形：", 陣.形)'
  },
  {
    name: '均',
    zh_tw: '平均 平均值 均值 均',
    zhuyin: 'ㄐㄩㄣ',
    en: 'mean average avg',
    kind: vscode.CompletionItemKind.Method,
    py: '.mean()',
    desc: '【勾股】推求全陣各項均值。',
    example: '均平數 = 陣.均()'
  },
  {
    name: '皆零',
    zh_tw: '全零 零矩陣 全部為零 皆零',
    zhuyin: 'ㄐㄧㄝ ㄌㄧㄥ',
    en: 'zeros zero empty',
    kind: vscode.CompletionItemKind.Method,
    py: '.zeros(shape)',
    desc: '【勾股】創設皆為零之純淨平湖方陣。',
    example: '平湖 = 算矩.皆零((3, 3))'
  },

  // 機器學習與深度學習 (PyTorch)
  {
    name: '量',
    zh_tw: '張量 深度張量 向量 量',
    zhuyin: 'ㄌㄧㄤ',
    en: 'tensor torch autograd',
    kind: vscode.CompletionItemKind.Method,
    py: 'torch.tensor(data, ...)',
    desc: '【天機】鑄造深度學習多維張量 (Tensor)。',
    example: '權 = 神算.量([2.0], requires_grad=True)'
  },
  {
    name: '反溯',
    zh_tw: '反向傳播 計算梯度 求導 反向 反溯',
    zhuyin: 'ㄈㄢ ㄙㄨ',
    en: 'backward autograd grad',
    kind: vscode.CompletionItemKind.Method,
    py: '.backward()',
    desc: '【盈不足】反向求勢傳播，計算各節點梯度 (backward)。',
    example: '損.反溯()'
  },
  {
    name: '勢',
    zh_tw: '梯度 勢能 導數 斜率 勢',
    zhuyin: 'ㄕ',
    en: 'grad gradient slope',
    kind: vscode.CompletionItemKind.Property,
    py: '.grad',
    desc: '【盈不足】反溯所得之梯度勢能向量。',
    example: '書("權重之勢：", 權.勢.析值())'
  },
  {
    name: '清勢',
    zh_tw: '歸零梯度 清除梯度 歸零 清勢',
    zhuyin: 'ㄑㄧㄥ ㄕ',
    en: 'zero_grad clear zero',
    kind: vscode.CompletionItemKind.Method,
    py: '.zero_grad()',
    desc: '【盈不足】清空優化器過往積存之梯度勢能。',
    example: '優化客.清勢()'
  },
  {
    name: '步進',
    zh_tw: '更新權重 優化一步 迭代 步進',
    zhuyin: 'ㄅㄨ ㄐㄧㄣ',
    en: 'step optimizer update',
    kind: vscode.CompletionItemKind.Method,
    py: '.step()',
    desc: '【盈不足】依循梯度精進更新網絡權重。',
    example: '優化客.步進()'
  },
  {
    name: '析值',
    zh_tw: '取出數值 轉為純量 提取純量 析值',
    zhuyin: 'ㄒㄧ ㄓ',
    en: 'item value scalar',
    kind: vscode.CompletionItemKind.Method,
    py: '.item()',
    desc: '【天機】剖析單元素張量為純量數值。',
    example: '純量 = 損.析值()'
  },
  {
    name: '矩積',
    zh_tw: '矩陣乘法 點積 矩陣相乘 矩積',
    zhuyin: 'ㄐㄩ ㄐㄧ',
    en: 'matmul dot multiply',
    kind: vscode.CompletionItemKind.Method,
    py: 'torch.matmul(a, b)',
    desc: '【天機】計算兩方陣或張量之矩陣乘積。',
    example: '積 = 神算.矩積(甲, 乙)'
  }
];

function activate(context) {
  // 1. 自動補全提供者 (Completion Item Provider)
  const completionProvider = vscode.languages.registerCompletionItemProvider(
    ['python', 'senran'],
    {
      provideCompletionItems(document, position) {
        const docText = document.getText();
        const hasSenran = docText.includes('senran') || docText.includes('引入') || docText.includes('書');

        const items = LEXICON.map(item => {
          const comp = new vscode.CompletionItem(item.name, item.kind);
          comp.detail = `[森蚺] ${item.py}`;
          // 支援 繁體中文、注音、英文字母
          comp.filterText = `${item.name} ${item.zh_tw || ''} ${item.zhuyin || ''} ${item.en || ''}`;
          
          const md = new vscode.MarkdownString();
          md.appendMarkdown(`### 🐍 森蚺典律：${item.name}\n\n`);
          md.appendMarkdown(`**原語**：\`${item.py}\`\n\n`);
          md.appendMarkdown(`${item.desc}\n\n`);
          md.appendCodeblock(item.example, 'python');
          comp.documentation = md;
          
          return comp;
        });

        // 若檔案中有 import senran，啟用「西邦之言自動提雅」：
        // 當使用者習慣性輸入英文（如 print, len, status_code, backward）時，自動推舉文言！
        if (hasSenran) {
          for (let item of LEXICON) {
            if (item.en) {
              const enKeywords = item.en.split(' ');
              for (let enKey of enKeywords) {
                if (!enKey || enKey.length < 2) continue;
                const enComp = new vscode.CompletionItem(`${item.name} (${enKey})`, item.kind);
                enComp.insertText = item.name;
                enComp.detail = `[森蚺提雅] 替代 ${enKey} ➜ ${item.name}`;
                enComp.filterText = enKey;
                enComp.sortText = `00_${enKey}`;
                enComp.documentation = new vscode.MarkdownString(
                  `**西邦俗語**：\`${enKey}\` ➜ **森蚺雅言**：\`${item.name}\`\n\n${item.desc}`
                );
                items.push(enComp);
              }
            }
          }
        }

        return items;
      }
    },
    '.', ' ', ''
  );

  // 2. 懸停古風註釋提供者 (Hover Provider)
  const hoverProvider = vscode.languages.registerHoverProvider(
    ['python', 'senran'],
    {
      provideHover(document, position) {
        const wordRange = document.getWordRangeAtPosition(position, /[\u4e00-\u9fa5_a-zA-Z0-9]+/);
        if (!wordRange) return null;

        const text = document.getText(wordRange);
        const match = LEXICON.find(item => item.name === text);
        
        if (match) {
          const md = new vscode.MarkdownString();
          md.appendMarkdown(`### 📜【森蚺典律】${match.name}\n\n`);
          md.appendMarkdown(`**底層 Python**：\`${match.py}\`\n\n`);
          md.appendMarkdown(`> *${match.desc}*\n\n`);
          md.appendMarkdown(`**示範調用**：\n`);
          md.appendCodeblock(match.example, 'python');
          return new vscode.Hover(md);
        }
        return null;
      }
    }
  );

  // 3. 一鍵化俗為雅（代碼轉錄指令）
  const transcribeCommand = vscode.commands.registerCommand('senran.transcribe', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('【森蚺】未得開啟中之文卷（無作用中的編輯器）。');
      return;
    }

    const document = editor.document;
    const selection = editor.selection;

    const isSelection = !selection.isEmpty;
    const textToConvert = isSelection ? document.getText(selection) : document.getText();
    const transcribed = transcribeCode(textToConvert);

    await editor.edit(editBuilder => {
      if (isSelection) {
        editBuilder.replace(selection, transcribed);
      } else {
        const fullRange = new vscode.Range(
          document.positionAt(0),
          document.positionAt(document.getText().length)
        );
        editBuilder.replace(fullRange, transcribed);
      }
    });

    vscode.window.showInformationMessage('🐍【森蚺】化俗為雅大成！已將代碼轉錄為古雅文言。');
  });

  // 4. 賦體排版（化為 .sr 駢儷賦體文章）
  const formatPianwenCommand = vscode.commands.registerCommand('senran.formatPianwen', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('【森蚺】未得開啟中之文卷。');
      return;
    }

    const document = editor.document;
    const text = document.getText();
    const pianwen = formatToPianwen(text);

    // 於右側開啟新視窗展現 Markdown 駢文
    const newDoc = await vscode.workspace.openTextDocument({
      content: pianwen,
      language: 'markdown'
    });
    await vscode.window.showTextDocument(newDoc, vscode.ViewColumn.Beside);
    vscode.window.showInformationMessage('📜【森蚺】駢儷賦體排印大成！已於側几展卷（Markdown 文卷）。');
  });

  // 5. 一鍵化雅為俗（逆轉為標準西邦代碼）
  const toStandardPyCommand = vscode.commands.registerCommand('senran.toStandardPy', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('【森蚺】未得開啟中之文卷（無作用中的編輯器）。');
      return;
    }

    const document = editor.document;
    const selection = editor.selection;

    const isSelection = !selection.isEmpty;
    const textToConvert = isSelection ? document.getText(selection) : document.getText();
    const standardCode = reverseTranscribeCode(textToConvert);

    await editor.edit(editBuilder => {
      if (isSelection) {
        editBuilder.replace(selection, standardCode);
      } else {
        const fullRange = new vscode.Range(
          document.positionAt(0),
          document.positionAt(document.getText().length)
        );
        editBuilder.replace(fullRange, standardCode);
      }
    });

    vscode.window.showInformationMessage('💻【森蚺】化雅為俗大成！已將文言代碼逆轉為標準西邦代碼。');
  });

  context.subscriptions.push(completionProvider, hoverProvider, transcribeCommand, formatPianwenCommand, toStandardPyCommand);
}

// 轉錄詞律規則
const TRANSCRIPTION_RULES = [
  [/\bprint\s*\(/g, "書("],
  [/\blen\s*\(/g, "計("],
  [/\brange\s*\(/g, "疇("],
  [/\bsum\s*\(/g, "總("],
  [/\bopen\s*\(/g, "啟("],
  [/\binput\s*\(/g, "問("],
  [/\bsorted\s*\(/g, "序("],
  [/\breversed\s*\(/g, "反("],
  [/\btype\s*\(/g, "審("],
  [/\bisinstance\s*\(/g, "係("],

  [/\bTrue\b/g, "真"],
  [/\bFalse\b/g, "假"],
  [/\bNone\b/g, "空"],

  [/\.status_code\b/g, ".格"],
  [/\.text\b/g, ".文"],
  [/\.content\b/g, ".實"],
  [/\.json\s*\(\s*\)/g, ".譜()"],
  [/\.get\s*\(/g, ".得("],
  [/\.post\s*\(/g, ".投("],

  [/\.backward\s*\(\s*\)/g, ".反溯()"],
  [/\.grad\b/g, ".勢"],
  [/\.zero_grad\s*\(\s*\)/g, ".清勢()"],
  [/\.step\s*\(\s*\)/g, ".步進()"],
  [/\.item\s*\(\s*\)/g, ".析值()"],
  [/\.tensor\s*\(/g, ".量("],
  [/\.matmul\s*\(/g, ".矩積("],
  [/\.fit\s*\(/g, ".習("],
  [/\.predict\s*\(/g, ".卜("],
  [/\.score\s*\(/g, ".考分("],

  [/\.array\s*\(/g, ".陣("],
  [/\.shape\b/g, ".形"],
  [/\.mean\s*\(\s*\)/g, ".均()"],
  [/\.zeros\s*\(/g, ".皆零("],
  [/\.ones\s*\(/g, ".皆一("],
  [/\.reshape\s*\(/g, ".塑("],
  [/\.columns\b/g, ".欄"],
  [/\.head\s*\(/g, ".冠("],
  [/\.tail\s*\(/g, ".履("],
  [/\.describe\s*\(\s*\)/g, ".描述()"],

  [/\.read\s*\(\s*\)/g, ".閱()"],
  [/\.write\s*\(/g, ".書("],
  [/\.close\s*\(\s*\)/g, ".閉()"],
  [/\.cursor\s*\(\s*\)/g, ".案台()"],
  [/\.execute\s*\(/g, ".判詞("],
  [/\.fetchall\s*\(\s*\)/g, ".盡攬()"],
  [/\.fetchone\s*\(\s*\)/g, ".攬一()"],
  [/\.commit\s*\(\s*\)/g, ".立契()"],

  [/\.plot\s*\(/g, ".繪("],
  [/\.scatter\s*\(/g, ".布星("],
  [/\.title\s*\(/g, ".題("],
  [/\.xlabel\s*\(/g, ".橫標("],
  [/\.ylabel\s*\(/g, ".縱標("],
  [/\.savefig\s*\(/g, ".存圖("],
  [/\.show\s*\(\s*\)/g, ".展現()"]
];

const IMPORT_RULES = [
  [/^import\s+requests\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('requests')`],
  [/^import\s+requests\b/, () => "求 = 引入('requests')"],
  [/^import\s+numpy\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('numpy')`],
  [/^import\s+numpy\b/, () => "算矩 = 引入('numpy')"],
  [/^import\s+pandas\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('pandas')`],
  [/^import\s+pandas\b/, () => "史冊 = 引入('pandas')"],
  [/^import\s+torch\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('torch')`],
  [/^import\s+torch\b/, () => "神算 = 引入('torch')"],
  [/^import\s+sqlite3\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('sqlite3')`],
  [/^import\s+sqlite3\b/, () => "庫 = 引入('sqlite3')"],
  [/^import\s+json\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('json')`],
  [/^import\s+json\b/, () => "法書 = 引入('json')"],
  [/^import\s+math\s+as\s+(\w+)/, (m, p1) => `${p1} = 引入('math')`],
  [/^import\s+math\b/, () => "算術 = 引入('math')"],
  [/^import\s+(\w+)\s+as\s+(\w+)/, (m, p1, p2) => `${p2} = 引入('${p1}')`],
  [/^import\s+(\w+)\b/, (m, p1) => `${p1} = 引入('${p1}')`]
];

const HEADER = "from senran import 引入, 書, 計, 疇, 總, 序, 錄, 譜, 若, 真, 假, 啟, 定\n\n";

function transcribeCode(code) {
  let lines = code.split("\n");
  let aliasMap = {};
  let newLines = [];

  for (let line of lines) {
    let trimmed = line.trim();
    let matched = false;
    for (let [pattern, repl] of IMPORT_RULES) {
      if (pattern.test(trimmed)) {
        if (/^import\s+requests\b/.test(trimmed) && !/as/.test(trimmed)) aliasMap["requests"] = "求";
        if (/^import\s+torch\b/.test(trimmed) && !/as/.test(trimmed)) aliasMap["torch"] = "神算";
        if (/^import\s+numpy\b/.test(trimmed) && !/as/.test(trimmed)) aliasMap["numpy"] = "算矩";
        if (/^import\s+pandas\b/.test(trimmed) && !/as/.test(trimmed)) aliasMap["pandas"] = "史冊";
        if (/^import\s+sqlite3\b/.test(trimmed) && !/as/.test(trimmed)) aliasMap["sqlite3"] = "庫";

        let indent = line.slice(0, line.length - line.trimStart().length);
        newLines.push(indent + trimmed.replace(pattern, repl));
        matched = true;
        break;
      }
    }
    if (!matched) newLines.push(line);
  }

  let result = newLines.join("\n");

  for (let [origVar, newVar] of Object.entries(aliasMap)) {
    let reg = new RegExp(`\\b${origVar}\\.`, 'g');
    result = result.replace(reg, `${newVar}.`);
  }

  for (let [pattern, repl] of TRANSCRIPTION_RULES) {
    result = result.replace(pattern, repl);
  }

  if (!result.includes("from senran import") && !result.includes("import senran")) {
    result = HEADER + result;
  }

  return result;
}

// 駢文賦體排版轉換器
function formatToPianwen(code) {
  const lines = code.split("\n");
  const pianwenLines = [
    "# 📜【森蚺駢儷憲典 · 賦體卷】",
    "",
    "> 夫運籌於帷幄之中，決勝於方寸之間。",
    ""
  ];

  for (let rawLine of lines) {
    let line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;

    let indent = rawLine.slice(0, rawLine.length - rawLine.trimStart().length);

    // 1. Import
    let m = line.match(/^from\s+senran\s+import\s+(.+)$/);
    if (m) {
      pianwenLines.push(`${indent}先啟森蚺道統，恭請符節「${m[1].replace(/,\s*/g, '、')}」入列几案；`);
      continue;
    }
    m = line.match(/^(\w+)\s*=\s*引入\(['"](.+?)['"]\)$/);
    if (m) {
      pianwenLines.push(`${indent}置百家之珍，引「${m[2]}」入府，銘曰「${m[1]}」；`);
      continue;
    }
    m = line.match(/^import\s+(\w+)(?:\s+as\s+(\w+))?$/);
    if (m) {
      let asname = m[2] || m[1];
      pianwenLines.push(`${indent}夫機巧初動，引外邦「${m[1]}」之庫，役使為「${asname}」；`);
      continue;
    }

    // 2. 網絡請求
    m = line.match(/^(\w+)\s*=\s*(\w+)\.(?:得|get)\((.+)\)$/);
    if (m) {
      pianwenLines.push(`${indent}遣驛使以往訪，運籌「${m[2]}.得(${m[3]})」，定卷為「${m[1]}」；`);
      continue;
    }

    // 3. 印出
    m = line.match(/^(?:書|print)\((.+)\)$/);
    if (m) {
      pianwenLines.push(`${indent}几案展卷，落字有聲，明書其辭：${m[1]}；`);
      continue;
    }

    // 4. 深度學習
    if (line.includes(".反溯()") || line.includes(".backward()")) {
      pianwenLines.push(`${indent}反溯求勢，洞燭幽微，萬千梯度皆通於指掌；`);
      continue;
    }
    if (line.includes(".清勢()") || line.includes(".zero_grad()")) {
      pianwenLines.push(`${indent}蕩滌前勢，澄澈靈台，重開造化新天；`);
      continue;
    }
    if (line.includes(".步進()") || line.includes(".step()")) {
      pianwenLines.push(`${indent}循梯度而步進，隨機變而精微，功德又添一重；`);
      continue;
    }

    // 5. 條件
    m = line.match(/^if\s+(.+):$/);
    if (m) {
      pianwenLines.push(`${indent}若夫考校其理，審「${m[1]}」符契而稱是：`);
      continue;
    }
    if (line === "else:") {
      pianwenLines.push(`${indent}如其不然，背道相左：`);
      continue;
    }

    // 6. 迴圈
    m = line.match(/^for\s+(\w+)\s+in\s+(.+):$/);
    if (m) {
      pianwenLines.push(`${indent}循序週流，以「${m[1]}」度「${m[2]}」，往復而行：`);
      continue;
    }

    // 7. 賦值
    m = line.match(/^(\w+)\s*=\s*(.+)$/);
    if (m) {
      pianwenLines.push(`${indent}設符節曰「${m[1]}」，權衡其理，賦其值曰「${m[2]}」；`);
      continue;
    }

    // 預設表達式
    pianwenLines.push(`${indent}操持法印，施號發令：「${line}」；`);
  }

  pianwenLines.push("");
  pianwenLines.push("---");
  pianwenLines.push("*🪶【賦畢 · 算道咸吉】*");
  return pianwenLines.join("\n");
}

// 逆轉為西邦原碼詞律表 (Reverse Transcription)
const REVERSE_TRANSCRIPTION_RULES = [
  [/\b書\s*\(/g, "print("],
  [/\b計\s*\(/g, "len("],
  [/\b疇\s*\(/g, "range("],
  [/\b總\s*\(/g, "sum("],
  [/\b求和\s*\(/g, "sum("],
  [/\b啟\s*\(/g, "open("],
  [/\b問\s*\(/g, "input("],
  [/\b序\s*\(/g, "sorted("],
  [/\b反\s*\(/g, "reversed("],
  [/\b審\s*\(/g, "type("],
  [/\b係\s*\(/g, "isinstance("],

  [/\b真\b/g, "True"],
  [/\b假\b/g, "False"],
  [/\b空\b/g, "None"],
  [/\b無\b/g, "None"],

  [/\.格\b/g, ".status_code"],
  [/\.態\b/g, ".status_code"],
  [/\.文\b/g, ".text"],
  [/\.實\b/g, ".content"],
  [/\.質\b/g, ".content"],
  [/\.譜\s*\(\s*\)/g, ".json()"],
  [/\.得\s*\(/g, ".get("],
  [/\.取\s*\(/g, ".get("],
  [/\.投\s*\(/g, ".post("],

  [/\.反溯\s*\(\s*\)/g, ".backward()"],
  [/\.溯\s*\(\s*\)/g, ".backward()"],
  [/\.勢\b/g, ".grad"],
  [/\.梯度\b/g, ".grad"],
  [/\.清勢\s*\(\s*\)/g, ".zero_grad()"],
  [/\.滌勢\s*\(\s*\)/g, ".zero_grad()"],
  [/\.步進\s*\(\s*\)/g, ".step()"],
  [/\.析值\s*\(\s*\)/g, ".item()"],
  [/\.量\s*\(/g, ".tensor("],
  [/\.矩積\s*\(/g, ".matmul("],
  [/\.習\s*\(/g, ".fit("],
  [/\.訓\s*\(/g, ".fit("],
  [/\.卜\s*\(/g, ".predict("],
  [/\.考分\s*\(/g, ".score("],

  [/\.陣\s*\(/g, ".array("],
  [/\.形\b/g, ".shape"],
  [/\.均\s*\(\s*\)/g, ".mean()"],
  [/\.皆零\s*\(/g, ".zeros("],
  [/\.皆一\s*\(/g, ".ones("],
  [/\.塑\s*\(/g, ".reshape("],
  [/\.欄\b/g, ".columns"],
  [/\.冠\s*\(/g, ".head("],
  [/\.履\s*\(/g, ".tail("],
  [/\.描述\s*\(\s*\)/g, ".describe()"],

  [/\.閱\s*\(\s*\)/g, ".read()"],
  [/\.書\s*\(/g, ".write("],
  [/\.閉\s*\(\s*\)/g, ".close()"],
  [/\.案台\s*\(\s*\)/g, ".cursor()"],
  [/\.判詞\s*\(/g, ".execute("],
  [/\.盡攬\s*\(\s*\)/g, ".fetchall()"],
  [/\.攬一\s*\(\s*\)/g, ".fetchone()"],
  [/\.立契\s*\(\s*\)/g, ".commit()"],

  [/\.繪\s*\(/g, ".plot("],
  [/\.布星\s*\(/g, ".scatter("],
  [/\.題\s*\(/g, ".title("],
  [/\.橫標\s*\(/g, ".xlabel("],
  [/\.縱標\s*\(/g, ".ylabel("],
  [/\.存圖\s*\(/g, ".savefig("],
  [/\.展現\s*\(\s*\)/g, ".show()"]
];

const REVERSE_IMPORT_RULES = [
  [/^(\w+)\s*=\s*引入\(['"]requests['"]\)/, (m, p1) => (p1 === 'requests' || p1 === '求') ? 'import requests' : `import requests as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]torch['"]\)/, (m, p1) => (p1 === 'torch' || p1 === '神算') ? 'import torch' : `import torch as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]numpy['"]\)/, (m, p1) => (p1 === 'numpy' || p1 === '算矩') ? 'import numpy' : `import numpy as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]pandas['"]\)/, (m, p1) => (p1 === 'pandas' || p1 === '史冊') ? 'import pandas' : `import pandas as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]sqlite3['"]\)/, (m, p1) => (p1 === 'sqlite3' || p1 === '庫') ? 'import sqlite3' : `import sqlite3 as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]json['"]\)/, (m, p1) => (p1 === 'json' || p1 === '法書') ? 'import json' : `import json as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]math['"]\)/, (m, p1) => (p1 === 'math' || p1 === '算術') ? 'import math' : `import math as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"]matplotlib\.pyplot['"]\)/, (m, p1) => (p1 === 'plt' || p1 === '丹青') ? 'import matplotlib.pyplot as plt' : `import matplotlib.pyplot as ${p1}`],
  [/^(\w+)\s*=\s*引入\(['"](.+?)['"]\)/, (m, p1, p2) => (p1 === p2) ? `import ${p2}` : `import ${p2} as ${p1}`]
];

function reverseTranscribeCode(code) {
  let lines = code.split("\n");
  let newLines = [];
  let aliasMap = {};

  for (let line of lines) {
    let trimmed = line.trim();
    if (trimmed.startsWith("from senran import") || trimmed.startsWith("import senran")) {
      continue;
    }

    let matched = false;
    for (let [pattern, repl] of REVERSE_IMPORT_RULES) {
      if (pattern.test(trimmed)) {
        if (/^求\s*=/.test(trimmed)) aliasMap["求"] = "requests";
        if (/^神算\s*=/.test(trimmed)) aliasMap["神算"] = "torch";
        if (/^算矩\s*=/.test(trimmed)) aliasMap["算矩"] = "numpy";
        if (/^史冊\s*=/.test(trimmed)) aliasMap["史冊"] = "pandas";
        if (/^庫\s*=/.test(trimmed)) aliasMap["庫"] = "sqlite3";
        if (/^丹青\s*=/.test(trimmed)) aliasMap["丹青"] = "plt";

        let indent = line.slice(0, line.length - line.trimStart().length);
        newLines.push(indent + trimmed.replace(pattern, repl));
        matched = true;
        break;
      }
    }
    if (!matched) newLines.push(line);
  }

  let result = newLines.join("\n");

  for (let [origVar, newVar] of Object.entries(aliasMap)) {
    let reg = new RegExp(`\\b${origVar}\\.`, 'g');
    result = result.replace(reg, `${newVar}.`);
  }

  for (let [pattern, repl] of REVERSE_TRANSCRIPTION_RULES) {
    result = result.replace(pattern, repl);
  }

  return result.replace(/^\n+/, '');
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
