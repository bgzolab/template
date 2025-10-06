# !/bin/bash
# 构建目录
cd /home/bgzo/workspaces/playground/astro-demo/dist/client
# 初始化git
git init
# 添加所有文件
git add .
# 提交更改
git commit -m "Deploy to GitHub Pages"
# 更名分支
git branch -M main
# 设置远程仓库地址(SSH)
git remote add origin git@github.com:bGZo/github-pages.git
# 推送到GitHub Pages分支（通常是gh-pages分支）
git push origin main --force
# 返回上级目录
cd -
echo "Deployed to GitHub Pages successfully."
