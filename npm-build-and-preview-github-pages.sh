#!/bin/bash
owner=bgzo
repo=github-pages

# 构建并预览 Astro 项目，然后将其部署到 GitHub Pages
npm run build
# 构建目录
cd /home/bgzo/workspaces/playground/astro-demo/dist/client
# 初始化git
git init
# 添加所有文件
git add .
# 提交更改
git commit -m "Deploy to GitHub Pages"
# 更名分支
git branch -M gh-pages
# 设置远程仓库地址(SSH)
git remote add origin git@github.com:${owner}/${repo}.git
# 推送到GitHub Pages分支（通常是gh-pages分支）
git push origin gh-pages --force
# 返回上级目录
cd -
echo "------------------------------------------------------------------"
echo "Deployed to GitHub Pages successfully."
echo "Github Pages URL: https://${owner}.github.io/${repo}/"
echo "Github Repo URL: https://github.com/${owner}/${repo}/tree/gh-pages"
echo "------------------------------------------------------------------"

