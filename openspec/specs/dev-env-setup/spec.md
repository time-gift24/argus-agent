## ADDED Requirements

### Requirement: make dev 启动开发服务器
开发者 SHALL 能通过 `make dev` 一行命令启动后端开发服务器，无需手动创建 `.env` 或设置环境变量。

#### Scenario: 首次 clone 后直接启动
- **WHEN** 开发者 clone 项目后进入 `backend/` 目录执行 `make dev`
- **THEN** 服务在 `http://localhost:8000` 启动，日志显示 uvicorn 正常运行

#### Scenario: 访问 API 文档
- **WHEN** 开发服务器运行中，访问 `http://localhost:8000/docs`
- **THEN** 返回 200 状态码，显示 Swagger UI

### Requirement: .env.dev 提供开发默认配置
项目 SHALL 包含 `.env.dev` 文件，提交到仓库，包含开发模式所需的全部默认环境变量。

#### Scenario: .env.dev 包含必需变量
- **WHEN** 检查 `.env.dev` 文件内容
- **THEN** 包含 `AES_KEY`（有效的 32 字节 base64）、`JWT_SECRET`、`DEV_MODE=true`

#### Scenario: 环境变量覆盖文件默认值
- **WHEN** 开发者设置环境变量 `JWT_SECRET=my-custom-secret` 后启动服务
- **THEN** 服务使用 `my-custom-secret` 而非 `.env.dev` 中的默认值

### Requirement: config.py 加载 .env.dev
`config.py` SHALL 通过 `env_file` 参数加载 `.env.dev`，环境变量优先级高于文件。

#### Scenario: 无环境变量时从 .env.dev 读取
- **WHEN** 未设置任何环境变量，启动服务
- **THEN** config 从 `.env.dev` 读取 AES_KEY 和 JWT_SECRET，服务正常启动

### Requirement: .env.example 作为模板文档
项目 SHALL 包含 `.env.example` 文件，列出所有环境变量及其说明，不含实际密钥值，供生产部署参考。

#### Scenario: 新人查看 .env.example
- **WHEN** 查看 `.env.example` 文件
- **THEN** 列出所有必需变量（AES_KEY、JWT_SECRET）和可选变量（DEV_MODE、OIDC_* 等），每个变量附带注释说明
