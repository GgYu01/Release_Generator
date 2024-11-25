from config.settings import settings
from core.manifest_parser import ManifestParser
from core.git_handler import GitHandler
from utils.logger import get_logger
from utils.common import normalize_tag
from rich.console import Console
from rich.traceback import install

def main() -> None:
    install()  # Enable rich traceback
    console = Console()
    logger = get_logger('Main')

    console.log("[bold green]Starting Release Note Generator[/bold green]")

    # 获取 grt 仓库的最新和次新的标签
    grt_repo_config = next((repo for repo in settings.repositories if repo.name == 'grt'), None)
    if grt_repo_config is None:
        console.log("[red]grt repository not found in settings[/red]")
        return

    grt_git_handler = GitHandler(grt_repo_config.path)
    grt_latest_tag, grt_previous_tag = grt_git_handler.get_last_two_tags()
    grt_tag_prefix = grt_repo_config.tag_prefix

    # 去除前缀以获取版本号
    grt_latest_version = normalize_tag(grt_latest_tag, grt_tag_prefix)
    grt_previous_version = normalize_tag(grt_previous_tag, grt_tag_prefix) if grt_previous_tag else None
    grt_latest_version = "2024_1120_01"
    grt_previous_version = "2024_1114_01"

    console.log(f"grt Latest version: {grt_latest_version}")
    logger.info(f"grt Latest version: {grt_latest_version}")
    console.log(f"grt Previous version: {grt_previous_version}")
    logger.info(f"grt Previous version: {grt_previous_version}")

    # 为每个仓库构建期望的标签并检查其存在性
    for repo_config in settings.repositories:
        repo_path = repo_config.path
        tag_prefix = repo_config.tag_prefix

        # 构建期望的标签
        latest_tag = tag_prefix + grt_latest_version
        previous_tag = tag_prefix + grt_previous_version if grt_previous_version else None

        console.log(f"[cyan]Processing repository: {repo_config.name}[/cyan]")
        logger.info(f"Processing repository: {repo_config.name}")

        git_handler = GitHandler(repo_path)

        # 获取仓库中的所有标签
        tags = git_handler.get_all_tags()

        latest_tag_exists = latest_tag in tags
        previous_tag_exists = previous_tag in tags if previous_tag else False

        console.log(f"Expected latest tag: {latest_tag}, Exists: {latest_tag_exists}")
        logger.info(f"Expected latest tag: {latest_tag}, Exists: {latest_tag_exists}")

        if not latest_tag_exists:
            console.log(f"[red]Latest tag {latest_tag} does not exist in {repo_config.name}[/red]")
            logger.warning(f"Latest tag {latest_tag} does not exist in {repo_config.name}")

        if previous_tag and not previous_tag_exists:
            console.log(f"[red]Previous tag {previous_tag} does not exist in {repo_config.name}[/red]")
            logger.warning(f"Previous tag {previous_tag} does not exist in {repo_config.name}")

        # 如果仓库有 manifest，解析并处理子仓库
        if repo_config.manifest:
            manifest_parser = ManifestParser(repo_config)
            projects = manifest_parser.parse()
            console.log(f"Found {len(projects)} projects in manifest of {repo_config.name}")
            logger.info(f"Parsed {len(projects)} projects in manifest for {repo_config.name}")
            for project in projects:
                project_name = project['name']
                project_path = project['absolute_path']
                console.log(f"Processing project: {project_name} at {project_path}")
                logger.info(f"Processing project: {project_name} at {project_path}")

                project_git_handler = GitHandler(project_path)

                # 构建子仓库的期望标签
                project_latest_tag = tag_prefix + grt_latest_version
                project_previous_tag = tag_prefix + grt_previous_version if grt_previous_version else None

                # 检查标签是否存在
                project_tags = project_git_handler.get_all_tags()

                project_latest_tag_exists = project_latest_tag in project_tags
                project_previous_tag_exists = project_previous_tag in project_tags if project_previous_tag else False

                console.log(f"Expected latest tag: {project_latest_tag}, Exists: {project_latest_tag_exists}")
                logger.info(f"Expected latest tag: {project_latest_tag}, Exists: {project_latest_tag_exists}")

                if not project_latest_tag_exists:
                    console.log(f"[red]Latest tag {project_latest_tag} does not exist in {project_path}[/red]")
                    logger.warning(f"Latest tag {project_latest_tag} does not exist in {project_path}")

                if project_previous_tag and not project_previous_tag_exists:
                    console.log(f"[red]Previous tag {project_previous_tag} does not exist in {project_path}[/red]")
                    logger.warning(f"Previous tag {project_previous_tag} does not exist in {project_path}")

        else:
            console.log(f"No manifest found for {repo_config.name}")
            logger.warning(f"No manifest found for {repo_config.name}")

if __name__ == "__main__":
    main()