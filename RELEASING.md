# 发版流程

在 GitHub 上发布一个 Release，GitHub Actions（`.github/workflows/publish.yml`）就会自动把新版本发布到 PyPI。不需要本地环境，也不需要 token。

## 一次性设置（只做一次）

自动发布用的是 PyPI 的 Trusted Publishing（可信发布），GitHub 里不存任何 token，但需要先在 pypi.org 上授权这个仓库：

pypi.org → 项目 **structocr** → Settings → Publishing → Add a new publisher → GitHub：

| 字段 | 值 |
| --- | --- |
| Owner | `dracula911` |
| Repository name | `structocr-python` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

没做这一步，自动发布会在最后上传时失败。

## 每次发版

1. **改版本号**：新开一个分支，修改 `structocr/version.py`（`__version__ = "1.7.2"`），提 PR 并合并到 `main`。
   - 版本号规则：只改文档或修 bug 加第三位（1.7.1 → 1.7.2），加新方法或新参数加第二位（1.7.2 → 1.8.0），不兼容的改动加第一位。
   - 同一个版本号在 PyPI 上只能发布一次，发过就不能覆盖，哪怕删掉也不行。
2. **发 Release**：GitHub 仓库页面 → Releases → Draft a new release。
   - Tag：填 `v` + 版本号，例如 `v1.7.2`，选择 "Create new tag on publish"，目标分支 `main`。
   - Title：同 tag 即可，描述里写这次改了什么。
   - 点 **Publish release**。
3. **看结果**：仓库 → Actions → "Publish to PyPI"，几分钟内跑完。流程依次是：
   1. 检查 tag 和代码里的版本号是否一致，不一致就停止；
   2. 跑测试；
   3. 打包并发布。
4. **确认上线**：打开 https://pypi.org/project/structocr/，或者看 `https://pypi.org/pypi/structocr/json` 里的版本号。npm 的页面有时要过几分钟才更新。

## 出错怎么办

- **"Release tag … does not match version …"**：tag 和代码版本号不一致。到 Releases 里删掉这个 Release，再到 Tags 里删掉对应的 tag；把版本号改对、合并后，重新发 Release。
- **测试失败**：什么都没有发布。修好代码合并后，删掉 Release 和 tag，重新发。
- **上传失败（403 / "trusted publisher" 相关报错）**：检查上面的一次性设置，仓库名、workflow 文件名、environment是否完全一致。设置好后在 Actions 里点 **Re-run jobs** 即可，不用重新发 Release。
- **版本号已存在**：说明这个版本发过了，只能改一个新的版本号再发。

## 手动发布（备用）

自动发布不可用时，在本地仓库根目录执行：

```bash
git checkout main
git pull
pip install --upgrade build twine
rm -rf dist
python -m build
twine upload dist/*
```

用户名填 `__token__`，密码填 PyPI API token。

发布前确认版本号：`python -c "exec(open('structocr/version.py').read()); print(__version__)"`。本地跑测试：`python -m unittest test_sdk`。
