import os
import json
import requests
import base64
import re

# GitHub配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 从环境变量获取GitHub token
REPO_OWNER = "bGZo"
REPO_NAME = "playground"
OUTPUT_FILE = "repo_stats.json"

def get_github_headers():
    """获取GitHub API请求头"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Repo-Stats-Script"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def get_branches(owner, repo):
    """获取仓库的所有分支"""
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    headers = get_github_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"获取分支失败: {response.status_code}")
        return []

    return response.json()

def get_commits_count(owner, repo, branch):
    """获取指定分支的提交数量"""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = get_github_headers()
    params = {"sha": branch, "per_page": 100}
    count = 0
    page = 1

    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            break

        commits = response.json()
        if not commits:
            break

        count += len(commits)
        if len(commits) < 100:  # 最后一页
            break
        page += 1

    return count

def get_latest_commit(owner, repo, branch):
    """获取指定分支的最新提交"""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = get_github_headers()
    params = {"sha": branch, "per_page": 1}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None

    commits = response.json()
    if not commits:
        return None

    commit = commits[0]
    return {
        "sha": commit["sha"],
        "message": commit["commit"]["message"].strip(),
        "author": commit["commit"]["author"]["name"],
        "date": commit["commit"]["author"]["date"]
    }

def get_readme_content(owner, repo, branch="main"):
    """获取README.md文件内容"""
    # 尝试常见的README文件名
    readme_files = ["README.md", "readme.md", "README.MD", "README"]

    headers = get_github_headers()

    for readme_file in readme_files:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{readme_file}"
        params = {"ref": branch}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            content_data = response.json()
            if content_data.get("encoding") == "base64":
                # 解码base64内容
                content = base64.b64decode(content_data["content"]).decode("utf-8")
                return content

    return ""

def extract_title_from_readme(readme_content):
    """从 README 内容中提取 H1 标题"""
    if not readme_content:
        return None

    # 匹配 Markdown H1 标题 (# 标题)
    h1_pattern = r'^#\s+(.+?)(?:\r?\n|$)'
    match = re.search(h1_pattern, readme_content, re.MULTILINE)

    if match:
        title = match.group(1).strip()
        # 清理标题中的特殊字符和多余空格
        title = re.sub(r'[^\w\s\-_\u4e00-\u9fff]', '', title)
        return title

    return None

def extract_name_from_branch(branch_name):
    """从分支名称中提取项目名称"""
    if not branch_name:
        return "Unknown Project"

    # 匹配 xxxx/xx/项目名 格式
    parts = branch_name.split('/')
    if len(parts) >= 3:
        # 取最后一部分作为项目名
        project_name = parts[-1]
        # 替换连字符和下划线为空格，并转换为标题格式
        project_name = project_name.replace('-', ' ').replace('_', ' ')
        # 首字母大写
        project_name = ' '.join(word.capitalize() for word in project_name.split())
        return project_name

    # 如果格式不匹配，直接返回分支名
    return branch_name

def get_repo_stats(owner, repo):
    """获取仓库统计信息"""
    branches = get_branches(owner, repo)
    if not branches:
        print("未找到任何分支")
        return []

    stats = []

    # 限制处理的分支数量，避免过多数据
    max_branches = 50
    processed_count = 0

    for branch in branches:
        if processed_count >= max_branches:
            print(f"已处理 {max_branches} 个分支，跳过剩余分支以避免数据过大")
            break

        branch_name = branch["name"]
        print(f"处理分支: {branch_name} ({processed_count + 1}/{min(len(branches), max_branches)})")

        try:
            # 获取提交数量
            commit_count = get_commits_count(owner, repo, branch_name)

            # 获取最新提交
            latest_commit = get_latest_commit(owner, repo, branch_name)

            if not latest_commit:
                continue

            # 获取README内容（已限制长度）
            readme_content = get_readme_content(owner, repo, branch_name)

            # 提取项目名称
            project_name = extract_title_from_readme(readme_content)
            if not project_name:
                project_name = extract_name_from_branch(branch_name)

            stats.append({
                "branch": branch_name,
                "name": project_name,
                "commit_count": commit_count,
                "latest_commit": latest_commit,
                "readme": readme_content
            })

            processed_count += 1

        except Exception as e:
            print(f"发生异常: {e}，跳过分支 {branch_name}")

    # 按照提交日期倒序排列
    stats.sort(key=lambda x: x["latest_commit"]["date"], reverse=True)

    return stats


if __name__ == "__main__":
    print("开始获取GitHub仓库统计信息...")

    # 检查配置
    if REPO_OWNER == "your-username" or REPO_NAME == "your-repo":
        print("请先配置REPO_OWNER和REPO_NAME变量")
        exit(1)

    if not GITHUB_TOKEN:
        print("警告：未设置GITHUB_TOKEN环境变量，API调用可能受到速率限制")

    repo_stats = get_repo_stats(REPO_OWNER, REPO_NAME)

    if repo_stats:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(repo_stats, f, indent=2, ensure_ascii=False)

        print(f"统计完成，结果已保存到 {OUTPUT_FILE}")
        print(f"共处理了 {len(repo_stats)} 个分支")
    else:
        print("未获取到任何统计信息")
