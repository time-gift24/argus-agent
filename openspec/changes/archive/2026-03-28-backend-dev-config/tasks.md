## 1. 配置文件

- [x] 1.1 创建 `backend/.env.dev`，包含 AES_KEY（32 字节 base64）、JWT_SECRET、DEV_MODE=true
- [x] 1.2 创建 `backend/.env.example`，列出所有变量及注释说明（不含实际值）

## 2. 代码修改

- [x] 2.1 修改 `config.py` 的 `SettingsConfigDict`，将 `env_file` 从 `.env` 改为 `.env.dev`

## 3. Makefile

- [x] 3.1 在 `backend/Makefile` 新增 `dev` 目标，执行 `uv run uvicorn main:app --reload --port 8000`

## 4. 验证

- [x] 4.1 执行 `make dev` 确认服务正常启动，访问 `/docs` 返回 200
- [x] 4.2 执行 `make test` 确认全部 32 个测试通过
