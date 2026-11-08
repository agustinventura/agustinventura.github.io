#!/usr/bin/env python3
"""
Compara el sitio estático compilado localmente con el sitio en producción.
Detecta regresiones en URLs y pérdida anormal de contenido (> threshold).
Compatible con Python 3.9+. No requiere librerías externas.
"""

import argparse
import html
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import Dict, List, Optional, Set, Tuple

class SimpleHTMLMetricsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_ignored_tag = 0
        self.ignored_tags = {"script", "style", "noscript", "svg", "nav", "footer", "header"}
        
        self.title: Optional[str] = None
        self.in_title = False
        self.h1: Optional[str] = None
        self.in_h1 = False
        
        self.text_chunks: List[str] = []
        self.img_count = 0
        self.pre_count = 0
        self.link_count = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        tag_lower = tag.lower()
        if tag_lower in self.ignored_tags:
            self.in_ignored_tag += 1
            return

        if self.in_ignored_tag == 0:
            if tag_lower == "title" and self.title is None:
                self.in_title = True
            elif tag_lower == "h1" and self.h1 is None:
                self.in_h1 = True
            elif tag_lower == "img":
                self.img_count += 1
            elif tag_lower == "pre":
                self.pre_count += 1
            elif tag_lower == "a":
                self.link_count += 1

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower in self.ignored_tags:
            self.in_ignored_tag = max(0, self.in_ignored_tag - 1)
            return

        if self.in_ignored_tag == 0:
            if tag_lower == "title":
                self.in_title = False
            elif tag_lower == "h1":
                self.in_h1 = False

    def handle_data(self, data: str):
        if self.in_ignored_tag > 0:
            return

        if self.in_title:
            self.title = (self.title or "") + data
        elif self.in_h1:
            self.h1 = (self.h1 or "") + data
        else:
            self.text_chunks.append(data)

    def get_metrics(self) -> Dict[str, any]:
        full_text = " ".join("".join(self.text_chunks).split())
        title_str = html.unescape((self.title or "").strip())
        h1_str = html.unescape((self.h1 or "").strip())
        return {
            "title": title_str,
            "h1": h1_str,
            "text_length": len(full_text),
            "word_count": len(full_text.split()),
            "img_count": self.img_count,
            "pre_count": self.pre_count,
            "link_count": self.link_count,
        }

def fetch_url(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; BlogRegressionChecker/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()

def parse_sitemap(sitemap_bytes: bytes, base_domain: str) -> List[str]:
    root = ET.fromstring(sitemap_bytes)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths = []
    for loc in root.findall(".//sm:loc", ns):
        if loc.text:
            url_str = loc.text.strip()
            parsed = urllib.parse.urlparse(url_str)
            path = parsed.path
            if not path.endswith("/"):
                path += "/"
            paths.append(path)
    return sorted(list(set(paths)))

def parse_rss_items(rss_bytes: bytes) -> int:
    try:
        root = ET.fromstring(rss_bytes)
        items = root.findall(".//item")
        return len(items)
    except Exception:
        return 0

def find_local_html_file(public_dir: str, path: str) -> Optional[str]:
    # Las URLs en el sitemap pueden venir percent-encoded (ej: %C3%AD para í)
    clean_path = urllib.parse.unquote(path).strip("/")
    candidate1 = os.path.join(public_dir, clean_path, "index.html")
    if os.path.isfile(candidate1):
        return candidate1
    candidate2 = os.path.join(public_dir, clean_path + ".html")
    if os.path.isfile(candidate2):
        return candidate2
    if clean_path == "" and os.path.isfile(os.path.join(public_dir, "index.html")):
        return os.path.join(public_dir, "index.html")
    # Intentar también sin decodificar por si el filesystem tuviese la ruta escapada
    raw_clean = path.strip("/")
    candidate3 = os.path.join(public_dir, raw_clean, "index.html")
    if os.path.isfile(candidate3):
        return candidate3
    return None

def analyze_html(content: str) -> Dict[str, any]:
    parser = SimpleHTMLMetricsParser()
    parser.feed(content)
    return parser.get_metrics()

def main():
    parser = argparse.ArgumentParser(description="Compara el sitio compilado con producción.")
    parser.add_argument("--new", default="public", help="Directorio con el nuevo build estático")
    parser.add_argument("--prod", default="https://www.agustinventura.dev", help="URL base de producción")
    parser.add_argument("--threshold", type=float, default=0.05, help="Tolerancia de pérdida porcentual (default: 0.05 = 5%)")
    args = parser.parse_args()

    public_dir = os.path.abspath(args.new)
    prod_base = args.prod.rstrip("/")
    threshold = args.threshold

    if not os.path.isdir(public_dir):
        print(f"❌ Error: El directorio {public_dir} no existe.")
        sys.exit(1)

    print(f"==> Iniciando comparación de sitio...")
    print(f"    Build local: {public_dir}")
    print(f"    Producción:  {prod_base}")
    print(f"    Umbral max tolerado de pérdida: {threshold * 100:.1f}%\n")

    errors: List[str] = []
    warnings: List[str] = []
    table_rows: List[str] = []

    # 1. Comprobar archivos clave
    key_files = ["sitemap.xml", "index.xml", "404.html"]
    for kf in key_files:
        if not os.path.exists(os.path.join(public_dir, kf)):
            errors.append(f"Falta archivo clave en build local: {kf}")

    # 2. Obtener sitemap de producción
    sitemap_url = f"{prod_base}/sitemap.xml"
    try:
        sitemap_bytes = fetch_url(sitemap_url)
        prod_paths = parse_sitemap(sitemap_bytes, prod_base)
        print(f"✅ Sitemap de producción obtenido: {len(prod_paths)} URLs encontradas.")
    except Exception as e:
        print(f"❌ Error descargando sitemap de producción ({sitemap_url}): {e}")
        sys.exit(1)

    # 3. Comparar RSS
    try:
        prod_rss_bytes = fetch_url(f"{prod_base}/index.xml")
        prod_rss_count = parse_rss_items(prod_rss_bytes)
        local_rss_file = os.path.join(public_dir, "index.xml")
        local_rss_count = 0
        if os.path.exists(local_rss_file):
            with open(local_rss_file, "rb") as f:
                local_rss_count = parse_rss_items(f.read())
        print(f"ℹ️  RSS: {prod_rss_count} items en prod vs {local_rss_count} items en local.")
        if local_rss_count < prod_rss_count:
            errors.append(f"El RSS tiene menos elementos ({local_rss_count}) que producción ({prod_rss_count})")
    except Exception as e:
        warnings.append(f"No se pudo comparar el RSS: {e}")

    # 4. Comparar URLs y contenido
    checked_count = 0
    for path in prod_paths:
        local_file = find_local_html_file(public_dir, path)
        if not local_file:
            errors.append(f"URL de producción desaparecida en build local: {path}")
            table_rows.append(f"| `{path}` | ❌ FALTANTE | - | - | - |")
            continue

        checked_count += 1
        page_url = f"{prod_base}{path}"
        try:
            prod_html = fetch_url(page_url).decode("utf-8", errors="replace")
        except Exception as e:
            warnings.append(f"No se pudo descargar de prod {page_url}: {e}")
            continue

        try:
            with open(local_file, "r", encoding="utf-8", errors="replace") as f:
                local_html = f.read()
        except Exception as e:
            errors.append(f"Error leyendo archivo local {local_file}: {e}")
            continue

        prod_metrics = analyze_html(prod_html)
        local_metrics = analyze_html(local_html)

        page_issues = []
        is_list_page = path in {"/", "/posts/", "/archives/", "/tags/", "/categories/"} or path.startswith(("/tags/", "/categories/"))

        # Título y H1
        if prod_metrics["title"] != local_metrics["title"]:
            # En páginas de lista, Blowfish puede añadir el nombre de sección 'Posts · ...'
            if is_list_page and (local_metrics["title"].endswith(prod_metrics["title"]) or prod_metrics["title"].endswith(local_metrics["title"])):
                pass
            else:
                page_issues.append(f"Título cambió de '{prod_metrics['title']}' a '{local_metrics['title']}'")
        
        if prod_metrics["h1"] and prod_metrics["h1"] != local_metrics["h1"]:
            page_issues.append(f"H1 cambió de '{prod_metrics['h1']}' a '{local_metrics['h1']}'")

        # Texto (para páginas de contenido individual se exige umbral estricto; para listas se tolera cambio de paginación/resúmenes)
        prod_len = prod_metrics["text_length"]
        local_len = local_metrics["text_length"]
        if prod_len > 0:
            loss_ratio = (prod_len - local_len) / prod_len
            if loss_ratio > threshold and not is_list_page:
                page_issues.append(f"Pérdida de texto de {loss_ratio*100:.1f}% ({prod_len} -> {local_len} chars)")

        # Imágenes y Bloques de código (en artículos individuales)
        if not is_list_page:
            for metric, name in [("img_count", "imágenes"), ("pre_count", "bloques de código")]:
                p_val = prod_metrics[metric]
                l_val = local_metrics[metric]
                if p_val > 0:
                    loss_metric = (p_val - l_val) / p_val
                    if loss_metric > threshold:
                        page_issues.append(f"Pérdida de {name}: {p_val} -> {l_val}")

        if page_issues:
            errors.extend([f"[{path}] {issue}" for issue in page_issues])
            table_rows.append(f"| `{path}` | ⚠️ FALLO | {prod_len} | {local_len} | {'; '.join(page_issues)} |")
        else:
            table_rows.append(f"| `{path}` | ✅ OK | {prod_len} | {local_len} | Idéntico / dentro de tolerancia |")

    # Resumen
    summary_md = [
        "## Resumen de Verificación de Regresión",
        f"- **URLs analizadas**: {checked_count}/{len(prod_paths)}",
        f"- **Estado general**: {'❌ FALLIDO' if errors else '✅ SUPERADO'}",
        "",
        "| URL | Estado | Caracteres Prod | Caracteres Local | Detalle |",
        "|---|---|---|---|---|",
    ] + table_rows[:35] # Limitar filas si son demasiadas

    if len(table_rows) > 35:
        summary_md.append(f"| ... y {len(table_rows) - 35} URLs más | ... | ... | ... | ... |")

    # Escribir a GITHUB_STEP_SUMMARY si existe
    step_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary_path:
        try:
            with open(step_summary_path, "a", encoding="utf-8") as f:
                f.write("\n".join(summary_md) + "\n")
        except Exception as e:
            print(f"Aviso: No se pudo escribir a GITHUB_STEP_SUMMARY: {e}")

    print("\n" + "\n".join(summary_md) + "\n")

    if warnings:
        print("⚠️ Advertencias:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ Se detectaron {len(errors)} posibles regresiones:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("🎉 La verificación de regresión ha finalizado sin errores.")
    sys.exit(0)

if __name__ == "__main__":
    main()
