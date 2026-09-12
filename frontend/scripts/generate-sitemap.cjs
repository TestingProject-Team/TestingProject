const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.yiyibook.store';
const SITEMAP_PATH = path.join(__dirname, '..', 'public', 'sitemap.xml');

function formatURL(loc, priority, changefreq, lastmod = new Date().toISOString().split('T')[0]) {
  return `  <url>
    <loc>${loc}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
}

async function generateSitemap() {
  console.log('Starting sitemap generation...');
  let categories = [];
  let books = [];
  let connection;

  // Try fetching dynamic IDs if DB is reachable, otherwise gracefully fall back to static
  if (process.env.DB_HOST) {
    try {
      const mysqlConfig = {
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME || 'bjf8ihu44kqfbqwzs1iv'
      };
      connection = await mysql.createConnection(mysqlConfig);
      const [cats] = await connection.query('SELECT id FROM categories');
      categories = cats;
      const [bks] = await connection.query('SELECT id FROM books');
      books = bks;
    } catch (e) {
      console.warn('DB not reachable for sitemap dynamic routes, generating static base sitemap.');
    } finally {
      if (connection) await connection.end();
    }
  }

  const staticPages = [
    { path: '/', priority: '1.0', freq: 'daily' },
    { path: '/search', priority: '0.8', freq: 'daily' },
    { path: '/flash-sale', priority: '0.9', freq: 'daily' },
    { path: '/coupons', priority: '0.8', freq: 'weekly' },
    { path: '/about', priority: '0.8', freq: 'monthly' },
    { path: '/new-books', priority: '0.9', freq: 'daily' },
    { path: '/used-books', priority: '0.8', freq: 'daily' },
    { path: '/promotions', priority: '0.9', freq: 'daily' },
    { path: '/contact', priority: '0.7', freq: 'monthly' },
    { path: '/terms', priority: '0.5', freq: 'monthly' },
    { path: '/privacy', priority: '0.5', freq: 'monthly' },
    { path: '/payment-privacy', priority: '0.5', freq: 'monthly' },
    { path: '/returns', priority: '0.6', freq: 'monthly' },
    { path: '/warranty', priority: '0.6', freq: 'monthly' },
    { path: '/shipping', priority: '0.6', freq: 'monthly' },
    { path: '/faq', priority: '0.7', freq: 'monthly' },
  ];

  let xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;

  // Add static pages
  staticPages.forEach(p => {
    xmlContent += formatURL(`${BASE_URL}${p.path}`, p.priority, p.freq) + '\n';
  });

  // Add categories if available
  categories.forEach(c => {
    xmlContent += formatURL(`${BASE_URL}/category/${c.id}`, '0.8', 'weekly') + '\n';
  });

  // Add books if available
  books.forEach(b => {
    xmlContent += formatURL(`${BASE_URL}/book/${b.id}`, '0.7', 'daily') + '\n';
  });

  xmlContent += '</urlset>\n';

  // Ensure public folder exists
  const publicDir = path.dirname(SITEMAP_PATH);
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }

  // Write file
  fs.writeFileSync(SITEMAP_PATH, xmlContent, 'utf8');
  console.log(`Sitemap successfully written to: ${SITEMAP_PATH}`);
}

generateSitemap();
