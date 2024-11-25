def normalize_tag(tag: str, prefix_to_remove: str) -> str:
    if tag.startswith(prefix_to_remove):
        return tag[len(prefix_to_remove):]
    return tag