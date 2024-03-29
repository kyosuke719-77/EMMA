## About EMMA

EMMAはHuangらが開発した頻出エピソードマイニング手法の一つです。  
mannila algorithm(MINEPI)を改良して作られたこの手法は以下のような特徴を持ちます。

- 単一系列を対象にするエピソードマイニング手法
- Head Supportと呼ばれるエピソードの数え方をする(Support = 出現数)
- depth first で頻出エピソードを探す
- 探索速度はエピソード長に依存する

本来のEMMAは6つのステップから構成されますが
このEMMAは連鎖パタンマイニング用にチューニングしています。  
(直後に続くエピソードのみを探索するようにしています)  
そのため、若干挙動が異なることをご了承ください。

## How to use EMMA
- 入力データ：csv(データのみを入力)
- 出力データ：txt

パラメータ
- ファイル選択：入力データをGUIで選択
- ファイル名：EMMAの結果を保存するファイルの名前
- misup：何回以上頻出しているパタンを抽出するか指定(2以上の整数)
- チェックボックス：複数系列を1系列とみなしてエピソードマイニングをする場合はチェックを入れる

なお、チェックボックス以外は入力必須項目です。
