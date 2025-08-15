from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import get_instagram_video
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/download', methods=['GET'])
def download():
    url = request.args.get('url')
    
    if not url or 'instagram.com' not in url:
        return jsonify({'error': 'Invalid Instagram URL'}), 400
    
    try:
        logger.info(f"Processing URL: {url}")
        video_url = get_instagram_video(url)
        return jsonify({'url': video_url})
    except Exception as e:
        logger.error(f"Error processing {url}: {str(e)}")
        return jsonify({
            'error': str(e),
            'solution': 'This content cannot be downloaded automatically'
        }), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)