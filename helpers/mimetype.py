import mimetypes


def get_mimetype(url: str) -> str:
    """
    Generated a mimeType for google drive files.\n
    Args:
        url: str, link to drive file or folder
    Returns:
        mimeType: str, google file mime type
    """
    mime_type = "application/vnd.google-apps."

    if "docs." in url:  # docs
        if "/spreadsheets/" in url:  # spreadsheet
            type = mime_type + url.split("https://docs.google.com/")[1].split(
                "/d/"
            )[0].rstrip("s")
        else:
            type = mime_type + url.split("https://docs.google.com/")[1].split(
                "/d/"
            )[0]
    elif "drive." in url:
        if "com/drive/" in url:  # folder
            type = mime_type + "folder"
        else:  # file
            type = mime_type + url.split(
                "https://drive.google.com/"
            )[1].split("/d/")[0]
    elif "//script" in url:  # Script
        type = mime_type + "script"
    elif "//photos" in url:
        type = mime_type + "photo"
    elif "com/maps" in url:
        type = mime_type + "map"
    elif "//videos" in url or "//video" in url:
        type = mime_type + "video"
    else:
        type = mime_type + "unknown"
    print(type)
    print(mimetypes.guess_type(url, strict=True))
    return type
