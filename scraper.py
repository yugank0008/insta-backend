from instaloader import Instaloader, Post
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

def extract_shortcode(url):
    """Extract Instagram post shortcode from URL"""
    parsed = urlparse(url)
    if not parsed.netloc.endswith('instagram.com'):
        raise ValueError("Invalid Instagram URL")
    
    path_parts = [p for p in parsed.path.split('/') if p]
    if len(path_parts) < 2:
        raise ValueError("URL doesn't contain post shortcode")
    
    return path_parts[1]

def get_instagram_video(url):
    """Get video URL using Instaloader"""
    L = Instaloader(
        quiet=True,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    
    try:
        shortcode = extract_shortcode(url)
        logger.info(f"Extracting post with shortcode: {shortcode}")
        
        post = Post.from_shortcode(L.context, shortcode)
        
        if not post.is_video:
            raise ValueError("The post is not a video")
            
        if not post.video_url:
            raise ValueError("Could not extract video URL")
            
        return post.video_url
        
    except Exception as e:
        logger.error(f"Failed to download {url}: {str(e)}")
        raise Exception(f"Could not download video: {str(e)}")