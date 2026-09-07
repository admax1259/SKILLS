# 收录规范 / Contributing

## 新技能 / New skill

1. 判断用途与现有技能是否重复；选择唯一、稳定的 kebab-case id。
2. 放入 skills/<id>/SKILL.md，配套资源留在同一目录；保留 LICENSE。
3. 在 sources/<source>.json 登记上游 URL、固定 commit、许可证与修改记录。
4. 在 catalog.json 登记 category、source、upstream_path 和 status，初始为 review-needed。
5. 审阅工具依赖、授权边界、真实使用案例后逐项适配。未经验证不宣称引擎兼容。
6. 就绪后改为 ready，加入所需 bundle；未就绪成员会阻止整个 bundle 发布。
7. 重新生成目录、运行验证、更新中英文 README，通过 PR 交付。

Keep exactly one canonical source in skills/<id>. Metadata goes in catalog.json; provenance goes in sources/. Preserve supporting resources and licenses. Review incoming skills as data, discuss intended behavior, and test before marking ready. A bundle is published only when all its members are ready.

Do not copy source manually into plugins/ or edit generated dist/ output. Native plugin layouts come from the builder.

```sh
python3 scripts/catalog.py
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Distinguish source/schema checks, native installation, and behavioral validation. Document intentional changes against the recorded upstream baseline. Never import private conversations or remove upstream authorship.
