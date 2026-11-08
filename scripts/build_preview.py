#!/usr/bin/env python3
"""Build an optional local browser preview; requires markdown-it-py."""

from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
markdown = (ROOT / "README.md").read_text(encoding="utf-8")
body = MarkdownIt("commonmark", {"html": True}).enable("table").render(markdown)
body = body.replace('src="./assets/', 'src="../assets/').replace('srcset="./assets/', 'srcset="../assets/')
template = r'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <link rel="icon" type="image/svg+xml" href="../assets/hero.svg">
  <title>Lucas Fang · GitHub profile preview</title>
  <style>
    :root { --page:#f4f3fb; --surface:#fffefa; --text:#29283b; --muted:#66677f; --line:#deddec; --link:#6b5db8; --subtle:#f1effa; }
    :root[data-theme="dark"] { --page:#1b1b29; --surface:#242435; --text:#f5f3ff; --muted:#b9b8d0; --line:#3d3c52; --link:#c4b7ff; --subtle:#302f45; }
    :root[data-theme="light"] { color-scheme:light; }
    :root[data-theme="dark"] { color-scheme:dark; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; scroll-padding-top:90px; }
    body { margin:0; background:var(--page); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; font-size:15px; }
    .toolbar { position:sticky; top:0; z-index:10; border-bottom:1px solid var(--line); background:var(--surface); }
    .toolbar-inner { max-width:1020px; margin:auto; padding:17px 24px; display:flex; align-items:center; justify-content:space-between; gap:16px; }
    .brand { color:var(--muted); font:12px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:.5px; }
    .brand strong { color:var(--text); font-weight:600; }
    .controls { display:flex; gap:6px; }
    button { background:transparent; border:1px solid var(--line); border-radius:6px; color:var(--muted); padding:7px 13px; font:inherit; font-size:12px; cursor:pointer; }
    button[aria-pressed="true"] { color:var(--link); border-color:var(--link); background:var(--subtle); }
    button:focus-visible,a:focus-visible,summary:focus-visible { outline:2px solid var(--link); outline-offset:4px; }
    .frame { max-width:1012px; margin:32px auto 72px; border:1px solid var(--line); border-radius:12px; background:var(--surface); overflow:hidden; }
    .filebar { padding:16px 32px; font:12px ui-monospace,SFMono-Regular,Consolas,monospace; color:var(--muted); border-bottom:1px solid var(--line); display:flex; justify-content:space-between; }
    .filebar span:last-child { color:var(--link); }
    .markdown-body { padding:32px 46px 24px; line-height:1.65; overflow-wrap:break-word; }
    .markdown-body > :first-child { margin-top:0; }
    .markdown-body a { color:var(--link); text-decoration:none; }
    .markdown-body a:hover { text-decoration:underline; }
    .markdown-body p { margin:0 0 17px; }
    .markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4 { line-height:1.3; color:var(--text); font-weight:600; }
    .markdown-body h1 { font-size:29px; letter-spacing:-.7px; padding-bottom:14px; border-bottom:1px solid var(--line); margin:28px 0 16px; }
    .markdown-body h2 { font-size:24px; letter-spacing:-.4px; margin:38px 0 21px; padding-bottom:12px; border-bottom:1px solid var(--line); }
    .markdown-body h3 { font-size:20px; margin:27px 0 14px; }
    .markdown-body h4 { font-size:16px; margin:25px 0 12px; }
    .markdown-body hr { border:0; height:1px; background:var(--line); margin:29px 0; }
    .markdown-body img { max-width:100%; height:auto; vertical-align:middle; }
    .markdown-body code { padding:3px 5px; background:var(--subtle); border-radius:4px; font:85% ui-monospace,SFMono-Regular,Consolas,monospace; }
    .markdown-body table { display:block; overflow-x:auto; border-collapse:collapse; width:max-content; max-width:100%; margin:20px 0; font-size:14px; }
    .markdown-body th,.markdown-body td { border:1px solid var(--line); padding:12px 15px; text-align:left; }
    .markdown-body th { background:var(--subtle); font-weight:600; }
    .markdown-body tr:nth-child(2n) { background:var(--subtle); }
    .markdown-body ul { padding-left:24px; }
    .markdown-body li { margin:9px 0; }
    .markdown-body details { margin:15px 0; padding:0; }
    .markdown-body details[open] { padding-bottom:7px; }
    .markdown-body details > summary { color:var(--link); padding:13px 0; cursor:pointer; line-height:1.6; }
    .markdown-body details[open] > summary { border-bottom:1px solid var(--line); margin-bottom:18px; }
    .markdown-body sub { color:var(--muted); line-height:1.7; font-size:11px; vertical-align:baseline; }
    .preview-note { text-align:center; color:var(--muted); margin:0 24px 40px; font-size:12px; }
    @media(max-width:700px) {
      .toolbar-inner { padding:12px 16px; }
      .brand { font-size:10px; }
      .brand .secondary { display:none; }
      .frame { margin:16px 10px 32px; border-radius:8px; }
      .filebar { padding:13px 18px; font-size:10px; }
      .filebar span:last-child { display:none; }
      .markdown-body { padding:20px 18px; font-size:14px; }
      .markdown-body h1 { font-size:24px; }
      .markdown-body h2 { font-size:22px; }
      .markdown-body table { font-size:12px; }
      .markdown-body th,.markdown-body td { padding:9px 10px; min-width:120px; }
    }
    @media(prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } }
  </style>
</head>
<body>
  <header class="toolbar">
    <div class="toolbar-inner">
      <div class="brand"><strong>LF / PROFILE</strong><span class="secondary"> &nbsp; · &nbsp; local GitHub README preview</span></div>
      <div class="controls" role="group" aria-label="Preview color theme">
        <button id="light" type="button" aria-pressed="true">Light</button>
        <button id="dark" type="button" aria-pressed="false">Dark</button>
      </div>
    </div>
  </header>
  <main class="frame">
    <div class="filebar"><span>lucialuka / README.md</span><span>● rendered preview</span></div>
    <article class="markdown-body">__README_BODY__</article>
  </main>
  <p class="preview-note">Local preview · The profile uses GitHub-native interactions. This preview toolbar is not part of the README.</p>
  <script>
    function setTheme(theme) {
      document.documentElement.dataset.theme = theme;
      document.documentElement.style.colorScheme = theme;
      for (const name of ['light','dark']) document.getElementById(name).setAttribute('aria-pressed', String(name === theme));
      for (const source of document.querySelectorAll('picture source')) source.media = source.srcset.includes('activity-' + theme) ? 'all' : 'not all';
    }
    document.getElementById('light').addEventListener('click', () => setTheme('light'));
    document.getElementById('dark').addEventListener('click', () => setTheme('dark'));
    setTheme('light');
  </script>
</body>
</html>
'''
output = ROOT / "preview" / "index.html"
output.parent.mkdir(exist_ok=True)
output.write_text(template.replace("__README_BODY__", body), encoding="utf-8")
print(output)
