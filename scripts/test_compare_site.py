import os
import shutil
import tempfile
import unittest

import importlib.util
import os
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "compare_site",
    os.path.join(os.path.dirname(__file__), "compare-site.py"),
)
compare_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare_site)

SimpleHTMLMetricsParser = compare_site.SimpleHTMLMetricsParser
analyze_html = compare_site.analyze_html
find_local_html_file = compare_site.find_local_html_file
parse_rss_items = compare_site.parse_rss_items
parse_sitemap = compare_site.parse_sitemap

class TestCompareSite(unittest.TestCase):
    def test_metrics_parser(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mi Gran Blog</title>
            <script>console.log("ignorar");</script>
            <style>body { color: red; }</style>
        </head>
        <body>
            <header><nav><a href="/">Inicio</a></nav></header>
            <main>
                <h1>Título del Post</h1>
                <p>Este es el texto del post con <a href="/otro">un enlace</a>.</p>
                <pre><code>código aquí</code></pre>
                <img src="/foto.jpg" alt="foto" />
            </main>
            <footer><p>Pie de página</p></footer>
        </body>
        </html>
        """
        metrics = analyze_html(html)
        self.assertEqual(metrics["title"], "Mi Gran Blog")
        self.assertEqual(metrics["h1"], "Título del Post")
        self.assertEqual(metrics["img_count"], 1)
        self.assertEqual(metrics["pre_count"], 1)
        self.assertEqual(metrics["link_count"], 1) # Nav ignorado
        self.assertGreater(metrics["text_length"], 0)

    def test_sitemap_parsing(self):
        sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://www.agustinventura.dev/</loc></url>
            <url><loc>https://www.agustinventura.dev/posts/ejemplo/</loc></url>
        </urlset>
        """
        paths = parse_sitemap(sitemap_xml, "https://www.agustinventura.dev")
        self.assertEqual(paths, ["/", "/posts/ejemplo/"])

    def test_rss_items_count(self):
        rss_xml = b"""<?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0">
            <channel>
                <title>Blog</title>
                <item><title>Post 1</title></item>
                <item><title>Post 2</title></item>
            </channel>
        </rss>
        """
        count = parse_rss_items(rss_xml)
        self.assertEqual(count, 2)

    def test_find_local_html_file(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp_dir, "posts", "post-1"))
            with open(os.path.join(tmp_dir, "posts", "post-1", "index.html"), "w") as f:
                f.write("content")
            with open(os.path.join(tmp_dir, "index.html"), "w") as f:
                f.write("home")

            self.assertIsNotNone(find_local_html_file(tmp_dir, "/"))
            self.assertIsNotNone(find_local_html_file(tmp_dir, "/posts/post-1/"))
            self.assertIsNone(find_local_html_file(tmp_dir, "/posts/inexistente/"))
        finally:
            shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    unittest.main()
