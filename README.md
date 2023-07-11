# 学長が転んだ
## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
キャラクターを操作し障害物や学長の目を避けながら馬に乗ることを目指すゲーム

## ゲームの実装
### 共通基本機能
* 背景画像表示
### 担当追加機能
* 操作キャラクタークラス
* 障害物クラス
* 学長クラス
* 遮蔽物クラス <- 担当
* メニュークラス
* 残機クラス
### ToDo
- [ ] 遮蔽物の描画
- [ ] プレイヤーの動きに応じて遮蔽物を移動
- [ ] プレイヤーが遮蔽物の後ろにいるかどうかの判定

### メモ
ToDoの最後のものはCharactorクラスと合わせた時に機能するものであり、マージ前の状態だと、エラーが出てしまうため、マージするまではコメントで消している。
