# Human-Like Writing Style Guide

类人写作风格指南，用于生成自然、不被 AI 检测器识别的学术写作。

---

## 核心原则

### 1. 结构多样性

**问题**: AI 生成的内容往往结构高度对称

**解决方案**: 刻意引入结构变化

```
❌ AI 风格（高度对称）:
Problem 1:
- Step 1: [explanation]
- Step 2: [explanation]
- Step 3: [explanation]

Problem 2:
- Step 1: [explanation]
- Step 2: [explanation]
- Step 3: [explanation]

✅ 人类风格（结构变化）:
Problem 1:
We start by observing that... Then, using Theorem 2.1...
The result follows immediately.

Problem 2:
This problem requires a different approach. First, note that...
After some algebraic manipulation, we obtain...
Finally, substituting back gives us the answer.
```

### 2. 自然语言过渡

**避免**: 机械的过渡词

**使用**: 自然的学术表达

| 避免 (AI 特征) | 使用 (自然) |
|---------------|-------------|
| "Let's break this down step by step" | "We begin by..." |
| "Now, let's consider..." | "Consider now..." / "Next," |
| "This brings us to our next point" | "From this," / "It follows that" |
| "In conclusion," | "Therefore," / "Thus," |
| "It's important to note that" | "Note that" / "Observe that" |

### 3. 简洁表达

**原则**: 显而易见的步骤可以省略或简化

```
❌ 过度解释:
Since x is a positive real number, and we know that the square
of any real number is non-negative, we can conclude that x² ≥ 0.
This is a fundamental property of real numbers.

✅ 简洁:
Since x > 0, we have x² > 0.
```

---

## 学术写作常用表达库

### 开始解答

| 中文思路 | English Expression |
|---------|-------------------|
| 首先考虑 | We first consider... / Consider first... |
| 不失一般性 | Without loss of generality (WLOG), |
| 设/令 | Let... / Suppose... / Assume... |
| 由定义 | By definition, |
| 根据定理 | By Theorem X.X, / From Theorem X.X, |
| 回顾 | Recall that... |

### 推导过程

| 中文思路 | English Expression |
|---------|-------------------|
| 因此 | Therefore, / Thus, / Hence, |
| 不难发现 | It is easy to see that... / Observe that... |
| 显然 | Clearly, / Obviously, (慎用) |
| 类似地 | Similarly, / By a similar argument, |
| 特别地 | In particular, |
| 换句话说 | In other words, / That is, |
| 注意到 | Note that... / Notice that... |

### 计算步骤

| 中文思路 | English Expression |
|---------|-------------------|
| 代入 | Substituting... / Plugging in... |
| 化简 | Simplifying, / This simplifies to... |
| 整理得 | Rearranging, / Collecting terms, |
| 约去 | Canceling... / The ... terms cancel. |
| 展开 | Expanding, |

### 结论

| 中文思路 | English Expression |
|---------|-------------------|
| 综上所述 | To summarize, / In summary, |
| 证毕 | ∎ / Q.E.D. / This completes the proof. |
| 所以 | So / Thus / Therefore |
| 最终答案 | The answer is... / We conclude that... |

---

## 风格变化技巧

### 1. 句式变化

```
变化1: 主语不同
- "We observe that..."
- "The result shows that..."
- "This implies..."
- "It follows that..."

变化2: 主动/被动交替
- "We can easily verify that..." (主动)
- "It can be verified that..." (被动)
- "This is verified by..." (被动)

变化3: 长短句交替
- "Since f is continuous, the limit exists." (短)
- "Given the continuity of f on the closed interval [a,b],
   and applying the Extreme Value Theorem, we conclude that
   f attains its maximum and minimum values." (长)
```

### 2. 证明结构变化

```
结构1: 直接证明
"We prove this directly. Let x ∈ A. Then... Therefore x ∈ B."

结构2: 反证法
"Suppose, for contradiction, that P does not hold. Then...
This contradicts our assumption. Hence P must hold."

结构3: 分情况讨论
"We consider two cases.
Case 1: x > 0. In this case...
Case 2: x ≤ 0. Here..."

结构4: 数学归纳法
"We proceed by induction on n.
Base case (n=1): [verification]
Inductive step: Suppose the claim holds for n=k. We show it
holds for n=k+1..."
```

### 3. 省略与详写的平衡

```
详写场景:
- 题目的关键步骤
- 非平凡的推导
- 容易出错的地方

可省略:
- 基本的代数运算
- 显而易见的结论
- 重复性的计算

示例:
"Expanding and simplifying (details omitted), we get x = 3."
"A straightforward calculation shows that..."
"The verification is routine and left to the reader."
```

---

## 应避免的 AI 特征表达

### 绝对禁止

| 表达 | 问题 |
|------|------|
| "Let's break this down step by step" | 典型 AI 开场白 |
| "Great question!" | AI 客服风格 |
| "I'll walk you through this" | 过于口语化 |
| "Here's how we can approach this" | AI 模板化 |
| "This is a fascinating problem" | 不必要的情感表达 |
| "Let me explain" | 口语化 |

### 尽量避免

| 表达 | 替代方案 |
|------|---------|
| "It is worth noting that" | "Note that" |
| "It should be emphasized that" | 直接陈述 |
| "In order to" | "To" |
| "Due to the fact that" | "Since" / "Because" |
| "At this point in time" | "Now" |
| "In the event that" | "If" |

---

## 数学写作特殊技巧

### 1. 公式与文字的结合

```
❌ 断裂感:
The formula is:
x = 2
So the answer is 2.

✅ 流畅:
Solving for x gives x = 2, which is our answer.

或者:
We find that
    x = 2.
```

### 2. 引用定理

```
❌ 生硬:
We will use Theorem 3.2. By Theorem 3.2, we have...

✅ 自然:
By the Bolzano-Weierstrass theorem (Theorem 3.2), every
bounded sequence has a convergent subsequence.

或:
The result follows from Theorem 3.2.
```

### 3. 计算过程的呈现

```
❌ 过于详细:
x + 3 = 7
x + 3 - 3 = 7 - 3
x = 4

✅ 适度:
Solving x + 3 = 7 gives x = 4.

或者（对复杂计算）:
\begin{align*}
E[X] &= \sum_{i=1}^{n} x_i p_i \\
     &= 1 \cdot 0.3 + 2 \cdot 0.5 + 3 \cdot 0.2 \\
     &= 1.9
\end{align*}
```

---

## 示例对比

### 证明题示例

**题目**: Prove that if $f$ is continuous on $[a,b]$ and $f(a) < 0 < f(b)$, then there exists $c \in (a,b)$ such that $f(c) = 0$.

**❌ AI 风格**:

> Let's break this down step by step.
>
> Step 1: We need to understand what we're trying to prove.
> We want to show that there exists a point c...
>
> Step 2: We'll use the Intermediate Value Theorem.
> The Intermediate Value Theorem states that...
>
> Step 3: Let's apply it to our situation.
> Since f is continuous on [a,b], and we have f(a) < 0 < f(b)...
>
> Step 4: Therefore, we can conclude that...

**✅ 人类风格**:

> Since $f$ is continuous on $[a,b]$ with $f(a) < 0 < f(b)$, the Intermediate Value Theorem guarantees the existence of some $c \in (a,b)$ such that $f(c) = 0$. ∎

或者（如果需要更详细）:

> This is a direct application of the Intermediate Value Theorem. Note that $0$ lies strictly between $f(a)$ and $f(b)$. Since $f$ is continuous on the closed interval $[a,b]$, the IVT implies that $f$ attains every value between $f(a)$ and $f(b)$, including $0$. Thus there exists $c \in (a,b)$ with $f(c) = 0$.

---

## 自检清单

写完后检查：

- [ ] 没有使用 "Let's break this down" 等 AI 特征表达
- [ ] 各题的结构不完全相同
- [ ] 使用了多种过渡表达
- [ ] 简单步骤没有过度解释
- [ ] 句式有长有短
- [ ] 整体读起来像是人写的
