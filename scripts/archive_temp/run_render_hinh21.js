const { renderHtmlToPng } = require('./scripts/render_infographic');

(async () => {
    try {
        await renderHtmlToPng(
            'E:/TestingProject/ảnh file docx/Hinh_2.1_Agile_Scrum_Workflow.html',
            'E:/TestingProject/ảnh file docx/Hinh_2.1_Agile_Scrum_Workflow.png',
            1400,
            960
        );
        console.log("Infographic Hinh_2.1 rendered successfully!");
    } catch (e) {
        console.error("Error rendering infographic:", e);
    }
})();
