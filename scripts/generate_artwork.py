#!/usr/bin/env python3
"""Rebuild the profile's self-contained, script-free SVG illustrations."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
INK = "#25263A"
LAVENDER = "#8A78D6"
BLUE = "#72B9D8"
YELLOW = "#F0C85A"
CORAL = "#E87B68"
WHITE = "#FFFDF8"
MUTED = "#686A83"
LINE = "#D5D7E8"


def text(x, y, value, size=16, color=WHITE, weight=400, mono=False, extra=""):
    font = "'SFMono-Regular',Consolas,'Liberation Mono',monospace" if mono else "Arial,Helvetica,sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def rect(x, y, w, h, fill, stroke="none", radius=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'


def line(x1, y1, x2, y2, color=LINE, extra=""):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" fill="none" {extra}/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" fill="none" {extra}/>'


def wrap(name, title, desc, height, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#D8D6EA" stroke-width="0.8"/></pattern>
  <linearGradient id="shade"><stop stop-color="#FFF8DB"/><stop offset="0.58" stop-color="#FFFDF8"/><stop offset="1" stop-color="#F0EEFF"/></linearGradient>
  <linearGradient id="trace"><stop stop-color="{BLUE}" stop-opacity="0.2"/><stop offset="1" stop-color="{LAVENDER}"/></linearGradient>
</defs>
<style>
  .signal {{ stroke-dasharray: 7 110; animation: travel 7s linear infinite; }}
  .pulse {{ animation: breathe 5s ease-in-out infinite; }}
  @keyframes travel {{ to {{ stroke-dashoffset: -234; }} }}
  @keyframes breathe {{ 0%,100% {{opacity:.4}} 50% {{opacity:1}} }}
  @media (prefers-reduced-motion: reduce) {{ .signal,.pulse {{ animation: none !important; }} }}
</style>
{body}
</svg>'''
    (ASSETS / name).write_text(svg + "\n", encoding="utf-8")


def hero():
    b = rect(1, 1, 1198, 454, "url(#shade)", LINE, 18)
    b += rect(700, 2, 498, 452, "url(#grid)", radius=18)
    b += text(48, 50, "LF / LUCAS FANG", 16, LAVENDER, 600, True, 'letter-spacing="1.8"')
    b += text(1150, 50, "ENGINEERING ACROSS LAYERS", 12, MUTED, 400, True, 'text-anchor="end" letter-spacing="1.1"')
    b += text(46, 160, "From silicon", 76, INK, 700, extra='letter-spacing="-3.5"')
    b += text(46, 244, "to software.", 76, LAVENDER, 700, extra='letter-spacing="-3.5"')
    b += text(50, 298, "Hardware–software co-design.", 22, INK)
    b += text(50, 332, "GPU compilers. AI systems. Ideas made executable.", 17, MUTED)
    b += line(48, 381, 1152, 381)
    for x, label, color in [(49, "01 / UNDERSTAND", LAVENDER), (423, "02 / BUILD", BLUE), (797, "03 / MEASURE", CORAL)]:
        b += text(x, 421, label, 13, color, 500, True, 'letter-spacing="1.7"')
    # An original circuit illustration, rather than a stock chip icon.
    for y, d in [(148, "M752 148H815V178H875"), (218, "M752 218H875"), (296, "M780 296H832V258H875")]:
        b += f'<path d="{d}" stroke="{LINE}" stroke-width="2" fill="none"/>'
        b += f'<path class="signal" d="{d}" stroke="{BLUE}" stroke-width="2" fill="none"/>'
    for d in ["M1025 178H1083V143H1144", "M1025 218H1144", "M1025 258H1083V298H1144"]:
        b += f'<path d="{d}" stroke="{LINE}" stroke-width="2" fill="none"/>'
        b += f'<path class="signal" d="{d}" stroke="{LAVENDER}" stroke-width="2" fill="none" style="animation-delay:-2s"/>'
    for x in range(892, 1015, 20):
        b += line(x, 124, x, 142, MUTED) + line(x, 294, x, 312, MUTED)
    for y in range(162, 284, 20):
        b += line(858, y, 875, y, MUTED) + line(1025, y, 1042, y, MUTED)
    b += rect(875, 142, 150, 152, "#E7E2FA", LAVENDER, 12)
    b += rect(888, 155, 124, 126, "#FFFDF8", "#C9C2E7", 5)
    for row in range(4):
        for col in range(4):
            b += rect(904 + col * 24, 169 + row * 24, 15, 15, [LAVENDER, BLUE, YELLOW, CORAL][(row + col) % 4], radius=2, extra=f'opacity="{0.55 + ((row + col) % 3) * 0.15}"')
    b += text(951, 116, "THE MACHINE", 11, MUTED, mono=True, extra='text-anchor="middle" letter-spacing="2"')
    b += text(950, 342, "OBSERVE → COMPILE → VERIFY", 11, LAVENDER, mono=True, extra='text-anchor="middle"')
    for x, y in [(752, 148), (752, 218), (780, 296), (1144, 143), (1144, 218), (1144, 298)]:
        b += f'<circle cx="{x}" cy="{y}" r="4" fill="{CORAL if x > 1000 else BLUE}" class="pulse"/>'
    wrap("hero.svg", "Lucas Fang — from silicon to software", "Hardware–software co-design, GPU compilers, and AI systems. An animated circuit connects software and a processor.", 456, b)


def compiler():
    b = rect(1, 1, 1198, 346, "#F0EEFF", "#D9D5EF", 14)
    b += text(40, 39, "01 / GPU COMPILER ENGINEERING", 12, LAVENDER, mono=True, extra='letter-spacing="1.7"')
    b += text(40, 94, "OpenAssembler", 44, INK, 700, extra='letter-spacing="-1.5"')
    b += text(1160, 38, "v0.3.0 / AMPERE sm_80", 12, MUTED, mono=True, extra='text-anchor="end"')
    b += text(41, 125, "A native-first compiler with bounded research paths.", 17, MUTED)
    nodes = [(40, 210, "INPUTS", "PTX / CUDA"), (284, 354, "CUSTOM BACKEND", "Select → allocate → schedule"), (672, 200, "TENSOR OPS", "GEMM / softmax / LN"), (906, 254, "HARDWARE", "NVIDIA SM80")]
    for x, w, label, sub in nodes:
        b += rect(x, 158, w, 73, WHITE, "#D9D5EF", 7)
        b += text(x + 17, 184, label, 11, LAVENDER, mono=True, extra='letter-spacing="1.1"')
        b += text(x + 17, 211, sub, 16, INK)
    for x1, x2 in [(250, 284), (638, 672), (872, 906)]:
        b += line(x1, 195, x2, 195, "#C4C0DC", 'stroke-width="2"')
        b += line(x1, 195, x2, 195, BLUE, 'stroke-width="2" class="signal"')
        b += f'<path d="M{x2-7} 191l7 4-7 4" fill="none" stroke="{BLUE}"/>'
    b += line(40, 247, 1160, 247)
    metrics = [
        (40, "0.3.0", "Current release", "Native-first compiler + research", LAVENDER),
        (440, "4 workers", "Default native builds", "Bounded at eight · deterministic output", CORAL),
        (840, "1–10%", "Experimental schedule deltas", "Five tested shapes · vs. prior OA", "#4D9DBD"),
    ]
    for x, value, label, sub, color in metrics:
        b += text(x, 287, value, 34, color, 700, extra='letter-spacing="-1.2"')
        b += text(x, 317, label, 14, INK)
        b += text(x, 336, sub, 11, MUTED)
    wrap("openassembler.svg", "OpenAssembler v0.3.0 — GPU compiler engineering", "OpenAssembler v0.3.0 is a native-first NVIDIA SM80 compiler and research platform with bounded parallel native builds, tensor-kernel experiments, cooperative FP32 reductions, and explicit application workflows. Experimental schedule improvements are shape-specific and do not establish universal speedups.", 348, b)


def grand_tool():
    bg = "#FFF8DB"
    dark = INK
    muted = "#64677E"
    border = "#E4DDBD"
    b = rect(1, 1, 1198, 346, bg, border, 14)
    b += text(40, 39, "02 / AI PRODUCT SYSTEMS", 12, "#6E5DB8", mono=True, extra='letter-spacing="1.7"')
    b += text(40, 94, "Grand Tool", 44, dark, 700, extra='letter-spacing="-1.5"')
    b += text(1160, 38, "PROMPT → DESIGN → DEMO", 12, muted, mono=True, extra='text-anchor="end"')
    b += text(41, 125, "An inspectable workflow from an idea to an implementable interface.", 17, muted)
    for i, (label, sub) in enumerate([("Prompt", "+ context"), ("Blueprint", "structured UI plan"), ("Design", "Pencil MCP"), ("Review", "human checkpoint"), ("Demo", "HTML / React")]):
        x = 40 + i * 232
        fill = "#8978D2" if i == 3 else "#FFFFFF"
        b += rect(x, 163, 192, 82, fill, border if i != 3 else dark, 8)
        b += text(x + 17, 188, f"0{i + 1}", 11, YELLOW if i == 3 else LAVENDER, mono=True)
        b += text(x + 17, 214, label, 22, WHITE if i == 3 else dark, 700)
        b += text(x + 17, 232, sub, 11, WHITE if i == 3 else muted)
        if i < 4:
            b += line(x + 192, 203, x + 231, 203, "#D0C8EA", 'stroke-width="2"')
            b += line(x + 192, 203, x + 231, 203, "#8978D2", 'class="signal" stroke-width="2"')
            b += f'<path d="M{x+223} 199l7 4-7 4" fill="none" stroke="#8978D2"/>'
    b += line(40, 272, 1160, 272, border)
    for x, title, sub in [(40, "MCP-first", "Native design-tool integration"), (440, "Artifact-driven", "State, exports, screenshots & review"), (840, "Local by design", "Python control plane · demo UI")]:
        b += text(x, 306, title, 20, dark, 700)
        b += text(x, 330, sub, 13, muted)
    wrap("grand-tool.svg", "Grand Tool — prompt to design to demo", "A local AI UI design workflow. Prompt and context become a blueprint, then a Pencil MCP design, a review with a human checkpoint, and an HTML or React demo. The diagram is conceptual, not a product screenshot.", 348, b)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    hero()
    compiler()
    grand_tool()
    print("Generated hero.svg, openassembler.svg, grand-tool.svg")
