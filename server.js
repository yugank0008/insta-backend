const express = require('express');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const cors = require('cors');

// Add stealth plugin to avoid detection
puppeteer.use(StealthPlugin());

const app = express();
app.use(cors());

app.get('/api/download', async (req, res) => {
    const { url } = req.query;

    if (!url || !url.includes('instagram.com')) {
        return res.status(400).json({ error: 'Invalid Instagram URL' });
    }

    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--single-process'
            ],
            executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || null
        });

        const page = await browser.newPage();
        
        // Set realistic headers
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        
        // Add random delays to appear human
        await page.setViewport({ width: 1366, height: 768 });
        await page.goto(url, { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });

        // Wait for video element to load
        await page.waitForSelector('video', { timeout: 10000 });
        
        const videoUrl = await page.evaluate(() => {
            const video = document.querySelector('video');
            return video?.src || null;
        });

        if (!videoUrl) throw new Error('Video element not found');

        res.json({ url: videoUrl });

    } catch (error) {
        console.error('Scraping failed:', error);
        res.status(500).json({ 
            error: 'Failed to download video',
            details: error.message 
        });
    } finally {
        if (browser) await browser.close();
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));