const vscode = require('vscode');

// 森蚺典律對照庫 (Senran Lexicon Database)
const LEXICON = [
  // 核心內建
  {
    name: '書',
    pinyin: 'shu',
    kind: vscode.CompletionItemKind.Function,
    py: 'print(*values, sep=" ", end="\\n")',
    desc: '【几案】印出內容於几案之上 (sys.stdout)。',
    example: '書("問天地好在！")'
  },
  {
    name: '問',
    pinyin: 'wen',
    kind: vscode.CompletionItemKind.Function,
    py: 'input(prompt="")',
    desc: '【几案】垂詢使用者，收納應對 (input)。',
    example: '名號 = 問("敢問壯士尊姓大名？")'
  },
  {
    name: '計',
    pinyin: 'ji',
    kind: vscode.CompletionItemKind.Function,
    py: 'len(obj)',
    desc: '【度量】度量事物長度或容量 (len)。',
    example: '門徒數 = 計(門生名錄)'
  },
  {
    name: '疇',
    pinyin: 'chou',
    kind: vscode.CompletionItemKind.Function,
    py: 'range(start, stop, step)',
    desc: '【度量】劃定數之疆界以供巡覽 (range)。',
    example: 'for 數 in 疇(1, 10):'
  },
  {
    name: '總',
    pinyin: 'zong',
    kind: vscode.CompletionItemKind.Function,
    py: 'sum(iterable, start=0)',
    desc: '【度量】薈萃總和 (sum)。',
    example: '全軍總數 = 總([10, 20, 30])'
  },
  {
    name: '引入',
    pinyin: 'yinru',
    kind: vscode.CompletionItemKind.Keyword,
    py: 'importlib.import_module(name)',
    desc: '【萬象】引進外邦庫卷並賦予萬象森羅動態代理。',
    example: '求 = 引入("requests")\n算矩 = 引入("numpy")'
  },
  {
    name: '啟',
    pinyin: 'qi',
    kind: vscode.CompletionItemKind.Function,
    py: 'open(file, mode="r", ...)',
    desc: '【案牘】啟開卷宗檔案，支援 with 語句上下文管理。',
    example: 'with 啟("碑銘.txt", "w") as 牘:\n    牘.書("天下大事，必作於細。")'
  },
  {
    name: '定',
    pinyin: 'ding',
    kind: vscode.CompletionItemKind.Function,
    py: 'assert condition, message',
    desc: '【明斷】若所思非是則鳴警斷言 (assert)。',
    example: '定(1 + 1 == 2, "一加一當為二")'
  },
  {
    name: '若',
    pinyin: 'ruo',
    kind: vscode.CompletionItemKind.Class,
    py: 'if-else conditional sugar',
    desc: '【若則】古風條件判斷流程控制 (若.則.否則)。',
    example: '若(功名 >= 60).則(lambda: 書("及格")).否則(lambda: 書("重修"))'
  },

  // 網絡與傳輸
  {
    name: '得',
    pinyin: 'de',
    kind: vscode.CompletionItemKind.Method,
    py: '.get(url, **kwargs)',
    desc: '【均輸】遣驛使往訪探問，取得回報 (requests.get)。',
    example: '報 = 求.得("https://httpbin.org/get")'
  },
  {
    name: '投',
    pinyin: 'tou',
    kind: vscode.CompletionItemKind.Method,
    py: '.post(url, data=None, json=None)',
    desc: '【均輸】投遞文卷至太虛伺服端 (requests.post)。',
    example: '報 = 求.投("https://httpbin.org/post", json=材料)'
  },
  {
    name: '格',
    pinyin: 'ge',
    kind: vscode.CompletionItemKind.Property,
    py: '.status_code',
    desc: '【驛報】回報狀態格品（如 200 表吉，404 表未尋得）。',
    example: '若(報.格 == 200).則(lambda: 書("吉"))'
  },
  {
    name: '文',
    pinyin: 'wen',
    kind: vscode.CompletionItemKind.Property,
    py: '.text',
    desc: '【驛報】由通訊所攜回之文章正文。',
    example: '書("所得之文：", 報.文)'
  },
  {
    name: '譜',
    pinyin: 'pu',
    kind: vscode.CompletionItemKind.Method,
    py: '.json()',
    desc: '【驛報】剖析為鍵值譜牒 (dict / JSON)。',
    example: '資料 = 報.譜()'
  },

  // 算學與矩陣
  {
    name: '陣',
    pinyin: 'zhen',
    kind: vscode.CompletionItemKind.Method,
    py: 'numpy.array(object)',
    desc: '【勾股】布列多維算數方陣 (array)。',
    example: '方陣 = 算矩.陣([[1, 2], [3, 4]])'
  },
  {
    name: '形',
    pinyin: 'xing',
    kind: vscode.CompletionItemKind.Property,
    py: '.shape',
    desc: '【勾股】方陣或張量之幾何形貌尺寸。',
    example: '書("陣形：", 陣.形)'
  },
  {
    name: '均',
    pinyin: 'jun',
    kind: vscode.CompletionItemKind.Method,
    py: '.mean()',
    desc: '【勾股】推求全陣各項均值。',
    example: '均平數 = 陣.均()'
  },
  {
    name: '皆零',
    pinyin: 'jieling',
    kind: vscode.CompletionItemKind.Method,
    py: '.zeros(shape)',
    desc: '【勾股】創設皆為零之純淨平湖方陣。',
    example: '平湖 = 算矩.皆零((3, 3))'
  },

  // 機器學習與深度學習 (PyTorch)
  {
    name: '量',
    pinyin: 'liang',
    kind: vscode.CompletionItemKind.Method,
    py: 'torch.tensor(data, ...)',
    desc: '【天機】鑄造深度學習多維張量 (Tensor)。',
    example: '權 = 神算.量([2.0], requires_grad=True)'
  },
  {
    name: '反溯',
    pinyin: 'fansu',
    kind: vscode.CompletionItemKind.Method,
    py: '.backward()',
    desc: '【盈不足】反向求勢傳播，計算各節點梯度 (backward)。',
    example: '損.反溯()'
  },
  {
    name: '勢',
    pinyin: 'shi',
    kind: vscode.CompletionItemKind.Property,
    py: '.grad',
    desc: '【盈不足】反溯所得之梯度勢能向量。',
    example: '書("權重之勢：", 權.勢.析值())'
  },
  {
    name: '清勢',
    pinyin: 'qingshi',
    kind: vscode.CompletionItemKind.Method,
    py: '.zero_grad()',
    desc: '【盈不足】清空優化器過往積存之梯度勢能。',
    example: '優化客.清勢()'
  },
  {
    name: '步進',
    pinyin: 'bujin',
    kind: vscode.CompletionItemKind.Method,
    py: '.step()',
    desc: '【盈不足】依循梯度精進更新網絡權重。',
    example: '優化客.步進()'
  },
  {
    name: '析值',
    pinyin: 'xizhi',
    kind: vscode.CompletionItemKind.Method,
    py: '.item()',
    desc: '【天機】剖析單元素張量為純量數值。',
    example: '純量 = 損.析值()'
  },
  {
    name: '矩積',
    pinyin: 'juji',
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
        const linePrefix = document.lineAt(position).text.substr(0, position.character);
        
        return LEXICON.map(item => {
          const comp = new vscode.CompletionItem(item.name, item.kind);
          comp.detail = `[森蚺] ${item.py}`;
          comp.filterText = `${item.name} ${item.pinyin}`;
          
          const md = new vscode.MarkdownString();
          md.appendMarkdown(`### 🐍 森蚺典律：${item.name}\n\n`);
          md.appendMarkdown(`**原語**：\`${item.py}\`\n\n`);
          md.appendMarkdown(`${item.desc}\n\n`);
          md.appendCodeblock(item.example, 'python');
          comp.documentation = md;
          
          return comp;
        });
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

  context.subscriptions.push(completionProvider, hoverProvider);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
