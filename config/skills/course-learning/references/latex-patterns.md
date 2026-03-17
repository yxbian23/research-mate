# LaTeX Patterns for Academic Homework

学术作业 LaTeX 常用模式和代码片段。

---

## 1. 文档基础结构

### 标准作业模板

```latex
\documentclass[11pt,a4paper]{article}

% ====== 基础包 ======
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{mathtools}       % 扩展 amsmath
\usepackage{enumitem}        % 列表控制
\usepackage{graphicx}        % 图片
\usepackage{hyperref}        % 超链接
\usepackage{algorithm}       % 算法环境
\usepackage{algpseudocode}   % 伪代码

% ====== 定理环境 ======
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}
\newtheorem{problem}{Problem}

\theoremstyle{remark}
\newtheorem*{remark}{Remark}
\newtheorem*{solution}{Solution}

% ====== 常用命令 ======
% 数集
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\C}{\mathbb{C}}

% 概率统计
\newcommand{\E}{\mathbb{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\Prob}{\mathbb{P}}

% 常用算子
\DeclareMathOperator*{\argmax}{argmax}
\DeclareMathOperator*{\argmin}{argmin}
\DeclareMathOperator{\tr}{tr}
\DeclareMathOperator{\diag}{diag}
\DeclareMathOperator{\rank}{rank}
\DeclareMathOperator{\sign}{sign}

% 其他
\newcommand{\norm}[1]{\left\| #1 \right\|}
\newcommand{\abs}[1]{\left| #1 \right|}
\newcommand{\inner}[2]{\langle #1, #2 \rangle}
\newcommand{\set}[1]{\left\{ #1 \right\}}

% ====== 文档信息 ======
\title{[Course Code] Homework [X]}
\author{[Name] \\ [Student ID]}
\date{\today}

\begin{document}
\maketitle

% 内容开始

\end{document}
```

---

## 2. 题目与解答格式

### 问题-解答结构

```latex
\begin{problem}[20 points]
Let $f: \R \to \R$ be a continuous function. Prove that...
\end{problem}

\begin{solution}
We proceed by contradiction. Suppose that...

Therefore, the claim holds. \qed
\end{solution}
```

### 分部分解答

```latex
\begin{problem}
Consider the following:
\begin{enumerate}[label=(\alph*)]
    \item Show that...
    \item Prove that...
    \item Find...
\end{enumerate}
\end{problem}

\begin{solution}
\begin{enumerate}[label=(\alph*)]
    \item We first show that...

    \item For the second part, observe that...

    \item To find the value, we compute...
\end{enumerate}
\end{solution}
```

---

## 3. 数学公式常用模式

### 多行对齐公式

```latex
% 基础对齐
\begin{align}
f(x) &= x^2 + 2x + 1 \\
     &= (x+1)^2
\end{align}

% 不编号版本
\begin{align*}
\E[X+Y] &= \E[X] + \E[Y] \\
        &= \mu_X + \mu_Y
\end{align*}

% 条件对齐
\begin{align*}
|x+y| &\leq |x| + |y| && \text{(triangle inequality)} \\
      &\leq 2\max\{|x|, |y|\} && \text{(by AM-GM)}
\end{align*}
```

### 分段函数

```latex
f(x) =
\begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
```

### 矩阵

```latex
% 普通矩阵
A = \begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix}

% 方括号矩阵
B = \begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}

% 行列式
\det(A) = \begin{vmatrix}
a & b \\
c & d
\end{vmatrix} = ad - bc
```

### 求和与积分

```latex
% 求和
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n

% 连乘
\prod_{i=1}^{n} x_i = x_1 \cdot x_2 \cdots x_n

% 积分
\int_{a}^{b} f(x) \, dx = F(b) - F(a)

% 多重积分
\iint_D f(x,y) \, dA = \int_a^b \int_c^d f(x,y) \, dy \, dx
```

---

## 4. 证明格式

### 直接证明

```latex
\begin{proof}
Let $x \in A$. By definition, $x$ satisfies property $P$.
Since $P$ implies $Q$, we have $x \in B$.
Therefore, $A \subseteq B$.
\end{proof}
```

### 反证法

```latex
\begin{proof}
Suppose, for the sake of contradiction, that $\sqrt{2}$ is rational.
Then $\sqrt{2} = p/q$ for some integers $p, q$ with $\gcd(p,q) = 1$.

Squaring both sides gives $2 = p^2/q^2$, so $p^2 = 2q^2$.
This means $p^2$ is even, hence $p$ is even.
Write $p = 2k$ for some integer $k$.

Substituting: $(2k)^2 = 2q^2$, so $4k^2 = 2q^2$, giving $q^2 = 2k^2$.
Thus $q^2$ is even, so $q$ is even.

But this contradicts $\gcd(p,q) = 1$, since both are even.
Therefore, $\sqrt{2}$ must be irrational.
\end{proof}
```

### 数学归纳法

```latex
\begin{proof}
We proceed by induction on $n$.

\textbf{Base case} ($n=1$): When $n=1$, the left side equals...
and the right side equals... Thus the claim holds.

\textbf{Inductive step}: Assume the claim holds for some $n = k \geq 1$.
We show it holds for $n = k+1$.

By the inductive hypothesis,
\[
\sum_{i=1}^{k} i = \frac{k(k+1)}{2}.
\]
Adding $(k+1)$ to both sides:
\begin{align*}
\sum_{i=1}^{k+1} i &= \frac{k(k+1)}{2} + (k+1) \\
&= \frac{k(k+1) + 2(k+1)}{2} \\
&= \frac{(k+1)(k+2)}{2}.
\end{align*}
This is exactly the formula with $n = k+1$.

By induction, the claim holds for all $n \geq 1$.
\end{proof}
```

---

## 5. 博弈论专用

### 支付矩阵

```latex
% 2x2 博弈矩阵
\begin{center}
\begin{tabular}{c|c|c|}
  & L & R \\ \hline
T & $(3,3)$ & $(0,5)$ \\ \hline
B & $(5,0)$ & $(1,1)$ \\ \hline
\end{tabular}
\end{center}

% 带标签的博弈矩阵
\begin{center}
\begin{tabular}{r|c|c|}
\multicolumn{1}{c}{} & \multicolumn{1}{c}{Player 2: L} & \multicolumn{1}{c}{Player 2: R} \\ \cline{2-3}
Player 1: T & $(a_{11}, b_{11})$ & $(a_{12}, b_{12})$ \\ \cline{2-3}
Player 1: B & $(a_{21}, b_{21})$ & $(a_{22}, b_{22})$ \\ \cline{2-3}
\end{tabular}
\end{center}
```

### 博弈树 (使用 tikz)

```latex
\usepackage{tikz}
\usetikzlibrary{trees}

\begin{tikzpicture}[
    level 1/.style={sibling distance=4cm, level distance=2cm},
    level 2/.style={sibling distance=2cm, level distance=2cm}
]
\node {Player 1}
    child {node {Player 2}
        child {node {$(3,1)$} edge from parent node[left] {L}}
        child {node {$(0,0)$} edge from parent node[right] {R}}
        edge from parent node[left] {A}
    }
    child {node {Player 2}
        child {node {$(2,2)$} edge from parent node[left] {L}}
        child {node {$(1,3)$} edge from parent node[right] {R}}
        edge from parent node[right] {B}
    };
\end{tikzpicture}
```

---

## 6. 机器学习/优化专用

### 优化问题

```latex
\begin{align*}
\min_{x \in \R^n} \quad & f(x) \\
\text{subject to} \quad & g_i(x) \leq 0, \quad i = 1, \ldots, m \\
& h_j(x) = 0, \quad j = 1, \ldots, p
\end{align*}
```

### 梯度与 Hessian

```latex
\nabla f(x) = \begin{pmatrix}
\frac{\partial f}{\partial x_1} \\
\vdots \\
\frac{\partial f}{\partial x_n}
\end{pmatrix}

\nabla^2 f(x) = \begin{pmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{pmatrix}
```

### 算法伪代码

```latex
\begin{algorithm}
\caption{Gradient Descent}
\begin{algorithmic}[1]
\Require $f$: objective function, $x_0$: initial point, $\alpha$: step size
\Ensure $x^*$: approximate minimizer
\State $x \gets x_0$
\While{not converged}
    \State $g \gets \nabla f(x)$
    \State $x \gets x - \alpha g$
\EndWhile
\State \Return $x$
\end{algorithmic}
\end{algorithm}
```

---

## 7. 概率与统计专用

### 条件概率

```latex
\Prob(A \mid B) = \frac{\Prob(A \cap B)}{\Prob(B)}
```

### 期望和方差

```latex
\E[X] = \sum_{x} x \cdot \Prob(X = x)

\Var(X) = \E[X^2] - (\E[X])^2 = \E[(X - \mu)^2]
```

### 分布

```latex
% 正态分布
X \sim \mathcal{N}(\mu, \sigma^2)

f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right)

% 泊松分布
X \sim \text{Poisson}(\lambda)

\Prob(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
```

---

## 8. 常用符号速查

### 希腊字母

| 小写 | 大写 | LaTeX |
|------|------|-------|
| α | A | `\alpha` |
| β | B | `\beta` |
| γ | Γ | `\gamma`, `\Gamma` |
| δ | Δ | `\delta`, `\Delta` |
| ε | E | `\epsilon`, `\varepsilon` |
| λ | Λ | `\lambda`, `\Lambda` |
| μ | M | `\mu` |
| σ | Σ | `\sigma`, `\Sigma` |
| φ | Φ | `\phi`, `\varphi`, `\Phi` |
| ω | Ω | `\omega`, `\Omega` |

### 关系符号

| 符号 | LaTeX |
|------|-------|
| ≤, ≥ | `\leq`, `\geq` |
| ≠ | `\neq` |
| ≈ | `\approx` |
| ∈, ∉ | `\in`, `\notin` |
| ⊆, ⊂ | `\subseteq`, `\subset` |
| ∀, ∃ | `\forall`, `\exists` |
| → | `\to`, `\rightarrow` |
| ⟹ | `\implies` |
| ⟺ | `\iff` |

### 其他常用

| 符号 | LaTeX |
|------|-------|
| ∞ | `\infty` |
| ∂ | `\partial` |
| ∇ | `\nabla` |
| · | `\cdot` |
| × | `\times` |
| ⊗ | `\otimes` |
| □ | `\square`, `\Box` |
| ∎ | `\qed`, `\blacksquare` |
