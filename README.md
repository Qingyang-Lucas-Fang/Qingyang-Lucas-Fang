<p><a id="top"></a></p>
<p align="center">
<img alt="Lucas Fang — hardware–software co-design. From silicon to software." src="./assets/hero.svg" width="100%"/>
</p>
<h1 align="center">Lucas Fang</h1>
<p align="center">
<b>Hardware–software co-design engineer · GPU compilers · AI systems</b>
</p>
<p align="center">
<a href="#selected-builds">Selected builds</a>   /
  <a href="#more-work">More work</a>   /
  <a href="#background">Background</a>   /
  <a href="#activity">Activity</a>   /
  <a href="#connect">Connect</a>
</p>
<hr/>
<p>I build across the stack: from <strong>GPU instruction encoding and compiler backends</strong> to <strong>AI workflows people can actually use</strong>. My work connects hardware behavior, mathematical reasoning, and software systems through measurement and working implementations.</p>
<p>My current focus is <strong>OpenAssembler v0.3.0</strong>: a native NVIDIA SASS/cubin compiler for SM80/A100 with exact shape-aware dispatch, OA-owned model kernels, and measured optimization research.</p>
<table>
<thead>
<tr>
<th style="text-align:left">Close to the hardware</th>
<th style="text-align:left">Across the system</th>
<th style="text-align:left">Built for people</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">PTX / SASS · NVIDIA Ampere</td>
<td style="text-align:left">Python · CUDA C/C++ frontends</td>
<td style="text-align:left">AI workflow orchestration · PyTorch integration</td>
</tr>
<tr>
<td style="text-align:left">Instruction encoding · Scheduling</td>
<td style="text-align:left">Emulation · Numerical verification</td>
<td style="text-align:left">MCP tooling · HTML / React demos</td>
</tr>
<tr>
<td style="text-align:left">Register allocation · GPU kernels</td>
<td style="text-align:left">Distributed learning · MLOps</td>
<td style="text-align:left">Reviewable artifacts · Developer tools</td>
</tr>
</tbody>
</table>
<p><a id="selected-builds"></a></p>
<h2>Selected builds</h2>
<h3>01 / OpenAssembler</h3>
<p><strong>Understanding the machine. Building the compiler.</strong></p>
<p>
<a href="https://github.com/lucialuka/OpenAssembler">
<img alt="OpenAssembler v0.3.0: a native NVIDIA SM80/A100 SASS and cubin compiler with shape-aware native GEMM dispatch, OA-owned model kernels, cooperative FP32 reductions, and measured optimization research. Results are contract-specific and do not establish universal speedups." src="./assets/openassembler.svg" width="100%"/>
</a>
</p>
<p>OpenAssembler combines a PTX-to-SASS compiler backend, instruction encoder/decoder, and GPU emulator for <strong>NVIDIA Ampere (<code>sm_80</code>)</strong>. The current native model route captures configured Python graphs and emits OA-owned forward, backward, MSE, and SGD cubins with full state verification; unsupported operations fail and vendor GPU fallback is disabled.</p>
<p>Shape-aware dispatch now covers <strong>42 exact contracts</strong>, installing <strong>34 tuned native policies</strong> plus eight verified baseline retentions; unknown or stale contracts fall back to the reference. The status snapshot reports <strong>952 checks passed</strong> with two optional Torch modules skipped, while native attention, cached decoding, model-build caching, GEMM, and rowwise measurements remain bounded by their explicit contracts. Matched <code>ptxas</code> and cuBLAS remain faster in the main comparisons, so the profile presents these as measured native paths and research results rather than universal speedup claims.</p>
<p><strong><a href="https://github.com/lucialuka/OpenAssembler">Explore the repository ↗</a></strong>   ·   <a href="https://github.com/lucialuka/OpenAssembler/releases/tag/v0.3.0">v0.3.0 release notes</a>   ·   <a href="https://github.com/lucialuka/OpenAssembler/blob/main/docs/STATUS.md">Architecture and status</a>   ·   <a href="https://github.com/lucialuka/OpenAssembler/blob/main/docs/COMMANDS.md">Command reference</a>   ·   <a href="https://github.com/lucialuka/OpenAssembler/tree/main/docs/research">Research catalogue</a>   ·   <a href="https://github.com/lucialuka/OpenAssembler/tree/main/docs/reverse_eng_results">Reverse-engineering results</a></p>
<details>
<summary><b>Open the engineering deep dive — architecture, evidence, and scope</b></summary>
<h4>Compiler core and tensor-GEMM extension</h4>
<ul>
<li><strong>A custom compiler backend:</strong> instruction selection, dead-code elimination, coalescing, linear-scan register allocation, basic-block scheduling, and optional 4× loop unrolling.</li>
<li><strong>An Ampere SASS encoder/decoder:</strong> instruction encodings, operands, control fields, and scheduling metadata.</li>
<li><strong>A SASS emulator:</strong> including tensor-core numerical behavior checked against recorded A100 results.</li>
<li><strong>Constant division and remainder lowering:</strong> multiply-high sequences with Z3-backed equivalence checks.</li>
<li><strong>A fast matrix-multiplication path:</strong> Strassen / AlphaTensor factorizations verified exactly over the rationals and compiled through the backend.</li>
<li><strong>Multiple entry points:</strong> a small Python kernel subset, PTX, and CUDA C/C++ through <code>nvcc</code>’s PTX frontend, plus an interactive CLI.</li>
<li><strong>Version 0.3.0 native-build path:</strong> bounded parallel compilation, with four workers by default and a cap of eight, while source order, cubin/SASS publication, and manifests remain deterministic.</li>
<li><strong>Shape-aware native dispatch:</strong> 42 exact GEMM contracts install 34 tuned policies and eight verified baseline retentions; unknown or stale contracts keep the reference path.</li>
<li><strong>Tensor-kernel research:</strong> full-tile FP16/BF16 GEMM with FP32 output, plus cooperative FP32 softmax and population LayerNorm with row/column tails.</li>
<li><strong>OA-owned model execution:</strong> a constrained Python model route emits forward, backward, MSE, and SGD kernels, with exact input contracts, saved native launch plans, and complete state verification.</li>
<li><strong>Operational transports:</strong> native compilation and execution can use local Linux, SSH, or Modal backends with shared compile/run/cnr workflows.</li>
</ul>
<p>The latest status page, updated November 12 and carrying the November 13 production snapshot, reports 952 passing repository checks with two optional Torch modules skipped. It also records nine of ten whole-transformer configurations passing both numerical gates, complete checks for the constrained native model route, and current A100 evidence for exact dispatch, attention, caching, GEMM, and rowwise paths. The tensor and model results remain shape- and contract-specific; same-source <code>ptxas</code> and cuBLAS remain faster in the main comparisons.</p>
<h4>Earlier compiler benchmark snapshot</h4>
<p>The following A100 measurements describe the earlier compiler/probe snapshot documented on 2 November 2026. They are retained as historical context and do not measure the current v0.3.0 native model route, exact dispatch table, or later kernel research.</p>
<table>
<thead>
<tr>
<th style="text-align:left">Measurement</th>
<th style="text-align:left">Result</th>
<th style="text-align:left">Context</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left">Division-by-7 loop</td>
<td style="text-align:left"><strong>1.36× speedup</strong></td>
<td style="text-align:left">0.629 → 0.464 ms vs. <code>ptxas</code>, A100</td>
</tr>
<tr>
<td style="text-align:left">Remainder-by-1000 loop</td>
<td style="text-align:left"><strong>1.19× speedup</strong></td>
<td style="text-align:left">0.373 → 0.312 ms vs. <code>ptxas</code>, A100</td>
</tr>
<tr>
<td style="text-align:left">Compiled probe correctness</td>
<td style="text-align:left"><strong>110 / 110 bit-exact</strong></td>
<td style="text-align:left">Hardware-tested compiler subset, A100</td>
</tr>
<tr>
<td style="text-align:left">Instruction count</td>
<td style="text-align:left"><strong>5.2% fewer</strong></td>
<td style="text-align:left">2,132 vs. 2,249 across 203 supported probes</td>
</tr>
<tr>
<td style="text-align:left">Matrix-multiply factorizations</td>
<td style="text-align:left"><strong>97 / 97 verified</strong></td>
<td style="text-align:left">Exact verification over the rationals</td>
</tr>
</tbody>
</table>
<p>These are <strong>project-reported results for specific workloads</strong>, documented in the repository's benchmark notes. The current status page separates native compiler results, library controls, application-front-end results, and experimental research. The tensor and rowwise paths have narrower shape, layout, precision, and launch contracts and should not be read as support for arbitrary models or GPUs.</p>
<p><strong>Current scope:</strong> the SASS encoder and latency model target <code>sm_80</code> on validated A100 paths. Native GEMM requires full tiles, contiguous K, FP32 accumulation/output, and exact contract selection. Cooperative rowwise operators are bounded FP32 paths without saved statistics, backward support, arbitrary layouts, or affine parameters. The native model route requires configured CPU graph factories and exact input shapes. The compatible ELF packaging still uses a <code>ptxas</code>-generated donor container.</p>
<details>
<summary>See the actual CLI</summary>
<p><img alt="OpenAssembler CLI screenshot from the project" src="https://raw.githubusercontent.com/lucialuka/OpenAssembler/main/figs/OpenAssembler_CLI.png"/></p>
</details>
</details>
<br/>
<h3>02 / Grand Tool</h3>
<p><strong>From a product idea to a reviewable design and a working demo.</strong></p>
<p>
<a href="https://github.com/lucialuka/AI-Automated-UI-Design-Workflow-From-Prompt-to-Demo">
<img alt="Grand Tool: prompt and context to blueprint, Pencil MCP design, review with a human checkpoint, then an HTML or React demo. A local, artifact-driven AI design workflow." src="./assets/grand-tool.svg" width="100%"/>
</a>
</p>
<p>An <strong>MCP-first local AI design workflow</strong> that connects prompts and context files to a structured blueprint, Pencil design automation, artifact review, and explicit HTML/React demo generation.</p>
<p>The system makes each stage inspectable: tasks keep their own state, design exports, screenshots, review notes, and generated code. A <strong>human review checkpoint</strong> sits between design review and code generation.</p>
<p><strong><a href="https://github.com/lucialuka/AI-Automated-UI-Design-Workflow-From-Prompt-to-Demo">Explore the repository ↗</a></strong>   ·   <a href="https://github.com/lucialuka/AI-Automated-UI-Design-Workflow-From-Prompt-to-Demo/blob/main/USER_GUIDE.md">User guide</a>   ·   <a href="https://github.com/lucialuka/AI-Automated-UI-Design-Workflow-From-Prompt-to-Demo/blob/main/DEVELOPER_GUIDE.md">Architecture</a></p>
<details>
<summary><b>Open the product deep dive — orchestration, artifacts, and outputs</b></summary>
<h4>The workflow</h4>
<table>
<thead>
<tr>
<th style="text-align:left">Stage</th>
<th style="text-align:left">Responsibility</th>
<th style="text-align:left">Inspectable output</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><strong>01 · Blueprint</strong></td>
<td style="text-align:left">Turn a prompt and context into a structured UI plan</td>
<td style="text-align:left">Enhanced prompt + <code>blueprint.md</code></td>
</tr>
<tr>
<td style="text-align:left"><strong>02 · Design</strong></td>
<td style="text-align:left">Use a tool-calling agent and Pencil MCP to construct the design</td>
<td style="text-align:left">Variables, layout, design export, screenshots</td>
</tr>
<tr>
<td style="text-align:left"><strong>03 · Review</strong></td>
<td style="text-align:left">Review artifacts, then wait for a person to approve or request changes</td>
<td style="text-align:left">Review reports + human checkpoint</td>
</tr>
<tr>
<td style="text-align:left"><strong>04 · Demo</strong></td>
<td style="text-align:left">Generate an implementation from the design export</td>
<td style="text-align:left">HTML demo or Vite / React / TypeScript / Tailwind app</td>
</tr>
</tbody>
</table>
<h4>Engineering choices</h4>
<ul>
<li><strong>Explicit orchestration:</strong> a phase-based state machine tracks each task from intake through code generation.</li>
<li><strong>Native design-tool integration:</strong> Pencil MCP exposes editor state, design operations, screenshots, and exports to the agent.</li>
<li><strong>Artifact continuity:</strong> the design export connects generation, review, and implementation.</li>
<li><strong>Task isolation:</strong> each run has its own context, state, screenshots, reviews, and code directory.</li>
<li><strong>A deterministic fallback:</strong> if Pencil MCP is unavailable, blueprint-derived design artifacts keep the demo path usable.</li>
<li><strong>A local product interface:</strong> a Python server provides task APIs and a browser UI for running and reviewing the workflow.</li>
</ul>
<p><strong>Stack:</strong> Python · DeepSeek · Pencil MCP · optional OpenRouter visual review · HTML/CSS/JS · React · TypeScript · Vite · Tailwind.</p>
<p><strong>Current scope:</strong> HTML and React are the documented MVP outputs. Native apps, WeChat mini programs, and full production applications are future extension targets. Fallback design artifacts come from the blueprint; generated React code may still require verification.</p>
</details>
<p><a id="more-work"></a></p>
<h2>More work</h2>
<p>Current public work beyond the featured repositories.</p>
<table>
<thead>
<tr>
<th style="text-align:left">Project</th>
<th style="text-align:left">What you’ll find</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:left"><a href="https://lucialuka.github.io/"><strong>Personal website ↗</strong></a></td>
<td style="text-align:left">A public home for selected work, background, and contact information.</td>
</tr>
<tr>
<td style="text-align:left"><a href="https://github.com/lucialuka/lucialuka"><strong>Profile source ↗</strong></a></td>
<td style="text-align:left">The versioned README, generated visual assets, and refresh tooling behind this GitHub profile.</td>
</tr>
</tbody>
</table>
<p align="right"><a href="https://github.com/lucialuka?tab=repositories">Browse all repositories →</a></p>
<p><a id="background"></a></p>
<h2>Background</h2>
<p><strong>Machine Learning Intern · University of California, Santa Cruz · Summer 2026</strong><br/>
Worked on peer-to-peer decentralized learning, convergence analysis, and network simulations for gossip-learning systems.</p>
<p>My foundation is in <strong>computational and applied mathematics</strong>, with interests spanning compiler engineering, distributed ML, and mathematical reasoning. I work in <strong>English and Chinese</strong>.</p>
<details>
<summary><b>Research interests &amp; mathematics highlights</b></summary>
<p><strong>Research interests</strong></p>
<ul>
<li>Knowledge distillation and convergence in asynchronous peer-to-peer gossip networks.</li>
<li>Internal model signals and selective intervention paths.</li>
<li>The relationship between mathematical structure, numerical behavior, and efficient implementation.</li>
</ul>
<p><a href="https://scholar.google.com/citations?user=5snMbcMAAAAJ&amp;hl=en">Find my papers and writing on Google Scholar ↗</a></p>
<p><strong>Mathematics highlights</strong></p>
<ul>
<li>Berkeley Math Tournament — national individual first place.</li>
<li>Stanford Math Tournament — global third place.</li>
<li>International Mathematical Modeling Challenge — finalist.</li>
</ul>
</details>
<p><a id="activity"></a></p>
<h2>Activity, in public</h2>
<p>
<a href="https://github.com/lucialuka?tab=overview">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="./assets/activity-dark.svg?refresh=20261113T195049Z"/>
<source media="(prefers-color-scheme: light)" srcset="./assets/activity-light.svg?refresh=20261113T195049Z"/>
<img alt="Lucas Fang’s public GitHub activity: original public repositories, stars, followers, contribution calendar, and repository language distribution. Values and update time are shown in the panel." src="./assets/activity-light.svg?refresh=20261113T195049Z" width="100%"/>
</picture>
</a>
</p>
<p><sub>Refreshes every six hours with GitHub Actions (scheduled runs can be delayed). Each successful refresh updates the statistics, UTC timestamp, and image cache key. Repository and star totals exclude forks; language shares reflect repository bytes, not proficiency. Contributions follow GitHub’s public visibility settings.</sub></p>
<p><a id="connect"></a></p>
<h2>Let’s build across layers.</h2>
<p>Interested in <strong>GPU compilers, hardware–software co-design, AI infrastructure, or developer tools</strong>? I’d love to compare notes.</p>
<p><strong><a href="mailto:LucasFang2@outlook.com">Email ↗</a></strong>   /   <strong><a href="https://www.linkedin.com/in/qingyang-f-0320563a3/">LinkedIn ↗</a></strong>   /   <strong><a href="https://scholar.google.com/citations?user=5snMbcMAAAAJ&amp;hl=en">Google Scholar ↗</a></strong>   /   <strong><a href="https://github.com/lucialuka">GitHub ↗</a></strong></p>
<p align="right"><a href="#top">Back to the top ↑</a></p>
