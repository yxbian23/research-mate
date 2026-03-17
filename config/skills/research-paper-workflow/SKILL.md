---
name: research-paper-workflow
description: Use this skill when writing research papers. Covers paper structure, LaTeX best practices, figure generation, experiment result formatting, and academic writing guidelines.
---

# Research Paper Workflow

This skill provides comprehensive guidance for writing high-quality machine learning research papers.

## When to Activate

- Writing a new research paper
- Formatting experiment results
- Creating figures and tables
- Preparing camera-ready submissions
- LaTeX troubleshooting

## Paper Structure

### Standard ML Paper Outline

```latex
\begin{document}

\title{Your Paper Title: A Subtitle if Needed}
\author{Author Names}

\maketitle
\begin{abstract}
% 150-250 words summarizing problem, method, results
\end{abstract}

\section{Introduction}
% Problem, motivation, contributions

\section{Related Work}
% Literature review, positioning

\section{Method}
% Technical approach

\section{Experiments}
% Setup, results, analysis

\section{Conclusion}
% Summary, limitations, future work

\end{document}
```

### Section Guidelines

#### Abstract (150-250 words)
1. **Problem**: What problem are you solving? (1-2 sentences)
2. **Gap**: Why is this hard/unsolved? (1 sentence)
3. **Method**: What's your approach? (2-3 sentences)
4. **Results**: Key quantitative results (1-2 sentences)
5. **Impact**: Why does this matter? (1 sentence)

#### Introduction
1. Establish the problem and its importance
2. Describe limitations of existing approaches
3. Present your key insight/contribution
4. Summarize your approach and results
5. List contributions (typically 3 bullet points)

```latex
Our main contributions are:
\begin{itemize}
    \item We propose X, the first method to...
    \item We introduce Y, a novel technique for...
    \item We demonstrate state-of-the-art results on Z benchmark...
\end{itemize}
```

#### Method
- Start with overview/intuition
- Use figures to illustrate architecture
- Define notation clearly
- Present key equations with explanation
- Describe training procedure

#### Experiments
- Dataset descriptions
- Implementation details
- Main results table
- Ablation studies
- Analysis/visualizations

## LaTeX Best Practices

### Document Setup

```latex
\documentclass{article}

% Essential packages
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}  % Better tables
\usepackage{hyperref}
\usepackage{cleveref}  % Smart references
\usepackage{algorithm,algorithmic}
\usepackage{subcaption}  % Subfigures

% Custom commands
\newcommand{\method}{\textsc{MethodName}}
\newcommand{\eg}{\emph{e.g.}}
\newcommand{\ie}{\emph{i.e.}}
\newcommand{\etal}{\emph{et al.}}

% Math operators
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator{\softmax}{softmax}
```

### Tables

```latex
\begin{table}[t]
\centering
\caption{Comparison with state-of-the-art methods on ImageNet.
Best results are \textbf{bold}, second best are \underline{underlined}.}
\label{tab:main_results}
\begin{tabular}{lccc}
\toprule
Method & Top-1 Acc & Top-5 Acc & Params \\
\midrule
ResNet-50 & 76.1 & 92.9 & 25M \\
ViT-B/16 & 77.9 & 93.9 & 86M \\
\midrule
\textbf{Ours} & \textbf{79.2} & \textbf{94.5} & \underline{45M} \\
\bottomrule
\end{tabular}
\end{table}
```

### Figures

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/architecture.pdf}
\caption{Overview of our proposed architecture.
(a) The encoder processes input images.
(b) The decoder generates output.}
\label{fig:architecture}
\end{figure}

% Subfigures
\begin{figure}[t]
\centering
\begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig_a.pdf}
    \caption{Training loss}
\end{subfigure}
\hfill
\begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{fig_b.pdf}
    \caption{Validation accuracy}
\end{subfigure}
\caption{Training curves for our method.}
\label{fig:training}
\end{figure}
```

### Equations

```latex
% Numbered equation
\begin{equation}
\mathcal{L} = \mathbb{E}_{x \sim p_{\text{data}}} \left[
    -\log p_\theta(x)
\right]
\label{eq:loss}
\end{equation}

% Aligned equations
\begin{align}
q_\phi(z|x) &= \mathcal{N}(z; \mu_\phi(x), \sigma_\phi^2(x)) \\
p_\theta(x|z) &= \mathcal{N}(x; \mu_\theta(z), \sigma^2 I)
\end{align}

% Inline math
The loss function $\mathcal{L}$ is minimized using Adam optimizer.
```

### Algorithms

```latex
\begin{algorithm}[t]
\caption{Training procedure}
\label{alg:training}
\begin{algorithmic}[1]
\REQUIRE Dataset $\mathcal{D}$, learning rate $\eta$
\ENSURE Trained model parameters $\theta$
\STATE Initialize parameters $\theta$
\FOR{$t = 1$ to $T$}
    \STATE Sample minibatch $\{x_i\}_{i=1}^B \sim \mathcal{D}$
    \STATE Compute loss $\mathcal{L} = \frac{1}{B}\sum_{i=1}^B \ell(x_i; \theta)$
    \STATE Update $\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$
\ENDFOR
\RETURN $\theta$
\end{algorithmic}
\end{algorithm}
```

## Figure Generation

### Matplotlib Style

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication-quality settings
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.figsize': (3.5, 2.5),  # Single column
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
})

# Create figure
fig, ax = plt.subplots()
ax.plot(x, y, label='Ours', color='#1f77b4', linewidth=1.5)
ax.plot(x, y2, label='Baseline', color='#ff7f0e', linestyle='--')
ax.set_xlabel('Epochs')
ax.set_ylabel('Accuracy (%)')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)

# Save as PDF for LaTeX
plt.savefig('figures/training_curve.pdf')
```

### Comparison Bar Chart

```python
def create_comparison_chart(methods, metrics, values):
    """Create grouped bar chart for method comparison."""
    x = np.arange(len(metrics))
    width = 0.8 / len(methods)

    fig, ax = plt.subplots(figsize=(6, 3))

    for i, (method, vals) in enumerate(zip(methods, values)):
        offset = (i - len(methods)/2 + 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=method)

    ax.set_ylabel('Score')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend(loc='upper right', frameon=False)
    ax.set_ylim(0, 100)

    plt.savefig('figures/comparison.pdf')
```

### Architecture Diagram

```python
# Using matplotlib for simple diagrams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(8, 3))

# Draw boxes
boxes = [
    ('Input', 0.1, 0.4),
    ('Encoder', 0.3, 0.4),
    ('Transformer', 0.5, 0.4),
    ('Decoder', 0.7, 0.4),
    ('Output', 0.9, 0.4),
]

for name, x, y in boxes:
    box = FancyBboxPatch((x-0.08, y-0.15), 0.16, 0.3,
                         boxstyle="round,pad=0.02",
                         facecolor='lightblue',
                         edgecolor='black')
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=9)

# Draw arrows
for i in range(len(boxes)-1):
    ax.annotate('', xy=(boxes[i+1][1]-0.08, boxes[i+1][2]),
                xytext=(boxes[i][1]+0.08, boxes[i][2]),
                arrowprops=dict(arrowstyle='->', color='black'))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.savefig('figures/architecture.pdf')
```

## Results Formatting

### Main Results Table Generator

```python
def generate_latex_table(results: dict, baseline_method: str = None):
    """Generate LaTeX table from results dictionary."""
    methods = list(results.keys())
    metrics = list(results[methods[0]].keys())

    # Find best values for each metric
    best_vals = {}
    second_best = {}
    for metric in metrics:
        vals = [(m, results[m][metric]) for m in methods]
        sorted_vals = sorted(vals, key=lambda x: x[1], reverse=True)
        best_vals[metric] = sorted_vals[0][0]
        second_best[metric] = sorted_vals[1][0] if len(sorted_vals) > 1 else None

    # Generate table
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Main results. Best in \\textbf{bold}, second best \\underline{underlined}.}",
        "\\label{tab:main}",
        "\\begin{tabular}{l" + "c" * len(metrics) + "}",
        "\\toprule",
        "Method & " + " & ".join(metrics) + " \\\\",
        "\\midrule",
    ]

    for method in methods:
        row = [method]
        for metric in metrics:
            val = results[method][metric]
            if method == best_vals[metric]:
                row.append(f"\\textbf{{{val:.1f}}}")
            elif method == second_best[metric]:
                row.append(f"\\underline{{{val:.1f}}}")
            else:
                row.append(f"{val:.1f}")
        lines.append(" & ".join(row) + " \\\\")

    lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ])

    return "\n".join(lines)
```

### Ablation Table

```latex
\begin{table}[t]
\centering
\caption{Ablation study on model components.}
\label{tab:ablation}
\begin{tabular}{ccc|cc}
\toprule
Component A & Component B & Component C & Metric 1 & Metric 2 \\
\midrule
\checkmark & & & 75.2 & 82.1 \\
\checkmark & \checkmark & & 78.5 & 85.3 \\
\checkmark & \checkmark & \checkmark & \textbf{81.2} & \textbf{88.7} \\
\bottomrule
\end{tabular}
\end{table}
```

## Writing Guidelines

### Clear Writing Principles

1. **Active voice**: "We propose X" not "X is proposed"
2. **Be specific**: "improves by 5%" not "significantly improves"
3. **One idea per sentence**: Break complex sentences
4. **Define acronyms**: First use should be spelled out
5. **Consistent terminology**: Pick one term and stick with it

### Common Phrases

```
Problem statements:
- "A fundamental challenge in X is..."
- "Despite recent progress, existing methods struggle to..."
- "However, this approach has limitations..."

Method introduction:
- "To address this, we propose..."
- "Our key insight is that..."
- "The main idea behind our approach is..."

Results:
- "Our method achieves state-of-the-art performance on..."
- "We observe that X outperforms Y by Z%..."
- "These results demonstrate that..."

Ablations:
- "To understand the contribution of each component..."
- "We ablate X and find that..."
- "Removing X leads to a Y% drop in performance..."
```

## Submission Checklist

### Before Submission
- [ ] Abstract within word limit
- [ ] All figures are vector (PDF) or high-res
- [ ] Tables fit within margins
- [ ] No overfull hboxes
- [ ] All references complete
- [ ] Supplementary materials organized
- [ ] Anonymous for blind review (if required)

### Camera Ready
- [ ] Author information added
- [ ] Acknowledgments added
- [ ] Copyright form signed
- [ ] Page limit respected
- [ ] Correct format/template used

## File Organization

```
paper/
├── main.tex           # Main document
├── sections/
│   ├── intro.tex
│   ├── related.tex
│   ├── method.tex
│   ├── experiments.tex
│   └── conclusion.tex
├── figures/
│   ├── architecture.pdf
│   ├── results.pdf
│   └── ...
├── tables/
│   └── results.tex
├── supplementary.tex
├── references.bib
└── Makefile
```
