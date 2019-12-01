# Amazon Sagemaker を用いた機械学習における CI/CD ハンズオン

## 1.GitHub リポジトリの作成
- リポジトリ名：`sagemaker-cicd`
- ハンズオンコンテンツをアップロード

## 2.Amazon SageMaker ノートブックインスタンスの作成
- 新規にノートブックインスタンスを作成
- ロールARNを確認して保存しておく

## 3.データの準備
- ノートブックインスタンス上へ GitHub リポジトリをクローン
- `data_preparation.ipynb` を実行

## 4.CodeBuild でビルドプロジェクトを作成
### sagemaker-cicd-model-dev の作成
- 送信元
  - ソースプロバイダ:GitHub
  - GitHub アカウントのリポジトリ：`sagemaker-cicd` を指定
- プライマリソースのウェブフックイベント
  - コードの変更がこのレポジトリにプッシュされるたびに再構築する
  - イベントタイプ：`PULL_REQUEST_CREATED`、`PULL_REQUEST_UPDATED`
  - プライマリソースのウェブフックイベント：^refs/heads/model-dev$
- 環境：マネージド型イメージ
  - オペレーティングシステム：`Ubuntu`
  - ランタイム:`Standard`
  - イメージ:`aws/codebuild/standard:2.0`
  - イメージのバージョン:`aws/codebuild/standard:2.0-1.13.0`
  - 環境タイプ:`Linux`
  - サービスロール:新しいサービスロール
  - ロール名:`codebuild-sagemaker-cicd-model-dev-service-role`
- Buildspec
  - `buildspec_train.yml` を指定

### sagemaker-cicd-endpoint-dev の作成
- 送信元
  - ソースプロバイダ:`GitHub`
  - GitHub アカウントのリポジトリ：`sagemaker-cicd` を指定
- プライマリソースのウェブフックイベント
  - コードの変更がこのレポジトリにプッシュされるたびに再構築する
  - イベントタイプ：`PULL_REQUEST_CREATED`、`PULL_REQUEST_UPDATED`
  - プライマリソースのウェブフックイベント：`^refs/heads/endpoint-dev$`
- 環境：マネージド型イメージ
  - オペレーティングシステム：`Ubuntu`
  - ランタイム:`Standard`
  - イメージ:`aws/codebuild/standard:2.0`
  - イメージのバージョン:`aws/codebuild/standard:2.0-1.13.0`
  - 環境タイプ:Linux
  - サービスロール:新しいサービスロール
  - ロール名:`codebuild-sagemaker-cicd-endpoint-dev-service-role`
- Buildspec
  - `buildspec_deploy.yml` を指定
  
## 5.IAMの設定変更
下記の2つのロールに対して、それぞれ2つのポリシーを追加する。
- 対象となるロール
  - `codebuild-sagemaker-cicd-model-dev-service-role`
  - `codebuild-sagemaker-cicd-endpoint-dev-service-role`
- 追加するポリシー
  - `AmazonSageMaker-ExecutionPolicy-XXXXX`
  - `AmazonSageMakerFullAccess`
    
## 6.機械学習における CI/CD の実行
### リポジトリの準備
リモートリポジトリに `endpoint-dev` ブランチを作成する。
```
$ git checkout -b endpoint-dev
$ git push -u origin endpoint-dev
```
### 機械学習モデル開発のCI/CD
ローカルリポジトリに `model-dev` ブランチを作成する。
```
$ git checkout -b model-dev
```
`buildspec_train.yml` を編集し `REPO_NAME` と `ROLE` を変更し、変更内容をコミットする。
```
$ git add test_train.yml
$ git commit -m “mod buildspec_train.yml”
$ git push origin HEAD
```
GitHub 上で `model-dev` ブランチから `endpoint-dev` ブランチへ向けて `Pull Request` を作成する。
SageMaker コンソール上で学習ジョブを検索し、S3 モデルアーティファクトの保存先を確認、プルリクをマージする。
- プロパティ：`training_task`
- 演算子：`Equals`
- 値：`cifar10-keras`

### 推論エンドポイント開発のCI/CD
`endpoint-dev` ブランチへ移動する。
```
$ git checkout  endpoint-dev
$ git branch
$ git status
```
`buildspec_depoy.yml` を編集し `MODEL_DATA` と `ROLE` を変更し、変更内容をコミットする。
```
$ git add buildspec_depoy.yml
$ git commit -m “mod model data path”
$ git push origin HEAD
```
GitHub 上で `endpoint-dev` ブランチから `master` ブランチへ向けて `Pull Request` を作成する。

