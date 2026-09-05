const fs = require('fs');
const path = require('path');

const mdPath = path.join(__dirname, '../docs/BVA_EP_TEST_REPORT_VAN_THIEN.md');
const docPath = path.join(__dirname, '../docs/BVA_EP_TEST_REPORT_VAN_THIEN.doc');
const docxPath = path.join(__dirname, '../docs/BVA_EP_TEST_REPORT_VAN_THIEN.docx');

const mdContent = fs.readFileSync(mdPath, 'utf8');

function mdToHtml(md) {
    const lines = md.split(/\r?\n/);
    let html = `<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head>
<meta charset="utf-8">
<title>BÁO CÁO KIỂM THỬ BVA & EP - VĂN THIÊN</title>
<!--[if gte mso 9]>
<xml>
 <w:WordDocument>
  <w:View>Print</w:View>
  <w:Zoom>100</w:Zoom>
  <w:DoNotOptimizeForBrowser/>
 </w:WordDocument>
</xml>
<![endif]-->
<style>
    @page Section1 {
        size: 8.27in 11.69in; /* A4 */
        margin: 1.0in 1.0in 1.0in 1.0in;
        mso-header-margin: 0.5in;
        mso-footer-margin: 0.5in;
        mso-paper-source: 0;
    }
    div.Section1 { page: Section1; }
    body {
        font-family: 'Times New Roman', 'Segoe UI', serif;
        font-size: 11.5pt;
        line-height: 1.5;
        color: #1a202c;
        margin: 0;
        padding: 0;
    }
    h1 {
        font-size: 18pt;
        font-weight: bold;
        color: #1a365d;
        text-align: center;
        text-transform: uppercase;
        margin-top: 15pt;
        margin-bottom: 10pt;
        border-bottom: 2pt solid #2b6cb0;
        padding-bottom: 5pt;
    }
    h2 {
        font-size: 14pt;
        font-weight: bold;
        color: #2c5282;
        margin-top: 18pt;
        margin-bottom: 8pt;
        border-bottom: 1pt solid #cbd5e0;
        padding-bottom: 3pt;
    }
    h3 {
        font-size: 12.5pt;
        font-weight: bold;
        color: #2b6cb0;
        margin-top: 12pt;
        margin-bottom: 6pt;
    }
    p, li {
        font-size: 11.5pt;
        margin-top: 4pt;
        margin-bottom: 4pt;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10pt;
        margin-bottom: 12pt;
        font-size: 9.5pt;
    }
    th {
        background-color: #2b6cb0;
        color: #ffffff;
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
        border: 1pt solid #1a365d;
        padding: 6pt 8pt;
    }
    td {
        border: 1pt solid #cbd5e0;
        padding: 6pt 8pt;
        vertical-align: top;
    }
    tr:nth-child(even) td {
        background-color: #f7fafc;
    }
    code {
        font-family: 'Consolas', monospace;
        background-color: #edf2f7;
        color: #6b46c1;
        padding: 2px 4px;
        font-size: 9.5pt;
    }
    pre {
        font-family: 'Consolas', monospace;
        background-color: #1a202c;
        color: #f7fafc;
        padding: 10pt;
        font-size: 9pt;
        white-space: pre-wrap;
        word-break: break-all;
    }
    .status-pass {
        color: #22543d;
        font-weight: bold;
        background-color: #c6f6d5;
        padding: 2px 6px;
        border: 1px solid #9ae6b4;
    }
</style>
</head>
<body>
<div class="Section1">\n`;

    let inTable = false;
    let inCode = false;
    let isHeader = false;

    lines.forEach(line => {
        if (line.startsWith('```')) {
            if (inCode) {
                html += '</pre>\n';
                inCode = false;
            } else {
                html += '<pre>';
                inCode = true;
            }
            return;
        }

        if (inCode) {
            html += line.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '\n';
            return;
        }

        if (line.startsWith('# ')) {
            html += `<h1>${line.substring(2)}</h1>\n`;
        } else if (line.startsWith('## ')) {
            html += `<h2>${line.substring(3)}</h2>\n`;
        } else if (line.startsWith('### ')) {
            html += `<h3>${line.substring(4)}</h3>\n`;
        } else if (line.startsWith('|')) {
            if (!inTable) {
                html += '<table>\n';
                inTable = true;
                isHeader = true;
            }

            if (/^\s*\|(?:\s*:?-+:?\s*\|)+\s*$/.test(line)) {
                return;
            }

            const cells = line.trim().replace(/^\||\|$/g, '').split('|');
            html += '<tr>';
            cells.forEach(cell => {
                let text = cell.trim();
                text = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
                text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
                text = text.replace(/\bPASS\b/g, '<span class="status-pass">PASS</span>');
                text = text.replace(/<br>/g, '<br/>');

                if (isHeader) {
                    html += `<th>${text}</th>`;
                } else {
                    html += `<td>${text}</td>`;
                }
            });
            html += '</tr>\n';
            isHeader = false;
        } else {
            if (inTable) {
                html += '</table>\n';
                inTable = false;
            }
            if (line.trim() !== '') {
                let pText = line.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
                pText = pText.replace(/`([^`]+)`/g, '<code>$1</code>');
                html += `<p>${pText}</p>\n`;
            }
        }
    });

    if (inTable) html += '</table>\n';
    if (inCode) html += '</pre>\n';

    html += '</div></body></html>';
    return html;
}

const htmlContent = mdToHtml(mdContent);

fs.writeFileSync(docPath, htmlContent, 'utf8');
fs.writeFileSync(docxPath, htmlContent, 'utf8');

console.log(`Word Documents generated successfully at:`);
console.log(`- ${docPath}`);
console.log(`- ${docxPath}`);
