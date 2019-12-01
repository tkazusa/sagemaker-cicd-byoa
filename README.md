# sagemaker-cicd-byoa

## GitHub リポジトリの作成
- リポジトリ名：sagemaker-cicd
- ハンズオンコンテンツをアップロード

## Amazon SageMaker ノートブックインスタンスの作成
- 新規にノートブックインスタンスを作成
- ロールARNを確認して保存しておく

## データの準備
- ノートブックインスタンス上へ GitHub リポジトリをクローン
- `data_preparation.ipynb` を実行

## CodeBuild でビルドプロジェクトを作成
### sagemaker-cicd-model-dev の作成
- 送信元
  - ソースプロバイダ:GitHub
  - GitHub アカウントのリポジトリ：`sagemaker-cicd` を指定
- プライマリソースのウェブフックイベント
  - コードの変更がこのレポジトリにプッシュされるたびに再構築する
  - イベントタイプ：`PULL_REQUEST_CREATED`、`PULL_REQUEST_UPDATED`
  - プライマリソースのウェブフックイベント：^refs/heads/model-dev$
- 環境：マネージド型イメージ
  - オペレーティングシステム：Ubuntu
  - ランタイム:Standard
  - イメージ:aws/codebuild/standard:2.0
  - イメージのバージョン:aws/codebuild/standard:2.0-1.13.0
  - 環境タイプ:Linux
  - サービスロール:新しいサービスロール
  - ロール名:`codebuild-sagemaker-cicd-model-dev-service-role`
- Buildspec
  - `buildspec_train.yml` を指定

